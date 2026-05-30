/**
 * Netlify Function: Proxy de imágenes
 * Evita CORS bloqueando por Cloudflare
 * 
 * Uso: /.netlify/functions/proxy-image?url=ENCODED_URL
 */

const https = require('https');
const http = require('http');

export const handler = async (event) => {
  try {
    // Obtener URL de la imagen
    const imageUrl = event.queryStringParameters?.url;
    
    if (!imageUrl) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'Missing url parameter' })
      };
    }

    // Decodificar URL
    let url;
    try {
      url = decodeURIComponent(imageUrl);
    } catch (e) {
      url = imageUrl;
    }

    // Validar que sea URL válida
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'Invalid URL' })
      };
    }

    // Hacer request a la imagen
    const imageBuffer = await fetchImage(url);

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'image/jpeg',
        'Cache-Control': 'public, max-age=31536000', // cachea 1 año
        'Access-Control-Allow-Origin': '*'
      },
      body: imageBuffer.toString('base64'),
      isBase64Encoded: true
    };
  } catch (error) {
    console.error('Proxy error:', error.message);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};

/**
 * Fetch imagen desde URL
 */
function fetchImage(url) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    
    const options = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      },
      timeout: 10000
    };

    protocol.get(url, options, (response) => {
      // Seguir redirects
      if (response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
        return fetchImage(response.headers.location).then(resolve).catch(reject);
      }

      if (response.statusCode !== 200) {
        reject(new Error(`HTTP ${response.statusCode}`));
        return;
      }

      const chunks = [];
      response.on('data', chunk => chunks.push(chunk));
      response.on('end', () => resolve(Buffer.concat(chunks)));
      response.on('error', reject);
    }).on('error', reject);
  });
}
