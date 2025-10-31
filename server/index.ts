import express, { type Request, Response, NextFunction } from "express";
import { createProxyMiddleware } from 'http-proxy-middleware';
import { spawn } from 'child_process';
import path from 'path';
import { registerRoutes } from "./routes";
import { setupVite, serveStatic, log } from "./vite";
import { seedExperts } from "./seed";

const app = express();

// Start Python backend automatically (disabled if PY_EXTERNAL is provided)
function startPythonBackend() {
  if (process.env.PY_EXTERNAL) {
    log(`Skipping local Python spawn. Using external backend at ${process.env.PY_EXTERNAL}`);
    return undefined;
  }
  const PY_PORT = parseInt(process.env.PY_PORT || '5100', 10);
  log(`Starting Python backend on port ${PY_PORT}...`);
  const pythonHost = process.platform === 'darwin' ? '127.0.0.1' : '0.0.0.0';
  const pythonProcess = spawn('python3', ['-m', 'uvicorn', 'python_backend.main:app', '--host', pythonHost, '--port', String(PY_PORT), '--reload'], {
    cwd: '.',
    stdio: ['ignore', 'pipe', 'pipe']
  });
  
  pythonProcess.stdout.on('data', (data) => {
    log(`[Python Backend] ${data.toString().trim()}`);
  });
  
  pythonProcess.stderr.on('data', (data) => {
    log(`[Python Backend Error] ${data.toString().trim()}`);
  });
  
  pythonProcess.on('error', (error) => {
    log(`[Python Backend] Failed to start: ${error.message}`);
  });
  
  pythonProcess.on('exit', (code) => {
    if (code !== null && code !== 0) {
      log(`[Python Backend] Exited with code ${code}`);
    }
  });
  
  return pythonProcess;
}

const pythonBackend = startPythonBackend();

// Proxy all /api requests to Python backend BEFORE any other middleware
// This ensures the request body is not consumed by express.json()
const PY_PORT = parseInt(process.env.PY_PORT || '5100', 10);
const PY_TARGET = process.env.PY_EXTERNAL || `http://localhost:${PY_PORT}`;
app.use('/api', createProxyMiddleware({
  target: PY_TARGET,
  changeOrigin: true,
  followRedirects: true,
  pathRewrite: function (path) {
    // http-proxy-middleware removes the mount path (/api) by default
    // We need to add it back since Python backend expects /api/...
    return '/api' + path;
  },
  // Cast para permitir handler específico sem quebrar tipos em versões diferentes
  ...( {
    onProxyReq: (proxyReq: any, req: any) => {
      // Ensure trailing slash for FastAPI compatibility on POST to conversations
      const currentPath = (proxyReq as any).path as string;
      if (req.method === 'POST' && currentPath === '/api/conversations') {
        (proxyReq as any).path = '/api/conversations/';
      }
    },
  } as any),
}));

declare module 'http' {
  interface IncomingMessage {
    rawBody: unknown
  }
}
app.use(express.json({
  verify: (req, _res, buf) => {
    (req as any).rawBody = buf;
  }
}));
app.use(express.urlencoded({ extended: false }));

// Middleware para logging estruturado de requisições /api
app.use((req, res, next) => {
  const start = Date.now();
  const path = req.path;
  const requestId = `req-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  (req as any).requestId = requestId;

  res.on("finish", () => {
    const duration = Date.now() - start;
    if (path.startsWith("/api")) {
      const status = res.statusCode;
      const isError = status >= 400;
      const isSlow = duration > 1000;
      
      let logLine = `${req.method} ${path} ${status} in ${duration}ms`;
      
      // Adicionar indicadores visuais para erros e requisições lentas
      if (isError) {
        logLine = `⚠️  ${logLine}`;
      } else if (isSlow) {
        logLine = `🐌 ${logLine}`;
      }
      
      // Para erros 5xx, logar JSON estruturado com request-id
      if (status >= 500) {
        const logData = {
          requestId,
          method: req.method,
          path,
          status,
          duration,
          timestamp: new Date().toISOString(),
        };
        console.error(`[ERROR] ${JSON.stringify(logData)}`);
      } else if (isError || isSlow) {
        // Para outros erros ou requisições lentas, logar linha formatada
        if (logLine.length > 100) {
          logLine = logLine.slice(0, 99) + "…";
        }
        log(logLine);
      } else {
        // Log normal truncado para requisições OK
        if (logLine.length > 80) {
          logLine = logLine.slice(0, 79) + "…";
        }
        log(logLine);
      }
    }
  });

  next();
});

(async () => {
  await seedExperts();
  
  // Serve avatar images and other attached assets
  // This must be before setupVite to avoid Vite intercepting the routes
  app.use('/attached_assets', express.static(path.resolve(process.cwd(), 'attached_assets')));
  
  const server = await registerRoutes(app);

  app.use((err: any, _req: Request, res: Response, _next: NextFunction) => {
    const status = (err as any).status || (err as any).statusCode || 500;
    const message = (err as any).message || "Internal Server Error";

    res.status(status).json({ message });
    throw err;
  });

  // importantly only setup vite in development and after
  // setting up all the other routes so the catch-all route
  // doesn't interfere with the other routes
  if (app.get("env") === "development") {
    await setupVite(app, server);
  } else {
    serveStatic(app);
  }

  // ALWAYS serve the app on the port specified in the environment variable PORT
  // Other ports are firewalled. Default to 5000 if not specified.
  // this serves both the API and the client.
  // It is the only port that is not firewalled.
  const port = parseInt(process.env.PORT || '3000', 10);
  const host = '0.0.0.0';
  server.listen(port, host, () => {
    log(`serving on port ${port} (host: ${host}) with PY_TARGET=${PY_TARGET}`);
  });
})();
