import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';
import http from 'http';
import { createServer as createViteServer } from 'vite';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PORT = 3000;
const PYTHON_PORT = 5000;

// Start Python HTMX Backend Process
console.log('Launching Python HTMX Backend (app.py)...');
const pythonProc = spawn('python3', ['app.py'], {
  cwd: process.cwd(),
  stdio: 'inherit',
});

pythonProc.on('error', (err) => {
  console.error('Failed to start Python process:', err);
});

async function startServer() {
  const app = express();

  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  // Proxy /api/htmx and /api endpoints to Python HTMX Backend on Port 5000
  app.all('/api/*', (req, res) => {
    const options: http.RequestOptions = {
      hostname: '127.0.0.1',
      port: PYTHON_PORT,
      path: req.originalUrl,
      method: req.method,
      headers: {
        ...req.headers,
        host: `127.0.0.1:${PYTHON_PORT}`,
      },
    };

    const proxyReq = http.request(options, (proxyRes) => {
      res.writeHead(proxyRes.statusCode || 200, proxyRes.headers);
      proxyRes.pipe(res, { end: true });
    });

    proxyReq.on('error', (err) => {
      console.error('Proxy connection error to Python server:', err.message);
      res.status(502).send('<div class="p-4 text-red-400 bg-red-950/30 border border-red-500/30 rounded-xl">Python HTMX backend is connecting... Please retry.</div>');
    });

    if (req.body && Object.keys(req.body).length > 0) {
      if (req.headers['content-type']?.includes('application/x-www-form-urlencoded')) {
        const bodyData = new URLSearchParams(req.body).toString();
        proxyReq.write(bodyData);
      } else if (req.headers['content-type']?.includes('application/json')) {
        proxyReq.write(JSON.stringify(req.body));
      }
    }

    proxyReq.end();
  });

  // Vite Middleware in Dev Mode or Static Files in Production
  if (process.env.NODE_ENV !== 'production') {
    console.log('Integrating Vite Development Middleware...');
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`Express Proxy and Application Server running on http://0.0.0.0:${PORT}`);
  });
}

startServer();

// Clean up Python process on termination
process.on('SIGINT', () => {
  pythonProc.kill();
  process.exit();
});
process.on('SIGTERM', () => {
  pythonProc.kill();
  process.exit();
});
