// Vercel Serverless Function - Proxy para Render Backend
import type { VercelRequest, VercelResponse } from '@vercel/node';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  // URL do backend (Render)
  const backendUrl = process.env.PY_EXTERNAL || 'https://advisior-cursor.onrender.com';
  
  // Pegar o caminho completo incluindo /api
  const path = req.url || '/';
  
  // Construir URL completa do backend
  const targetUrl = `${backendUrl}${path}`;
  
  console.log(`[Proxy] ${req.method} ${path} → ${targetUrl}`);
  
  try {
    // Headers para enviar ao backend
    const headers: Record<string, string> = {
      'Content-Type': req.headers['content-type'] || 'application/json',
    };
    
    // Configuração do fetch
    const fetchOptions: RequestInit = {
      method: req.method,
      headers,
    };
    
    // Adicionar body para POST/PUT/PATCH
    if (req.method && ['POST', 'PUT', 'PATCH'].includes(req.method) && req.body) {
      fetchOptions.body = JSON.stringify(req.body);
    }
    
    // Fazer request para o backend
    const response = await fetch(targetUrl, fetchOptions);
    
    // Pegar resposta
    const data = await response.text();
    
    // Retornar com mesmo status code e content-type
    res.status(response.status);
    res.setHeader('Content-Type', response.headers.get('content-type') || 'application/json');
    
    // Tentar parsear como JSON, senão retornar texto
    try {
      const json = JSON.parse(data);
      return res.json(json);
    } catch {
      return res.send(data);
    }
    
  } catch (error) {
    console.error('[Proxy Error]', error);
    return res.status(502).json({ 
      error: 'Erro ao conectar com backend',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
}

