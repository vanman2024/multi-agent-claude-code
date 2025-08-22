// Health check endpoint
function getHealth() {
  return {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    version: '1.0.1' // Updated version
  };
}

module.exports = { getHealth };