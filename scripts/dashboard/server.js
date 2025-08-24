#!/usr/bin/env node

/**
 * Simple HTTP server to serve the Agent Performance Dashboard
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

class DashboardServer {
  constructor(port = 3000) {
    this.port = port;
    this.dashboardPath = __dirname;
    this.dataPath = path.join(__dirname, '../data');
  }

  getMimeType(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    const mimeTypes = {
      '.html': 'text/html',
      '.css': 'text/css',
      '.js': 'application/javascript',
      '.json': 'application/json',
      '.png': 'image/png',
      '.jpg': 'image/jpeg',
      '.ico': 'image/x-icon'
    };
    return mimeTypes[ext] || 'text/plain';
  }

  handleRequest(req, res) {
    const parsedUrl = url.parse(req.url, true);
    let filePath = parsedUrl.pathname;

    // Handle root request
    if (filePath === '/') {
      filePath = '/index.html';
    }

    // Handle data requests
    if (filePath.startsWith('/data/')) {
      const dataFile = path.join(this.dataPath, filePath.replace('/data/', ''));
      this.serveFile(dataFile, res);
      return;
    }

    // Handle static files
    const fullPath = path.join(this.dashboardPath, filePath);
    this.serveFile(fullPath, res);
  }

  serveFile(filePath, res) {
    fs.readFile(filePath, (err, content) => {
      if (err) {
        if (err.code === 'ENOENT') {
          res.writeHead(404, { 'Content-Type': 'text/plain' });
          res.end('File not found');
        } else {
          res.writeHead(500, { 'Content-Type': 'text/plain' });
          res.end('Server error');
        }
        return;
      }

      const mimeType = this.getMimeType(filePath);
      res.writeHead(200, { 
        'Content-Type': mimeType,
        'Access-Control-Allow-Origin': '*'
      });
      res.end(content);
    });
  }

  start() {
    const server = http.createServer((req, res) => {
      this.handleRequest(req, res);
    });

    server.listen(this.port, () => {
      console.log(`🚀 Agent Performance Dashboard server running at:`);
      console.log(`   http://localhost:${this.port}`);
      console.log('');
      console.log('📊 Dashboard Features:');
      console.log('   • Agent activity timeline');
      console.log('   • Task completion rate metrics');
      console.log('   • Performance graphs over time');
      console.log('   • Export functionality for reports');
      console.log('');
      console.log('Press Ctrl+C to stop the server');
    });

    // Graceful shutdown
    process.on('SIGINT', () => {
      console.log('\n🛑 Shutting down dashboard server...');
      server.close(() => {
        console.log('✅ Server closed successfully');
        process.exit(0);
      });
    });
  }
}

// CLI usage
if (require.main === module) {
  const port = process.argv[2] ? parseInt(process.argv[2]) : 3000;
  
  if (isNaN(port) || port < 1 || port > 65535) {
    console.error('❌ Invalid port number. Using default port 3000.');
    new DashboardServer().start();
  } else {
    new DashboardServer(port).start();
  }
}

module.exports = DashboardServer;