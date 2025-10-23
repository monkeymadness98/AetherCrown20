#!/usr/bin/env node
// scripts/verify-env.js
// Verify environment variables are properly set

const fs = require("fs");

function verifyEnv() {
  console.log("=== Environment Variable Verification ===\n");

  const requiredEnvVars = [
    { key: "SUPABASE_URL", category: "Database" },
    { key: "SUPABASE_SERVICE_ROLE_KEY", category: "Database" },
    { key: "PAYPAL_CLIENT_ID", category: "Payments" },
    { key: "PAYPAL_SECRET", category: "Payments" },
    { key: "STRIPE_SECRET_KEY", category: "Payments" },
    { key: "FRONTEND_URL", category: "URLs" },
    { key: "BACKEND_URL", category: "URLs" },
    { key: "SENTRY_DSN", category: "Monitoring" },
    { key: "HEALTHCHECKS_URL", category: "Monitoring" },
    { key: "ENVIRONMENT", category: "Configuration" },
  ];

  const optionalEnvVars = [
    { key: "RENDER_API_KEY", category: "Deployment" },
    { key: "RENDER_SERVICE_ID", category: "Deployment" },
    { key: "VERCEL_TOKEN", category: "Deployment" },
    { key: "VERCEL_PROJECT_ID", category: "Deployment" },
    { key: "VERCEL_ORG_ID", category: "Deployment" },
  ];

  const results = {
    required: { present: [], missing: [] },
    optional: { present: [], missing: [] },
  };

  // Check required vars
  console.log("Required Environment Variables:");
  requiredEnvVars.forEach((envVar) => {
    const value = process.env[envVar.key];
    const status = value ? "✅" : "❌";
    const display = value ? "(set)" : "(MISSING)";
    console.log(`  ${status} ${envVar.key} [${envVar.category}]: ${display}`);

    if (value) {
      results.required.present.push(envVar.key);
    } else {
      results.required.missing.push(envVar.key);
    }
  });

  console.log("\nOptional Environment Variables:");
  optionalEnvVars.forEach((envVar) => {
    const value = process.env[envVar.key];
    const status = value ? "✅" : "⚠️ ";
    const display = value ? "(set)" : "(not set)";
    console.log(`  ${status} ${envVar.key} [${envVar.category}]: ${display}`);

    if (value) {
      results.optional.present.push(envVar.key);
    } else {
      results.optional.missing.push(envVar.key);
    }
  });

  // Summary
  console.log("\n=== Summary ===");
  console.log(`Required: ${results.required.present.length}/${requiredEnvVars.length} present`);
  console.log(`Optional: ${results.optional.present.length}/${optionalEnvVars.length} present`);

  if (results.required.missing.length > 0) {
    console.log("\n❌ Missing required variables:");
    results.required.missing.forEach((key) => console.log(`   - ${key}`));
    console.log("\n💡 Tip: Create a .env file or set these in your environment");
    
    // Check if .env.example exists
    if (fs.existsSync(".env.example")) {
      console.log("   Reference .env.example for guidance");
    }
    
    process.exit(1);
  } else {
    console.log("\n✅ All required environment variables are set!");
    process.exit(0);
  }
}

verifyEnv();
