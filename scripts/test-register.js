const fs = require('fs');
const path = require('path');

function loadEnv(filePath) {
  const p = path.resolve(__dirname, '..', filePath);
  if (!fs.existsSync(p)) {
    console.error('.env file not found at', p);
    process.exit(1);
  }
  const content = fs.readFileSync(p, 'utf8');
  content.split(/\r?\n/).forEach(line => {
    const l = line.trim();
    if (!l || l.startsWith('#')) return;
    const idx = l.indexOf('=');
    if (idx === -1) return;
    const key = l.slice(0, idx);
    const val = l.slice(idx + 1);
    process.env[key] = val;
  });
}

(async function () {
  loadEnv('.env');

  // require the register function
  const registerPath = path.resolve(__dirname, '..', 'netlify', 'functions', 'register.js');
  if (!fs.existsSync(registerPath)) {
    console.error('register function not found at', registerPath);
    process.exit(1);
  }

  const register = require(registerPath);

  const recipient = process.env.TEST_RECIPIENT || process.env.SMTP_USER;
  const event = {
    httpMethod: 'POST',
    body: JSON.stringify({ name: 'Prueba Local', email: recipient, phone: '+15551234567', password: 'test12345' })
  };

  try {
    const res = await register.handler(event, {});
    console.log('Handler returned:', res && typeof res === 'object' ? res.statusCode : res);
    try {
      console.log('Body:', JSON.parse(res.body || '{}'));
    } catch (e) {
      console.log('Body (raw):', res.body);
    }
    process.exit(0);
  } catch (err) {
    console.error('Error invoking register.handler:', err);
    process.exit(1);
  }
})();
