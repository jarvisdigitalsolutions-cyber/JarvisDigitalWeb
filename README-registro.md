Registro - despliegue rápido

Archivos añadidos:
- `netlify/functions/register.js` — función serverless para procesar registros y enviar email.
- `package.json` — dependencias necesarias (`@sendgrid/mail`, `nodemailer`).

Variables de entorno recomendadas (Netlify / Vercel):
- `SENDGRID_API_KEY` — opcional, si usas SendGrid.
- `SENDGRID_FROM` — dirección desde la que envía SendGrid (opcional).
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS` — si prefieres SMTP/Gmail.
- `EMAIL_FROM` — dirección "from" alternativa.

Variables adicionales para autenticación y persistencia (opcional, recomendado):
- `SUPABASE_URL` — URL de tu proyecto Supabase
- `SUPABASE_SERVICE_ROLE_KEY` — Service Role Key (server-side) de Supabase
- `JWT_SECRET` — secreto para firmar tokens JWT (cámbialo por una cadena segura)
- `SITE_URL` — URL pública de tu sitio (opcional, usada en enlaces de activación)

Endpoint de registro (Netlify):
POST /.netlify/functions/register

Ejemplo curl:
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"Juan","email":"juan@gmail.com","phone":"+15551234567"}' \
  https://<tu-sitio>.netlify.app/.netlify/functions/register
```

Notas:
- Si usas Vercel, coloca la función en `api/register.js` y ajusta la URL a `/api/register`.
- No subas credenciales en el frontend; configura las variables en el panel de Netlify/Vercel.

Base de datos (Supabase)
------------------------
Si quieres persistir usuarios y soportar login, crea una tabla `users` en Supabase con esta estructura mínima (SQL):

```sql
create table public.users (
  id uuid default uuid_generate_v4() primary key,
  name text,
  email text unique not null,
  phone text,
  password_hash text,
  verified boolean default false,
  verification_token text,
  created_at timestamptz default now()
);
```

Usa `SUPABASE_URL` y `SUPABASE_SERVICE_ROLE_KEY` en Netlify para que las funciones puedan insertar/leer usuarios.

Flujo recomendado
------------------
1. El usuario envía el formulario en `registro.html` (name,email,phone,password).
2. `/.netlify/functions/register` crea el usuario (Supabase) y envía un email de verificación con un enlace.
3. El usuario hace clic en el enlace → `/.netlify/functions/activate?token=...` marca la cuenta como verificada.
4. `/.netlify/functions/login` permite iniciar sesión y devuelve un JWT.

