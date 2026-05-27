const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
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
    const { email, password } = body;
    if (!email || !password) return { statusCode: 400, body: JSON.stringify({ error: 'Email y contraseña requeridos.' }) };

    if (!supabase) return { statusCode: 500, body: JSON.stringify({ error: 'No hay configuración de base de datos.' }) };

    const { data, error } = await supabase.from('users').select('id,name,email,password_hash,verified').eq('email', email).limit(1);
    if (error) {
      console.error('supabase select err', error);
      return { statusCode: 500, body: JSON.stringify({ error: 'Error al autenticar.' }) };
    }
    if (!data || !data.length) return { statusCode: 401, body: JSON.stringify({ error: 'Credenciales inválidas.' }) };

    const user = data[0];
    if (!user.verified) return { statusCode: 403, body: JSON.stringify({ error: 'Cuenta no verificada.' }) };

    const ok = await bcrypt.compare(password, user.password_hash || '');
    if (!ok) return { statusCode: 401, body: JSON.stringify({ error: 'Credenciales inválidas.' }) };

    const jwtSecret = process.env.JWT_SECRET || 'change-me';
    const token = jwt.sign({ sub: user.id, email: user.email }, jwtSecret, { expiresIn: '7d' });

    return { statusCode: 200, body: JSON.stringify({ ok: true, token, user: { id: user.id, name: user.name, email: user.email } }) };
  } catch (err) {
    console.error('login error', err);
    return { statusCode: 500, body: JSON.stringify({ error: 'Internal error' }) };
  }
};
