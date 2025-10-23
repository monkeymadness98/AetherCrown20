#!/usr/bin/env node
// scripts/deploy-frontend.js
// Deploy frontend to Vercel

const { execSync } = require("child_process");
const fs = require("fs");

async function deployFrontend() {
  const vercelToken = process.env.VERCEL_TOKEN;

  if (!vercelToken) {
    console.error("❌ Error: VERCEL_TOKEN must be set");
    process.exit(1);
  }

  console.log("=== Deploying Frontend to Vercel ===\n");

  // Determine deploy path
  const deployPath = fs.existsSync("frontend") ? "frontend" : ".";
  console.log(`Deploy path: ${deployPath}`);

  try {
    // Install Vercel CLI if not available
    try {
      execSync("vercel --version", { stdio: "ignore" });
    } catch {
      console.log("Installing Vercel CLI...");
      execSync("npm install -g vercel@latest", { stdio: "inherit" });
    }

    // Deploy
    console.log("\nDeploying to production...");
    execSync(`vercel ${deployPath} --prod --confirm --token ${vercelToken}`, {
      stdio: "inherit",
      env: { ...process.env, VERCEL_TOKEN: vercelToken },
    });

    console.log("\n✅ Frontend deployed successfully!");
    process.exit(0);
  } catch (error) {
    console.error("❌ Deploy failed:", error.message);
    process.exit(1);
  }
}

deployFrontend();
