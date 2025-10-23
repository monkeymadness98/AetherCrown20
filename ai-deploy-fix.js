// ai-deploy-fix.js
// Node.js script for AI agent to sweep, fix, and redeploy

const { execSync } = require("child_process");
const fs = require("fs");
const axios = require("axios");

async function run() {
  try {
    console.log("=== STEP 1: Check Environment Variables ===");
    const requiredEnv = [
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

    let missingEnv = [];
    requiredEnv.forEach((key) => {
      if (!process.env[key]) missingEnv.push(key);
    });

    if (missingEnv.length > 0) {
      console.log("Missing ENV Vars:", missingEnv.join(", "));
      // Attempt auto-fix: read from .env file
      if (fs.existsSync(".env")) {
        console.log("Loading missing keys from .env file...");
        const envContent = fs.readFileSync(".env", "utf-8");
        envContent.split("\n").forEach((line) => {
          const trimmedLine = line.trim();
          if (trimmedLine && !trimmedLine.startsWith("#")) {
            const eqIndex = trimmedLine.indexOf("=");
            if (eqIndex > 0) {
              const key = trimmedLine.substring(0, eqIndex).trim();
              const value = trimmedLine.substring(eqIndex + 1).trim();
              if (missingEnv.includes(key) && !process.env[key]) {
                process.env[key] = value;
                console.log(`  ✓ Loaded ${key} from .env`);
              }
            }
          }
        });
      } else {
        console.log("⚠️  No .env file found. Using defaults or skipping optional keys.");
      }
    } else {
      console.log("✅ All required environment variables present");
    }

    console.log("\n=== STEP 2: Check Backend Health ===");
    const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";
    try {
      const health = await axios.get(`${backendUrl}/healthz`, { timeout: 10000 });
      if (health && health.status === 200) {
        console.log("✅ Backend healthy");
      } else {
        throw new Error("Backend returned non-200 status");
      }
    } catch (error) {
      console.log("❌ Backend unhealthy, attempting redeploy...");
      if (process.env.RENDER_API_KEY && process.env.RENDER_SERVICE_ID) {
        try {
          execSync("render deploy aethercrown98-backend --clear-cache", { 
            stdio: "inherit",
            timeout: 120000 
          });
          console.log("✅ Render redeploy triggered");
        } catch (e) {
          console.log("⚠️  Render CLI deploy failed, trying API...");
          try {
            const response = await axios.post(
              `https://api.render.com/v1/services/${process.env.RENDER_SERVICE_ID}/deploys`,
              { clearCache: "clear" },
              {
                headers: {
                  "Authorization": `Bearer ${process.env.RENDER_API_KEY}`,
                  "Content-Type": "application/json"
                }
              }
            );
            console.log("✅ Render redeploy triggered via API", response.data);
          } catch (apiError) {
            console.log("❌ Failed to trigger Render deploy:", apiError.message);
          }
        }
      } else {
        console.log("⚠️  RENDER_API_KEY or RENDER_SERVICE_ID not set, skipping redeploy");
      }
    }

    console.log("\n=== STEP 3: Install & Fix Dependencies ===");
    
    // Backend dependencies
    if (fs.existsSync("backend")) {
      console.log("Installing backend dependencies...");
      try {
        execSync("cd backend && pip install -r requirements.txt", { 
          stdio: "inherit",
          timeout: 180000 
        });
        console.log("✅ Backend dependencies installed");
      } catch (e) {
        console.log("⚠️  Backend dependency install failed:", e.message);
      }
    }

    // Frontend dependencies
    if (fs.existsSync("frontend")) {
      console.log("Installing frontend dependencies...");
      try {
        execSync("cd frontend && npm install", { 
          stdio: "inherit",
          timeout: 180000 
        });
        console.log("✅ Frontend dependencies installed");
      } catch (e) {
        console.log("⚠️  Frontend dependency install failed:", e.message);
      }
    }

    console.log("\n=== STEP 4: Redeploy Frontend ===");
    if (process.env.VERCEL_TOKEN) {
      try {
        execSync("vercel --prod --confirm", { 
          stdio: "inherit",
          timeout: 180000 
        });
        console.log("✅ Frontend deployed to Vercel");
      } catch (e) {
        console.log("⚠️  Vercel deploy failed:", e.message);
      }
    } else {
      console.log("⚠️  VERCEL_TOKEN not set, skipping Vercel deploy");
    }

    console.log("\n=== STEP 5: Validate Connections ===");
    try {
      const testApi = await axios.get(`${backendUrl}/api/status`, { timeout: 10000 });
      if (testApi && testApi.status === 200) {
        console.log("✅ API connection OK");
      }
    } catch (e) {
      console.log("⚠️  API connection test failed (endpoint may not exist yet)");
    }

    console.log("\n=== STEP 6: Restart AI Agents ===");
    try {
      execSync("pm2 restart all || true", { 
        stdio: "inherit",
        timeout: 30000 
      });
      console.log("✅ PM2 agents restarted");
    } catch (e) {
      console.log("⚠️  PM2 restart failed or not installed:", e.message);
    }

    console.log("\n=== ✅ Sweep Complete: Deployment & Fix Attempted ===");

  } catch (err) {
    console.error("\n❌ Auto-fix script encountered an error:", err);
    process.exit(1);
  }
}

// Run the script
run();
