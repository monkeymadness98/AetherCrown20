#!/usr/bin/env node
// scripts/deploy-backend.js
// Trigger backend deployment to Render

const axios = require("axios");

async function deployBackend() {
  const renderApiKey = process.env.RENDER_API_KEY;
  const renderServiceId = process.env.RENDER_SERVICE_ID;

  if (!renderApiKey || !renderServiceId) {
    console.error("❌ Error: RENDER_API_KEY and RENDER_SERVICE_ID must be set");
    process.exit(1);
  }

  console.log("=== Deploying Backend to Render ===\n");
  console.log(`Service ID: ${renderServiceId}`);

  try {
    const response = await axios.post(
      `https://api.render.com/v1/services/${renderServiceId}/deploys`,
      { clearCache: "clear" },
      {
        headers: {
          "Authorization": `Bearer ${renderApiKey}`,
          "Content-Type": "application/json",
        },
      }
    );

    console.log("✅ Deploy triggered successfully!");
    console.log("Response:", JSON.stringify(response.data, null, 2));
    console.log("\nCheck deployment status at: https://dashboard.render.com");
    process.exit(0);
  } catch (error) {
    console.error("❌ Deploy failed:", error.message);
    if (error.response) {
      console.error("Response data:", error.response.data);
    }
    process.exit(1);
  }
}

deployBackend();
