const nodemailer = require('nodemailer');
const bcrypt = require('bcryptjs');
const crypto = require('crypto');
let sgMail;
try { sgMail = require('@sendgrid/mail'); } catch (e) { /* optional */ }
const { createClient } = require('@supabase/supabase-js');

const supabase = (process.env.SUPABASE_URL && process.env.SUPABASE_SERVICE_ROLE_KEY)
  ? createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY)
  : null;

exports.handler = async function (event, context) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const body = JSON.parse(event.body || '{}');
    const { name, email, phone, password } = body;

    if (!email || !email.endsWith('@gmail.com')) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Se requiere un correo Gmail válido.' }) };
    }
    if (!phone) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Se requiere un número de teléfono.' }) };
    }
    if (!password || password.length < 6) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Contraseña mínima 6 caracteres.' }) };
    }

    // If Supabase configured, create user record
    let verificationToken = null;
    if (supabase) {
      // check existing
      const { data: existing, error: selErr } = await supabase.from('users').select('id,verified').eq('email', email).limit(1);
      if (selErr) console.warn('supabase select error', selErr.message || selErr);
      if (existing && existing.length) {
        return { statusCode: 400, body: JSON.stringify({ error: 'Ya existe una cuenta con ese correo.' }) };
      }

      const passwordHash = await bcrypt.hash(password, 10);
      verificationToken = crypto.randomBytes(24).toString('hex');

      const { data: insertData, error: insertErr } = await supabase.from('users').insert([{
        name, email, phone, password_hash: passwordHash, verified: false, verification_token: verificationToken
      }]);

      if (insertErr) {
        console.error('supabase insert err', insertErr);
        return { statusCode: 500, body: JSON.stringify({ error: 'Error al crear usuario.' }) };
      }
    }

    const subject = `Registro PlayStore · ${name || email}`;
    const siteUrl = process.env.SITE_URL || process.env.NETLIFY_SITE_URL || 'https://your-site.netlify.app';
    const activatePath = `${siteUrl.replace(/\/$/, '')}/.netlify/functions/activate?token=${verificationToken || 'no-token'}`;
    const html = `
      <h2>Hola ${name || 'usuario'}</h2>
      <p>Gracias por registrarte en PlayStore. Tu correo: <strong>${email}</strong></p>
      <p>Teléfono: <strong>${phone}</strong></p>
      <p>Haz clic en el siguiente enlace para activar tu cuenta:</p>
      <p><a href="${activatePath}">Activar cuenta</a></p>
      <p>Si no solicitaste este correo, ignóralo.</p>
    `;

    // Prefer SendGrid if API key is provided
    if (process.env.SENDGRID_API_KEY && sgMail) {
      sgMail.setApiKey(process.env.SENDGRID_API_KEY);
      const msg = {
        to: email,
        from: process.env.EMAIL_FROM || process.env.SENDGRID_FROM || 'no-reply@playstore.example',
        subject,
        html,
      };
      await sgMail.send(msg);
    } else if (process.env.SMTP_HOST && process.env.SMTP_USER && process.env.SMTP_PASS) {
      const transporter = nodemailer.createTransport({
        host: process.env.SMTP_HOST,
        port: Number(process.env.SMTP_PORT) || 587,
        secure: process.env.SMTP_SECURE === 'true',
        auth: {
          user: process.env.SMTP_USER,
          pass: process.env.SMTP_PASS,
        },
      });

      await transporter.sendMail({
        from: process.env.EMAIL_FROM || process.env.SMTP_USER,
        to: email,
        subject,
        html,
      });
    } else {
      return { statusCode: 500, body: JSON.stringify({ error: 'No email transport configured. Set SENDGRID_API_KEY or SMTP_* env vars.' }) };
    }

    return { statusCode: 200, body: JSON.stringify({ ok: true, message: 'Email de verificación enviado' }) };
  } catch (err) {
    console.error('register error', err);
    return { statusCode: 500, body: JSON.stringify({ error: err.message || 'Internal error' }) };
  }
};
