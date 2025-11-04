// API Configuration
// Em produção, chama Render direto (sem proxy Vercel)
// Em desenvolvimento, usa proxy local

export const API_BASE_URL = import.meta.env.PROD 
  ? 'https://advisior-cursor.onrender.com'
  : '';

export function getApiUrl(path: string): string {
  // Se já começa com http, retorna direto
  if (path.startsWith('http')) {
    return path;
  }
  
  // Em produção, adiciona base URL do Render
  if (import.meta.env.PROD) {
    return `${API_BASE_URL}${path}`;
  }
  
  // Em desenvolvimento, usa caminho relativo (proxy local)
  return path;
}

