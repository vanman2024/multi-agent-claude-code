import React from 'react';
import TestComponent from '../components/TestComponent';

export default function Home() {
  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui' }}>
      <h1>Multi-Agent Framework Test</h1>
      <p>This is a test Next.js application for the multi-agent development framework.</p>
      
      <section style={{ marginTop: '2rem' }}>
        <h2>Framework Status</h2>
        <ul>
          <li>✅ Next.js Application Running</li>
          <li>✅ TypeScript Configured</li>
          <li>✅ Testing Setup Complete</li>
          <li>✅ API Routes Available</li>
        </ul>
      </section>

      <section style={{ marginTop: '2rem' }}>
        <h2>Test Component</h2>
        <TestComponent />
      </section>

      <section style={{ marginTop: '2rem' }}>
        <h2>Deployment Info</h2>
        <p>Environment: {process.env.NODE_ENV}</p>
        <p>Deployed via: Vercel</p>
      </section>
    </div>
  );
}