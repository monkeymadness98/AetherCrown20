// ai-agent-sweep.js
// Comprehensive AI Agent Repo Automation Script
// Handles continuous deployment, monitoring, error sweeps, and auto-fixes

const { execSync, exec } = require("child_process");
const fs = require("fs");
const path = require("path");
const axios = require("axios");
const { promisify } = require("util");

const execAsync = promisify(exec);

class AIAgentSweep {
  constructor() {
    this.config = {
      backendUrl: process.env.BACKEND_URL || "http://localhost:8000",
      frontendUrl: process.env.FRONTEND_URL || "http://localhost:3000",
      environment: process.env.ENVIRONMENT || "development",
      supabaseUrl: process.env.SUPABASE_URL,
      supabaseKey: process.env.SUPABASE_SERVICE_ROLE_KEY,
      renderApiKey: process.env.RENDER_API_KEY,
      renderServiceId: process.env.RENDER_SERVICE_ID,
      vercelToken: process.env.VERCEL_TOKEN,
      sentryDsn: process.env.SENTRY_DSN,
      healthchecksUrl: process.env.HEALTHCHECKS_URL,
    };

    this.report = {
      timestamp: new Date().toISOString(),
      environment: this.config.environment,
      checks: [],
      errors: [],
      fixes: [],
      warnings: [],
    };
  }

  log(level, category, message, data = {}) {
    const entry = { level, category, message, data, timestamp: new Date().toISOString() };
    console.log(`[${level.toUpperCase()}] [${category}] ${message}`);
    
    if (level === "error") {
      this.report.errors.push(entry);
    } else if (level === "fix") {
      this.report.fixes.push(entry);
    } else if (level === "warn") {
      this.report.warnings.push(entry);
    }
    
    this.report.checks.push(entry);
  }

  // 1️⃣ Environment Verification
  async verifyEnvironment() {
    this.log("info", "ENV", "=== Environment Verification ===");

    const requiredEnvVars = [
      "SUPABASE_URL",
      "SUPABASE_SERVICE_ROLE_KEY",
      "PAYPAL_CLIENT_ID",
      "PAYPAL_SECRET",
      "STRIPE_SECRET_KEY",
      "FRONTEND_URL",
      "BACKEND_URL",
      "SENTRY_DSN",
      "HEALTHCHECKS_URL",
      "ENVIRONMENT",
    ];

    const optionalEnvVars = [
      "RENDER_API_KEY",
      "RENDER_SERVICE_ID",
      "VERCEL_TOKEN",
      "VERCEL_PROJECT_ID",
      "VERCEL_ORG_ID",
    ];

    let missing = [];
    let missingOptional = [];

    requiredEnvVars.forEach((key) => {
      if (!process.env[key]) missing.push(key);
    });

    optionalEnvVars.forEach((key) => {
      if (!process.env[key]) missingOptional.push(key);
    });

    if (missing.length > 0) {
      this.log("warn", "ENV", `Missing required env vars: ${missing.join(", ")}`);

      // Auto-load from .env file
      if (fs.existsSync(".env")) {
        this.log("fix", "ENV", "Attempting to load from .env file...");
        const envContent = fs.readFileSync(".env", "utf-8");
        envContent.split("\n").forEach((line) => {
          const trimmedLine = line.trim();
          if (trimmedLine && !trimmedLine.startsWith("#")) {
            const eqIndex = trimmedLine.indexOf("=");
            if (eqIndex > 0) {
              const key = trimmedLine.substring(0, eqIndex).trim();
              const value = trimmedLine.substring(eqIndex + 1).trim();
              if (missing.includes(key) && !process.env[key]) {
                process.env[key] = value;
                this.log("fix", "ENV", `Loaded ${key} from .env file`);
              }
            }
          }
        });
      }
    } else {
      this.log("info", "ENV", "✅ All required environment variables present");
    }

    if (missingOptional.length > 0) {
      this.log("info", "ENV", `Optional env vars not set: ${missingOptional.join(", ")}`);
    }

    // Validate URLs point to correct backends
    if (process.env.FRONTEND_URL && process.env.BACKEND_URL) {
      this.log("info", "ENV", `Frontend: ${process.env.FRONTEND_URL} → Backend: ${process.env.BACKEND_URL}`);
    }

    return { missing, missingOptional };
  }

  // 2️⃣ Backend Health & Redeploy
  async checkBackendHealth() {
    this.log("info", "BACKEND", "=== Backend Health Check ===");

    try {
      const healthUrl = `${this.config.backendUrl}/healthz`;
      this.log("info", "BACKEND", `Checking ${healthUrl}...`);
      
      const response = await axios.get(healthUrl, { timeout: 15000 });
      
      if (response.status === 200) {
        this.log("info", "BACKEND", "✅ Backend healthy", response.data);
        return { healthy: true, data: response.data };
      } else {
        throw new Error(`Backend returned status ${response.status}`);
      }
    } catch (error) {
      this.log("error", "BACKEND", `❌ Backend unhealthy: ${error.message}`);

      // Attempt auto-redeploy
      if (this.config.renderApiKey && this.config.renderServiceId) {
        this.log("fix", "BACKEND", "Attempting Render redeploy with cache clear...");
        try {
          const deployResponse = await axios.post(
            `https://api.render.com/v1/services/${this.config.renderServiceId}/deploys`,
            { clearCache: "clear" },
            {
              headers: {
                "Authorization": `Bearer ${this.config.renderApiKey}`,
                "Content-Type": "application/json",
              },
            }
          );
          this.log("fix", "BACKEND", "✅ Render redeploy triggered", deployResponse.data);
        } catch (deployError) {
          this.log("error", "BACKEND", `Failed to redeploy: ${deployError.message}`);
        }
      } else {
        this.log("warn", "BACKEND", "Cannot auto-redeploy: RENDER_API_KEY or RENDER_SERVICE_ID not set");
      }

      return { healthy: false, error: error.message };
    }
  }

  // 3️⃣ Dependency Fix & Build
  async fixDependencies() {
    this.log("info", "DEPS", "=== Dependency Fix & Build ===");

    // Backend dependencies
    if (fs.existsSync("backend/requirements.txt")) {
      this.log("info", "DEPS", "Installing backend dependencies...");
      try {
        execSync("cd backend && pip install -r requirements.txt", {
          stdio: "inherit",
          timeout: 300000,
        });
        this.log("fix", "DEPS", "✅ Backend dependencies installed");
      } catch (error) {
        this.log("error", "DEPS", `Backend dependency install failed: ${error.message}`);
      }
    }

    // Root requirements.txt
    if (fs.existsSync("requirements.txt")) {
      this.log("info", "DEPS", "Installing root dependencies...");
      try {
        execSync("pip install -r requirements.txt", {
          stdio: "inherit",
          timeout: 300000,
        });
        this.log("fix", "DEPS", "✅ Root dependencies installed");
      } catch (error) {
        this.log("error", "DEPS", `Root dependency install failed: ${error.message}`);
      }
    }

    // Frontend dependencies
    if (fs.existsSync("frontend/package.json")) {
      this.log("info", "DEPS", "Installing frontend dependencies...");
      try {
        execSync("cd frontend && npm install", {
          stdio: "inherit",
          timeout: 300000,
        });
        this.log("fix", "DEPS", "✅ Frontend dependencies installed");

        // Build frontend
        this.log("info", "DEPS", "Building frontend...");
        execSync("cd frontend && npm run build", {
          stdio: "inherit",
          timeout: 300000,
        });
        this.log("fix", "DEPS", "✅ Frontend built successfully");
      } catch (error) {
        this.log("error", "DEPS", `Frontend operations failed: ${error.message}`);
      }
    }

    return { success: true };
  }

  // 4️⃣ Frontend Deployment
  async deployFrontend() {
    this.log("info", "FRONTEND", "=== Frontend Deployment ===");

    if (!this.config.vercelToken) {
      this.log("warn", "FRONTEND", "VERCEL_TOKEN not set, skipping deployment");
      return { deployed: false, reason: "No token" };
    }

    try {
      this.log("info", "FRONTEND", "Deploying to Vercel...");
      
      // Check if frontend directory exists or deploy root
      const deployPath = fs.existsSync("frontend") ? "frontend" : ".";
      
      execSync(`vercel ${deployPath} --prod --confirm --token ${this.config.vercelToken}`, {
        stdio: "inherit",
        timeout: 300000,
        env: { ...process.env, VERCEL_TOKEN: this.config.vercelToken },
      });
      
      this.log("fix", "FRONTEND", "✅ Frontend deployed to Vercel");

      // Verify deployment
      await this.sleep(10000); // Wait for deployment to propagate
      
      try {
        const response = await axios.get(this.config.frontendUrl, { timeout: 10000 });
        if (response.status === 200) {
          this.log("info", "FRONTEND", "✅ Frontend accessible and responding");
        }
      } catch (error) {
        this.log("warn", "FRONTEND", "Frontend deployed but not yet accessible");
      }

      return { deployed: true };
    } catch (error) {
      this.log("error", "FRONTEND", `Deployment failed: ${error.message}`);
      return { deployed: false, error: error.message };
    }
  }

  // 5️⃣ AI Agent Verification
  async verifyAIAgents() {
    this.log("info", "AI_AGENTS", "=== AI Agent Verification ===");

    try {
      // Check if PM2 is available
      const { stdout } = await execAsync("pm2 list").catch(() => ({ stdout: "" }));
      
      if (stdout) {
        this.log("info", "AI_AGENTS", "PM2 agents status:");
        console.log(stdout);

        // Parse PM2 output to detect failed agents
        if (stdout.includes("errored") || stdout.includes("stopped")) {
          this.log("fix", "AI_AGENTS", "Restarting failed/stopped agents...");
          execSync("pm2 restart all", { stdio: "inherit" });
          this.log("fix", "AI_AGENTS", "✅ Agents restarted");
        } else {
          this.log("info", "AI_AGENTS", "✅ All agents running");
        }
      } else {
        this.log("info", "AI_AGENTS", "PM2 not available or no agents configured");
      }

      return { verified: true };
    } catch (error) {
      this.log("warn", "AI_AGENTS", `Agent check failed: ${error.message}`);
      return { verified: false, error: error.message };
    }
  }

  // 6️⃣ Database & Service Check
  async checkDatabaseAndServices() {
    this.log("info", "DB_SERVICES", "=== Database & Service Check ===");

    // Check Supabase connectivity
    if (this.config.supabaseUrl && this.config.supabaseKey) {
      try {
        const response = await axios.get(`${this.config.supabaseUrl}/rest/v1/`, {
          headers: {
            apikey: this.config.supabaseKey,
            Authorization: `Bearer ${this.config.supabaseKey}`,
          },
          timeout: 10000,
        });
        this.log("info", "DB_SERVICES", "✅ Supabase connectivity OK");
      } catch (error) {
        this.log("error", "DB_SERVICES", `Supabase connection failed: ${error.message}`);
      }
    } else {
      this.log("info", "DB_SERVICES", "Supabase credentials not configured");
    }

    // Test payment integrations (without making actual charges)
    if (process.env.STRIPE_SECRET_KEY) {
      this.log("info", "DB_SERVICES", "✅ Stripe credentials configured");
    }

    if (process.env.PAYPAL_CLIENT_ID && process.env.PAYPAL_SECRET) {
      this.log("info", "DB_SERVICES", "✅ PayPal credentials configured");
    }

    return { checked: true };
  }

  // 7️⃣ UI & Dashboard Check
  async checkUIAndDashboard() {
    this.log("info", "UI", "=== UI & Dashboard Check ===");

    const dashboardUrls = [
      { name: "Dev Hub", url: `${this.config.frontendUrl}/dev` },
      { name: "Live Dashboard", url: `${this.config.frontendUrl}/live` },
      { name: "Main Page", url: this.config.frontendUrl },
    ];

    for (const dashboard of dashboardUrls) {
      try {
        const response = await axios.get(dashboard.url, { timeout: 10000 });
        if (response.status === 200) {
          this.log("info", "UI", `✅ ${dashboard.name} accessible`);
        }
      } catch (error) {
        this.log("warn", "UI", `${dashboard.name} not accessible: ${error.message}`);
      }
    }

    return { checked: true };
  }

  // 8️⃣ Monitoring & Reporting
  async generateReport() {
    this.log("info", "REPORT", "=== Generating Sweep Report ===");

    const reportPath = path.join("/tmp", `sweep-report-${Date.now()}.json`);
    
    this.report.summary = {
      totalChecks: this.report.checks.length,
      errors: this.report.errors.length,
      fixes: this.report.fixes.length,
      warnings: this.report.warnings.length,
      environment: this.config.environment,
    };

    fs.writeFileSync(reportPath, JSON.stringify(this.report, null, 2));
    this.log("info", "REPORT", `✅ Report saved to ${reportPath}`);

    // Display summary
    console.log("\n" + "=".repeat(60));
    console.log("SWEEP SUMMARY");
    console.log("=".repeat(60));
    console.log(`Total Checks: ${this.report.summary.totalChecks}`);
    console.log(`Errors: ${this.report.summary.errors}`);
    console.log(`Auto-Fixes Applied: ${this.report.summary.fixes}`);
    console.log(`Warnings: ${this.report.summary.warnings}`);
    console.log(`Environment: ${this.report.summary.environment}`);
    console.log("=".repeat(60) + "\n");

    if (this.report.errors.length > 0) {
      console.log("❌ ERRORS REQUIRING MANUAL INTERVENTION:");
      this.report.errors.forEach((err, i) => {
        console.log(`  ${i + 1}. [${err.category}] ${err.message}`);
      });
      console.log();
    }

    if (this.report.fixes.length > 0) {
      console.log("✅ AUTO-FIXES APPLIED:");
      this.report.fixes.forEach((fix, i) => {
        console.log(`  ${i + 1}. [${fix.category}] ${fix.message}`);
      });
      console.log();
    }

    // Send to health checks service if configured
    if (this.config.healthchecksUrl) {
      try {
        await axios.post(this.config.healthchecksUrl, this.report);
        this.log("info", "REPORT", "✅ Report sent to health checks service");
      } catch (error) {
        this.log("warn", "REPORT", `Failed to send to health checks: ${error.message}`);
      }
    }

    return this.report;
  }

  // 9️⃣ Post-Fix Deployment
  async postFixDeployment() {
    this.log("info", "POST_FIX", "=== Post-Fix Deployment ===");

    // If critical errors were auto-fixed, retry deployments
    if (this.report.fixes.length > 0) {
      const hasCriticalFixes = this.report.fixes.some(
        (fix) => fix.category === "BACKEND" || fix.category === "DEPS"
      );

      if (hasCriticalFixes) {
        this.log("info", "POST_FIX", "Critical fixes applied, retrying backend health check...");
        await this.sleep(30000); // Wait for services to stabilize
        await this.checkBackendHealth();
      }
    }

    // Final validation
    try {
      const healthUrl = `${this.config.backendUrl}/healthz`;
      const response = await axios.get(healthUrl, { timeout: 10000 });
      
      if (response.status === 200) {
        this.log("info", "POST_FIX", "✅ Final health check: Backend operational");
      }
    } catch (error) {
      this.log("error", "POST_FIX", "❌ Final health check: Backend still unhealthy");
    }

    return { completed: true };
  }

  // Utility: Sleep function
  sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  // Main execution
  async execute() {
    console.log("\n" + "=".repeat(60));
    console.log("AI AGENT DEPLOYMENT SWEEP");
    console.log(`Started at: ${new Date().toISOString()}`);
    console.log(`Environment: ${this.config.environment}`);
    console.log("=".repeat(60) + "\n");

    try {
      await this.verifyEnvironment();
      await this.checkBackendHealth();
      await this.fixDependencies();
      await this.deployFrontend();
      await this.verifyAIAgents();
      await this.checkDatabaseAndServices();
      await this.checkUIAndDashboard();
      await this.postFixDeployment();
      await this.generateReport();

      console.log("\n✅ Sweep completed successfully\n");
      process.exit(0);
    } catch (error) {
      console.error("\n❌ Sweep failed with error:", error);
      this.log("error", "SWEEP", `Fatal error: ${error.message}`, { stack: error.stack });
      await this.generateReport();
      process.exit(1);
    }
  }
}

// Run if executed directly
if (require.main === module) {
  const sweep = new AIAgentSweep();
  sweep.execute();
}

module.exports = AIAgentSweep;
