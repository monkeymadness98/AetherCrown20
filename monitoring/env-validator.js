#!/usr/bin/env node

/**
 * Environment Variables Validation Script
 * 
 * Validates that all required environment variables are set across different platforms.
 * Use this to verify your deployment configuration before pushing to production.
 */

const fs = require('fs');
const path = require('path');

// Define all required environment variables
const REQUIRED_VARS = {
  // OpenAI
  openai: [
    { name: 'OPENAI_API_KEY', platforms: ['GitHub Secrets', 'Render', 'Vercel'] }
  ],
  
  // Supabase
  supabase: [
    { name: 'SUPABASE_URL', platforms: ['GitHub Secrets', 'Render', 'Vercel', 'Supabase Edge'] },
    { name: 'SUPABASE_ANON_KEY', platforms: ['GitHub Secrets', 'Render', 'Vercel'] },
    { name: 'SUPABASE_SERVICE_ROLE_KEY', platforms: ['GitHub Secrets', 'Render', 'Supabase Edge'] },
    { name: 'NEXT_PUBLIC_SUPABASE_URL', platforms: ['Vercel'] },
    { name: 'NEXT_PUBLIC_SUPABASE_ANON_KEY', platforms: ['Vercel'] }
  ],
  
  // Database
  database: [
    { name: 'DATABASE_URL', platforms: ['GitHub Secrets', 'Render', 'Supabase'] }
  ],
  
  // PayPal
  paypal: [
    { name: 'PAYPAL_CLIENT_ID', platforms: ['GitHub Secrets', 'Render', 'Vercel'] },
    { name: 'PAYPAL_SECRET', platforms: ['GitHub Secrets', 'Render'] }
  ],
  
  // Render
  render: [
    { name: 'RENDER_API_KEY', platforms: ['GitHub Secrets'] },
    { name: 'RENDER_SERVICE_ID', platforms: ['GitHub Secrets'] }
  ],
  
  // Vercel
  vercel: [
    { name: 'VERCEL_TOKEN', platforms: ['GitHub Secrets'] },
    { name: 'VERCEL_PROJECT_ID', platforms: ['GitHub Secrets'] },
    { name: 'VERCEL_ORG_ID', platforms: ['GitHub Secrets'] },
    { name: 'VERCEL_ENV', platforms: ['Vercel'] }
  ],
  
  // Frontend/API
  frontend: [
    { name: 'NEXT_PUBLIC_API_URL', platforms: ['Vercel'] }
  ]
};

// Optional but recommended variables
const OPTIONAL_VARS = [
  { name: 'REDIS_URL', platforms: ['Render'], purpose: 'Caching and sessions' },
  { name: 'SECRET_KEY', platforms: ['Render', 'Vercel'], purpose: 'JWT and session encryption' },
  { name: 'ENV', platforms: ['All'], purpose: 'Environment identifier (development/production)' },
  { name: 'LOG_LEVEL', platforms: ['Render'], purpose: 'Logging verbosity' },
  { name: 'CORS_ORIGINS', platforms: ['Render'], purpose: 'Cross-origin resource sharing' }
];

/**
 * Check if variable exists in current environment
 */
function checkLocalEnv(varName) {
  return {
    name: varName,
    exists: !!process.env[varName],
    value: process.env[varName] ? '***SET***' : 'NOT SET'
  };
}

/**
 * Print validation report
 */
function printReport() {
  console.log('='.repeat(80));
  console.log('🔐 AETHER EMPIRE - ENVIRONMENT VARIABLES VALIDATION');
  console.log('='.repeat(80));
  console.log('');
  
  console.log('📋 REQUIRED VARIABLES BY CATEGORY');
  console.log('-'.repeat(80));
  
  let totalRequired = 0;
  let localSet = 0;
  
  for (const [category, vars] of Object.entries(REQUIRED_VARS)) {
    console.log(`\n${category.toUpperCase()}:`);
    
    vars.forEach(varInfo => {
      totalRequired++;
      const status = checkLocalEnv(varInfo.name);
      
      if (status.exists) localSet++;
      
      const icon = status.exists ? '✅' : '❌';
      console.log(`  ${icon} ${varInfo.name}`);
      console.log(`     Platforms: ${varInfo.platforms.join(', ')}`);
      console.log(`     Local Status: ${status.value}`);
    });
  }
  
  console.log('\n' + '-'.repeat(80));
  console.log(`📊 Summary: ${localSet}/${totalRequired} required variables set locally`);
  
  console.log('\n' + '='.repeat(80));
  console.log('🔧 OPTIONAL VARIABLES');
  console.log('-'.repeat(80));
  
  let optionalSet = 0;
  OPTIONAL_VARS.forEach(varInfo => {
    const status = checkLocalEnv(varInfo.name);
    if (status.exists) optionalSet++;
    
    const icon = status.exists ? '✅' : '⚪';
    console.log(`  ${icon} ${varInfo.name}`);
    console.log(`     Purpose: ${varInfo.purpose}`);
    console.log(`     Platforms: ${varInfo.platforms.join(', ')}`);
    console.log(`     Status: ${status.value}`);
  });
  
  console.log('\n' + '-'.repeat(80));
  console.log(`📊 Optional: ${optionalSet}/${OPTIONAL_VARS.length} variables set`);
  
  console.log('\n' + '='.repeat(80));
  console.log('📝 PLATFORM CHECKLIST');
  console.log('-'.repeat(80));
  
  console.log('\n1. GitHub Secrets (https://github.com/monkeymadness98/AetherCrown20/settings/secrets/actions)');
  console.log('   Required: OPENAI_API_KEY, SUPABASE_*, DATABASE_URL, PAYPAL_*, RENDER_*, VERCEL_*');
  
  console.log('\n2. Render Environment (https://dashboard.render.com/)');
  console.log('   Required: OPENAI_API_KEY, SUPABASE_*, DATABASE_URL, PAYPAL_*');
  console.log('   Optional: REDIS_URL, SECRET_KEY, ENV, LOG_LEVEL, CORS_ORIGINS');
  
  console.log('\n3. Vercel Environment (https://vercel.com/dashboard)');
  console.log('   Required: OPENAI_API_KEY, SUPABASE_*, PAYPAL_CLIENT_ID, NEXT_PUBLIC_*');
  console.log('   Optional: SECRET_KEY, VERCEL_ENV');
  
  console.log('\n4. Supabase Edge Functions (https://app.supabase.com/)');
  console.log('   Required: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, DATABASE_URL');
  
  console.log('\n' + '='.repeat(80));
  console.log('💡 NEXT STEPS');
  console.log('-'.repeat(80));
  
  if (localSet < totalRequired) {
    console.log('\n⚠️  Missing variables detected in local environment!');
    console.log('   1. Copy .env.template to .env: cp .env.template .env');
    console.log('   2. Fill in all required values in .env');
    console.log('   3. Run this script again to verify');
  } else {
    console.log('\n✅ All required variables are set locally!');
  }
  
  console.log('\n📌 Platform Setup:');
  console.log('   1. Add secrets to GitHub: Settings → Secrets and variables → Actions');
  console.log('   2. Configure Render: Dashboard → Service → Environment');
  console.log('   3. Configure Vercel: Project Settings → Environment Variables');
  console.log('   4. Configure Supabase: Project → Edge Functions → Secrets');
  
  console.log('\n🔍 Verification:');
  console.log('   • GitHub: Workflows will fail if secrets are missing');
  console.log('   • Render: Check /healthz and /_env_check endpoints');
  console.log('   • Vercel: Check deployment logs for env var errors');
  console.log('   • Supabase: Check edge function logs');
  
  console.log('\n' + '='.repeat(80));
  console.log('');
}

/**
 * Generate a checklist file
 */
function generateChecklist() {
  const checklistPath = path.join(__dirname, '..', 'ENV_CHECKLIST.md');
  
  let content = '# Environment Variables Checklist\n\n';
  content += 'Use this checklist to ensure all environment variables are configured across all platforms.\n\n';
  content += '## Platform Setup Status\n\n';
  content += '- [ ] GitHub Secrets configured\n';
  content += '- [ ] Render Environment configured\n';
  content += '- [ ] Vercel Environment configured\n';
  content += '- [ ] Supabase Edge Function secrets configured\n\n';
  
  content += '## Required Variables by Platform\n\n';
  
  // Group by platform
  const platformVars = {
    'GitHub Secrets': [],
    'Render': [],
    'Vercel': [],
    'Supabase Edge': []
  };
  
  for (const vars of Object.values(REQUIRED_VARS)) {
    vars.forEach(varInfo => {
      varInfo.platforms.forEach(platform => {
        if (platformVars[platform]) {
          if (!platformVars[platform].includes(varInfo.name)) {
            platformVars[platform].push(varInfo.name);
          }
        }
      });
    });
  }
  
  for (const [platform, vars] of Object.entries(platformVars)) {
    content += `### ${platform}\n\n`;
    vars.sort().forEach(varName => {
      content += `- [ ] ${varName}\n`;
    });
    content += '\n';
  }
  
  content += '## Optional Variables\n\n';
  OPTIONAL_VARS.forEach(varInfo => {
    content += `- [ ] ${varInfo.name} (${varInfo.purpose})\n`;
  });
  
  content += '\n## Verification Steps\n\n';
  content += '1. **Local Development**: Run `node monitoring/env-validator.js`\n';
  content += '2. **Render**: Visit `https://aetherai-8wcw.onrender.com/_env_check`\n';
  content += '3. **GitHub Actions**: Check workflow runs for errors\n';
  content += '4. **Vercel**: Check deployment logs\n';
  content += '5. **Supabase**: Test edge function invocation\n';
  
  fs.writeFileSync(checklistPath, content);
  console.log(`📄 Checklist generated: ${checklistPath}`);
}

/**
 * Main execution
 */
function main() {
  // Check if .env file exists
  const envPath = path.join(__dirname, '..', '.env');
  if (!fs.existsSync(envPath)) {
    console.log('⚠️  No .env file found!');
    console.log('   Copy .env.template to .env and fill in your values.');
    console.log('   $ cp .env.template .env\n');
  }
  
  printReport();
  generateChecklist();
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { checkLocalEnv, REQUIRED_VARS, OPTIONAL_VARS };
