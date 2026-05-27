const { createClient } = require('@supabase/supabase-js');

const supabase = (process.env.SUPABASE_URL && process.env.SUPABASE_SERVICE_ROLE_KEY)
  ? createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY)
  : null;

exports.handler = async function (event, context) {
  try {
    const token = (event.httpMethod === 'GET') ? (event.queryStringParameters && event.queryStringParameters.token) : JSON.parse(event.body || '{}').token;
    if (!token) return { statusCode: 400, body: JSON.stringify({ error: 'Token requerido.' }) };

    if (!supabase) return { statusCode: 500, body: JSON.stringify({ error: 'No hay configuración de base de datos.' }) };

    const { data, error } = await supabase.from('users').select('id,verified').eq('verification_token', token).limit(1);
    if (error) {
      console.error('supabase select err', error);
      return { statusCode: 500, body: JSON.stringify({ error: 'Error al verificar token.' }) };
    }
    if (!data || !data.length) return { statusCode: 404, body: JSON.stringify({ error: 'Token inválido o expirado.' }) };

    const user = data[0];
    if (user.verified) {
      return { statusCode: 200, body: JSON.stringify({ ok: true, message: 'Cuenta ya verificada.' }) };
    }

    const { error: updErr } = await supabase.from('users').update({ verified: true, verification_token: null }).eq('id', user.id);
    if (updErr) {
      console.error('supabase update err', updErr);
      return { statusCode: 500, body: JSON.stringify({ error: 'No se pudo activar la cuenta.' }) };
    }

    // Optionally redirect to a success page
    const siteUrl = process.env.SITE_URL || process.env.NETLIFY_SITE_URL || '';
    const redirectTo = siteUrl ? `${siteUrl.replace(/\/$/, '')}/registro.html?activated=1` : null;
    if (redirectTo) {
      return { statusCode: 302, headers: { Location: redirectTo }, body: '' };
    }

    return { statusCode: 200, body: JSON.stringify({ ok: true, message: 'Cuenta activada' }) };
  } catch (err) {
    console.error('activate error', err);
    return { statusCode: 500, body: JSON.stringify({ error: 'Internal error' }) };
  }
};
