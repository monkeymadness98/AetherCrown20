#!/usr/bin/env node
// scripts/health-check.js
// Standalone health check utility for monitoring services

const axios = require("axios");

async function healthCheck() {
  const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";
  const frontendUrl = process.env.FRONTEND_URL || "http://localhost:3000";

  console.log("=== AetherCrown20 Health Check ===\n");

  const results = {
    backend: { status: "unknown", details: null },
    frontend: { status: "unknown", details: null },
    timestamp: new Date().toISOString(),
  };

  // Check Backend
  console.log(`Checking Backend: ${backendUrl}/healthz`);
  try {
    const response = await axios.get(`${backendUrl}/healthz`, { timeout: 10000 });
    if (response.status === 200) {
      results.backend.status = "healthy";
      results.backend.details = response.data;
      console.log("✅ Backend: Healthy");
      console.log("   Response:", JSON.stringify(response.data, null, 2));
    } else {
      results.backend.status = "unhealthy";
      results.backend.details = { statusCode: response.status };
      console.log(`⚠️  Backend: Returned status ${response.status}`);
    }
  } catch (error) {
    results.backend.status = "error";
    results.backend.details = { error: error.message };
    console.log("❌ Backend: Error -", error.message);
  }

  // Check Frontend
  console.log(`\nChecking Frontend: ${frontendUrl}`);
  try {
    const response = await axios.get(frontendUrl, { timeout: 10000 });
    if (response.status === 200) {
      results.frontend.status = "healthy";
      results.frontend.details = { statusCode: response.status };
      console.log("✅ Frontend: Healthy");
    } else {
      results.frontend.status = "unhealthy";
      results.frontend.details = { statusCode: response.status };
      console.log(`⚠️  Frontend: Returned status ${response.status}`);
    }
  } catch (error) {
    results.frontend.status = "error";
    results.frontend.details = { error: error.message };
    console.log("❌ Frontend: Error -", error.message);
  }

  // Summary
  console.log("\n=== Summary ===");
  console.log(`Backend:  ${results.backend.status}`);
  console.log(`Frontend: ${results.frontend.status}`);
  console.log(`Timestamp: ${results.timestamp}`);

  // Exit code based on health
  const allHealthy = results.backend.status === "healthy" && results.frontend.status === "healthy";
  process.exit(allHealthy ? 0 : 1);
}

healthCheck();
