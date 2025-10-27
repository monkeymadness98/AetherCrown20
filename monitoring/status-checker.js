#!/usr/bin/env node

/**
 * Aether Empire Status Checker
 * 
 * Monitors the health of all services in the Aether AI Empire stack:
 * - Render Backend
 * - Supabase Edge Functions
 * - Vercel Frontend
 * 
 * Logs results to /logs/system_status.json
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

// Configuration
// NOTE: Update the URLs below with your actual deployment URLs
const CONFIG = {
  endpoints: [
    {
      name: 'Render Backend Health',
      url: 'https://aetherai-8wcw.onrender.com/healthz',
      type: 'backend'
    },
    {
      name: 'Render Backend API',
      url: 'https://aetherai-8wcw.onrender.com/clocks',
      type: 'backend'
    },
    // Note: Supabase function URL needs to be configured with actual project ID
    // Example: https://abcdefghij.supabase.co/functions/v1/aether-sync
    {
      name: 'Supabase Edge Function (aether-sync)',
      url: process.env.SUPABASE_FUNCTION_URL || 'https://placeholder.supabase.co/functions/v1/aether-sync',
      type: 'supabase',
      optional: true
    },
    // Note: Vercel URL needs to be configured with actual deployment URL
    {
      name: 'Vercel Frontend Health',
      url: process.env.VERCEL_APP_URL ? `${process.env.VERCEL_APP_URL}/api/health` : null,
      type: 'vercel',
      optional: true
    }
  ],
  logDir: path.join(__dirname, '..', 'logs'),
  logFile: 'system_status.json'
};

/**
 * Make HTTP/HTTPS request to check endpoint
 */
function checkEndpoint(endpoint) {
  return new Promise((resolve) => {
    if (!endpoint.url || endpoint.url.includes('placeholder')) {
      resolve({
        name: endpoint.name,
        url: endpoint.url || 'not-configured',
        status: 'skipped',
        statusCode: null,
        responseTime: null,
        message: 'Endpoint not configured',
        timestamp: new Date().toISOString()
      });
      return;
    }

    const startTime = Date.now();
    const urlObj = new URL(endpoint.url);
    const client = urlObj.protocol === 'https:' ? https : http;

    const options = {
      hostname: urlObj.hostname,
      port: urlObj.port,
      path: urlObj.pathname + urlObj.search,
      method: 'GET',
      timeout: 10000,
      headers: {
        'User-Agent': 'AetherEmpire-StatusChecker/1.0'
      }
    };

    const req = client.request(options, (res) => {
      const responseTime = Date.now() - startTime;
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        const result = {
          name: endpoint.name,
          url: endpoint.url,
          status: res.statusCode >= 200 && res.statusCode < 300 ? 'healthy' : 'unhealthy',
          statusCode: res.statusCode,
          responseTime: responseTime,
          timestamp: new Date().toISOString(),
          type: endpoint.type
        };

        // Try to parse JSON response
        try {
          result.response = JSON.parse(data);
        } catch (e) {
          result.response = data.substring(0, 200); // First 200 chars
        }

        resolve(result);
      });
    });

    req.on('error', (error) => {
      resolve({
        name: endpoint.name,
        url: endpoint.url,
        status: 'error',
        statusCode: null,
        responseTime: Date.now() - startTime,
        error: error.message,
        timestamp: new Date().toISOString(),
        type: endpoint.type
      });
    });

    req.on('timeout', () => {
      req.destroy();
      resolve({
        name: endpoint.name,
        url: endpoint.url,
        status: 'timeout',
        statusCode: null,
        responseTime: Date.now() - startTime,
        error: 'Request timeout (>10s)',
        timestamp: new Date().toISOString(),
        type: endpoint.type
      });
    });

    req.end();
  });
}

/**
 * Check all endpoints
 */
async function checkAllEndpoints() {
  console.log('🔍 Aether Empire Status Check');
  console.log('=' .repeat(50));
  console.log(`Timestamp: ${new Date().toISOString()}\n`);

  const results = [];

  for (const endpoint of CONFIG.endpoints) {
    if (endpoint.optional && !endpoint.url) {
      console.log(`⏭️  Skipping ${endpoint.name} (optional, not configured)`);
      continue;
    }

    console.log(`Checking ${endpoint.name}...`);
    const result = await checkEndpoint(endpoint);
    results.push(result);

    // Display result
    const icon = result.status === 'healthy' ? '✅' : 
                 result.status === 'skipped' ? '⏭️' : '❌';
    console.log(`${icon} ${result.name}: ${result.status} (${result.responseTime}ms)`);
    
    if (result.statusCode) {
      console.log(`   Status Code: ${result.statusCode}`);
    }
    
    if (result.error) {
      console.log(`   Error: ${result.error}`);
    }
    
    console.log('');
  }

  return results;
}

/**
 * Save results to log file
 */
function saveResults(results) {
  // Ensure log directory exists
  if (!fs.existsSync(CONFIG.logDir)) {
    fs.mkdirSync(CONFIG.logDir, { recursive: true });
  }

  const logFilePath = path.join(CONFIG.logDir, CONFIG.logFile);
  
  // Read existing log or create new
  let logData = { checks: [] };
  
  if (fs.existsSync(logFilePath)) {
    try {
      const existingData = fs.readFileSync(logFilePath, 'utf8');
      logData = JSON.parse(existingData);
    } catch (e) {
      console.warn('⚠️  Could not read existing log file, creating new');
    }
  }

  // Add new check results
  logData.checks.push({
    timestamp: new Date().toISOString(),
    results: results,
    summary: {
      total: results.length,
      healthy: results.filter(r => r.status === 'healthy').length,
      unhealthy: results.filter(r => r.status === 'unhealthy').length,
      errors: results.filter(r => r.status === 'error').length,
      skipped: results.filter(r => r.status === 'skipped').length
    }
  });

  // Keep only last 100 checks to prevent file from growing too large
  if (logData.checks.length > 100) {
    logData.checks = logData.checks.slice(-100);
  }

  // Write to file
  fs.writeFileSync(logFilePath, JSON.stringify(logData, null, 2));
  console.log(`📝 Results saved to ${logFilePath}`);
}

/**
 * Main execution
 */
async function main() {
  try {
    const results = await checkAllEndpoints();
    
    console.log('=' .repeat(50));
    console.log('📊 Summary');
    console.log('-'.repeat(50));
    
    const summary = {
      total: results.length,
      healthy: results.filter(r => r.status === 'healthy').length,
      unhealthy: results.filter(r => r.status === 'unhealthy').length,
      errors: results.filter(r => r.status === 'error').length,
      skipped: results.filter(r => r.status === 'skipped').length
    };
    
    console.log(`Total Endpoints: ${summary.total}`);
    console.log(`✅ Healthy: ${summary.healthy}`);
    console.log(`❌ Unhealthy: ${summary.unhealthy}`);
    console.log(`⚠️  Errors: ${summary.errors}`);
    console.log(`⏭️  Skipped: ${summary.skipped}`);
    
    saveResults(results);
    
    // Exit with error code if any service is unhealthy
    if (summary.unhealthy > 0 || summary.errors > 0) {
      console.log('\n⚠️  Some services are not healthy!');
      process.exit(1);
    }
    
    console.log('\n✅ All checked services are healthy!');
    process.exit(0);
    
  } catch (error) {
    console.error('❌ Fatal error during status check:', error);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { checkEndpoint, checkAllEndpoints, saveResults };
