// Vercel Serverless Function - Proxy para Render Backend
// Este arquivo cria um proxy para TODAS as rotas /api/*

export const config = {
  runtime: 'edge',
};

export default async function handler(request: Request) {
  const url = new URL(request.url);
  
  // Pegar o caminho após /api
  const path = url.pathname;
  
  // URL do backend (Render)
  const backendUrl = process.env.PY_EXTERNAL || 'https://advisior-cursor.onrender.com';
  
  // Construir URL completa do backend
  const targetUrl = `${backendUrl}${path}${url.search}`;
  
  console.log(`[Proxy] ${request.method} ${path} → ${targetUrl}`);
  
  // Headers para enviar
  const headers = new Headers(request.headers);
  headers.set('host', new URL(backendUrl).host);
  
  try {
    // Fazer request para o backend
    const response = await fetch(targetUrl, {
      method: request.method,
      headers,
      body: request.body,
      // @ts-ignore
      duplex: 'half',
    });
    
    // Retornar resposta do backend
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: response.headers,
    });
  } catch (error) {
    console.error('[Proxy Error]', error);
    return new Response(
      JSON.stringify({ 
        error: 'Erro ao conectar com backend',
        message: error instanceof Error ? error.message : 'Unknown error',
      }),
      {
        status: 502,
        headers: { 'Content-Type': 'application/json' },
      }
    );
  }
}

