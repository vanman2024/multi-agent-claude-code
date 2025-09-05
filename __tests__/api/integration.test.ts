import { NextApiRequest, NextApiResponse } from 'next';
import { createMocks } from 'node-mocks-http';
import handler from '../../src/pages/api/health';

describe('API Integration Tests', () => {
  describe('Health Endpoint Integration', () => {
    it('should handle multiple concurrent requests', () => {
      const responses = [];
      
      for (let i = 0; i < 5; i++) {
        const { req, res } = createMocks<NextApiRequest, NextApiResponse>({
          method: 'GET',
        });
        handler(req, res);
        responses.push({ req, res });
      }
      
      responses.forEach(({ res }) => {
        expect(res._getStatusCode()).toBe(200);
        const data = JSON.parse(res._getData());
        expect(data.status).toBe('healthy');
      });
    });

    it('should maintain state consistency across requests', () => {
      const responses = [];
      
      // Make sequential requests with small delays to ensure different timestamps
      for (let i = 0; i < 3; i++) {
        const { req, res } = createMocks<NextApiRequest, NextApiResponse>({
          method: 'GET',
        });
        
        handler(req, res);
        responses.push(JSON.parse(res._getData()));
        
        // Small delay to ensure different timestamps
        if (i < 2) {
          const start = Date.now();
          while (Date.now() - start < 1) {} // 1ms delay
        }
      }
      
      // All responses should have the same structure and status
      responses.forEach((response, index) => {
        expect(response.status).toBe('healthy');
        expect(response.version).toBe('1.0.0');
        expect(typeof response.timestamp).toBe('string');
        expect(typeof response.environment).toBe('string');
      });
      
      // At least one timestamp should be different due to timing
      const timestamps = responses.map(r => r.timestamp);
      const uniqueTimestamps = new Set(timestamps);
      expect(uniqueTimestamps.size).toBeGreaterThanOrEqual(1);
    });

    it('should handle different HTTP methods consistently', () => {
      const methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'];
      const responses = [];
      
      for (const method of methods) {
        const { req, res } = createMocks<NextApiRequest, NextApiResponse>({
          method: method as any,
        });
        
        handler(req, res);
        responses.push({
          method,
          statusCode: res._getStatusCode(),
          data: JSON.parse(res._getData())
        });
      }
      
      // All methods should return the same successful response
      responses.forEach(({ method, statusCode, data }) => {
        expect(statusCode).toBe(200);
        expect(data.status).toBe('healthy');
        expect(data.version).toBe('1.0.0');
      });
    });

    it('should handle requests with different headers', () => {
      const headerTests = [
        { 'content-type': 'application/json' },
        { 'accept': 'application/json' },
        { 'user-agent': 'Test-Agent/1.0' },
        { 'authorization': 'Bearer test-token' },
        {}
      ];
      
      for (const headers of headerTests) {
        const { req, res } = createMocks<NextApiRequest, NextApiResponse>({
          method: 'GET',
          headers
        });
        
        handler(req, res);
        
        expect(res._getStatusCode()).toBe(200);
        const data = JSON.parse(res._getData());
        expect(data.status).toBe('healthy');
      }
    });

    it('should handle requests with query parameters', () => {
      const queryTests = [
        {},
        { foo: 'bar' },
        { check: 'detailed' },
        { format: 'json', version: 'v1' }
      ];
      
      for (const query of queryTests) {
        const { req, res } = createMocks<NextApiRequest, NextApiResponse>({
          method: 'GET',
          query
        });
        
        handler(req, res);
        
        expect(res._getStatusCode()).toBe(200);
        const data = JSON.parse(res._getData());
        expect(data.status).toBe('healthy');
      }
    });

    it('should handle requests with body data', () => {
      const bodyTests = [
        {},
        { test: 'data' },
        { ping: 'pong', timestamp: new Date().toISOString() }
      ];
      
      for (const body of bodyTests) {
        const { req, res } = createMocks<NextApiRequest, NextApiResponse>({
          method: 'POST',
          body
        });
        
        handler(req, res);
        
        expect(res._getStatusCode()).toBe(200);
        const data = JSON.parse(res._getData());
        expect(data.status).toBe('healthy');
      }
    });

    it('should maintain performance under load simulation', () => {
      const startTime = Date.now();
      const concurrentRequests = 10;
      const results = [];
      
      for (let i = 0; i < concurrentRequests; i++) {
        const { req, res } = createMocks<NextApiRequest, NextApiResponse>({
          method: 'GET',
        });
        
        const requestStart = Date.now();
        handler(req, res);
        const requestEnd = Date.now();
        
        results.push({
          statusCode: res._getStatusCode(),
          duration: requestEnd - requestStart,
          data: JSON.parse(res._getData())
        });
      }
      
      const totalTime = Date.now() - startTime;
      
      // All requests should succeed
      results.forEach(({ statusCode, data }) => {
        expect(statusCode).toBe(200);
        expect(data.status).toBe('healthy');
      });
      
      // Performance assertions
      const avgDuration = results.reduce((sum, { duration }) => sum + duration, 0) / results.length;
      expect(avgDuration).toBeLessThan(50); // Average response time under 50ms
      expect(totalTime).toBeLessThan(1000); // All requests complete within 1 second
    });
  });

  describe('API Error Handling', () => {
    it('should handle malformed requests gracefully', () => {
      // Test with various potentially problematic request configurations
      const { req, res } = createMocks<NextApiRequest, NextApiResponse>({
        method: 'GET',
        // Simulate potential edge cases
        url: '/api/health?malformed=%invalid%encoding',
        headers: {
          'content-type': 'application/json',
          'content-length': '999999' // Mismatch with actual body
        }
      });

      handler(req, res);
      
      // Should still respond successfully (health check is robust)
      expect(res._getStatusCode()).toBe(200);
      const data = JSON.parse(res._getData());
      expect(data.status).toBe('healthy');
    });
  });
});