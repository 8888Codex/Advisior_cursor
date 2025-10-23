import express, { type Request, Response, NextFunction } from "express";
import { createProxyMiddleware } from 'http-proxy-middleware';
import { spawn } from 'child_process';
import { registerRoutes } from "./routes";
import { setupVite, serveStatic, log } from "./vite";
import { seedExperts } from "./seed";

const app = express();

// Start Python backend automatically
function startPythonBackend() {
  log("Starting Python backend on port 5001...");
  const pythonProcess = spawn('python3', ['-m', 'uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '5001', '--reload'], {
    cwd: 'python_backend',
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

declare module 'http' {
  interface IncomingMessage {
    rawBody: unknown
  }
}
app.use(express.json({
  verify: (req, _res, buf) => {
    req.rawBody = buf;
  }
}));
app.use(express.urlencoded({ extended: false }));

app.use((req, res, next) => {
  const start = Date.now();
  const path = req.path;
  let capturedJsonResponse: Record<string, any> | undefined = undefined;

  const originalResJson = res.json;
  res.json = function (bodyJson, ...args) {
    capturedJsonResponse = bodyJson;
    return originalResJson.apply(res, [bodyJson, ...args]);
  };

  res.on("finish", () => {
    const duration = Date.now() - start;
    if (path.startsWith("/api")) {
      let logLine = `${req.method} ${path} ${res.statusCode} in ${duration}ms`;
      if (capturedJsonResponse) {
        logLine += ` :: ${JSON.stringify(capturedJsonResponse)}`;
      }

      if (logLine.length > 80) {
        logLine = logLine.slice(0, 79) + "…";
      }

      log(logLine);
    }
  });

  next();
});

(async () => {
  // Proxy all /api requests to Python backend on port 5001
  // Note: http-proxy-middleware automatically removes the /api prefix when proxying
  // We need to add it back with pathRewrite
  app.use('/api', createProxyMiddleware({
    target: 'http://localhost:5001/api',
    changeOrigin: true,
  }));
  
  await seedExperts();
  const server = await registerRoutes(app);

  app.use((err: any, _req: Request, res: Response, _next: NextFunction) => {
    const status = err.status || err.statusCode || 500;
    const message = err.message || "Internal Server Error";

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
  const port = parseInt(process.env.PORT || '5000', 10);
  server.listen({
    port,
    host: "0.0.0.0",
    reusePort: true,
  }, () => {
    log(`serving on port ${port}`);
  });
})();
