import { NextApiRequest, NextApiResponse } from 'next';
import handler from '../../src/pages/api/health';
import { createMocks } from 'node-mocks-http';

describe('/api/health', () => {
  it('should return health status with correct structure', async () => {
    const { req, res } = createMocks<NextApiRequest, NextApiResponse>({
      method: 'GET',
    });

    await handler(req, res);

    expect(res._getStatusCode()).toBe(200);
    
    const data = JSON.parse(res._getData());
    expect(data).toHaveProperty('status');
    expect(data).toHaveProperty('timestamp');
    expect(data).toHaveProperty('environment');
    expect(data).toHaveProperty('version');
    
    expect(data.status).toBe('healthy');
    expect(data.version).toBe('1.0.0');
    expect(typeof data.timestamp).toBe('string');
    expect(typeof data.environment).toBe('string');
  });

  it('should return valid ISO timestamp', async () => {
    const { req, res } = createMocks<NextApiRequest, NextApiResponse>({
      method: 'GET',
    });

    await handler(req, res);
    
    const data = JSON.parse(res._getData());
    const timestamp = new Date(data.timestamp);
    
    expect(timestamp instanceof Date).toBe(true);
    expect(timestamp.toISOString()).toBe(data.timestamp);
  });

  it('should return environment from NODE_ENV or default to development', () => {
    const originalEnv = process.env.NODE_ENV;
    
    // Test with NODE_ENV set
    (process.env as any).NODE_ENV = 'production';
    const { req: req1, res: res1 } = createMocks<NextApiRequest, NextApiResponse>({
      method: 'GET',
    });
    
    handler(req1, res1);
    const data1 = JSON.parse(res1._getData());
    expect(data1.environment).toBe('production');

    // Test without NODE_ENV
    (process.env as any).NODE_ENV = '';
    const { req: req2, res: res2 } = createMocks<NextApiRequest, NextApiResponse>({
      method: 'GET',
    });
    
    handler(req2, res2);
    const data2 = JSON.parse(res2._getData());
    expect(data2.environment).toBe('development');
    
    // Restore original environment
    (process.env as any).NODE_ENV = originalEnv;
  });

  it('should handle POST method (should work same as GET)', () => {
    const { req, res } = createMocks<NextApiRequest, NextApiResponse>({
      method: 'POST',
    });

    handler(req, res);

    expect(res._getStatusCode()).toBe(200);
    const data = JSON.parse(res._getData());
    expect(data.status).toBe('healthy');
  });

  it('should handle PUT method (should work same as GET)', () => {
    const { req, res } = createMocks<NextApiRequest, NextApiResponse>({
      method: 'PUT',
    });

    handler(req, res);

    expect(res._getStatusCode()).toBe(200);
    const data = JSON.parse(res._getData());
    expect(data.status).toBe('healthy');
  });

  it('should return response within reasonable time', () => {
    const start = Date.now();
    
    const { req, res } = createMocks<NextApiRequest, NextApiResponse>({
      method: 'GET',
    });

    handler(req, res);
    
    const duration = Date.now() - start;
    expect(duration).toBeLessThan(100); // Should respond within 100ms
  });

  it('should return timestamp close to current time', () => {
    const beforeCall = Date.now();
    
    const { req, res } = createMocks<NextApiRequest, NextApiResponse>({
      method: 'GET',
    });

    handler(req, res);
    
    const afterCall = Date.now();
    const data = JSON.parse(res._getData());
    const responseTime = new Date(data.timestamp).getTime();
    
    expect(responseTime).toBeGreaterThanOrEqual(beforeCall);
    expect(responseTime).toBeLessThanOrEqual(afterCall);
  });
});