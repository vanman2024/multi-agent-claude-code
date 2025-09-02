import { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: string;
  trend?: 'up' | 'down' | 'neutral';
}

const StatCard = ({ title, value, icon, trend }: StatCardProps) => {
  const trendColors = {
    up: 'text-green-600',
    down: 'text-red-600',
    neutral: 'text-gray-600'
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400">{title}</p>
          <p className="text-2xl font-bold mt-2 dark:text-white">{value}</p>
        </div>
        <div className="text-3xl">{icon}</div>
      </div>
      {trend && (
        <div className={`mt-4 text-sm ${trendColors[trend]}`}>
          {trend === 'up' && '↑ 12% from last month'}
          {trend === 'down' && '↓ 3% from last month'}
          {trend === 'neutral' && '→ No change'}
        </div>
      )}
    </div>
  );
};

export default function Dashboard() {
  const [darkMode, setDarkMode] = useState(false);

  // Mock data - would come from API
  const stats = {
    deployments: 17,
    apiCalls: '2,451',
    activeProjects: 3,
    lastLogin: '2 hours ago'
  };

  return (
    <div className={`min-h-screen ${darkMode ? 'dark bg-gray-900' : 'bg-gray-50'}`}>
      <Head>
        <title>User Dashboard | Multi-Agent Framework</title>
        <meta name="description" content="View your usage statistics and recent activity" />
      </Head>

      <nav className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/" className="text-xl font-bold text-gray-900 dark:text-white">
                Multi-Agent Framework
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setDarkMode(!darkMode)}
                className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600"
                aria-label="Toggle dark mode"
              >
                {darkMode ? '☀️' : '🌙'}
              </button>
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
                  U
                </div>
                <span className="text-sm font-medium text-gray-900 dark:text-white">User</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Welcome back! Here's an overview of your activity.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Recent Deployments"
            value={stats.deployments}
            icon="🚀"
            trend="up"
          />
          <StatCard
            title="API Calls"
            value={stats.apiCalls}
            icon="📡"
            trend="up"
          />
          <StatCard
            title="Active Projects"
            value={stats.activeProjects}
            icon="📁"
            trend="neutral"
          />
          <StatCard
            title="Last Login"
            value={stats.lastLogin}
            icon="🕐"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4 dark:text-white">Recent Activity</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between py-2 border-b dark:border-gray-700">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">✅</span>
                  <div>
                    <p className="font-medium dark:text-white">Deployment Successful</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">main branch - 5 minutes ago</p>
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-between py-2 border-b dark:border-gray-700">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">🔄</span>
                  <div>
                    <p className="font-medium dark:text-white">PR Merged</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">#109 - 30 minutes ago</p>
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-between py-2">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">🧪</span>
                  <div>
                    <p className="font-medium dark:text-white">Tests Passed</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">All checks green - 1 hour ago</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4 dark:text-white">Quick Actions</h2>
            <div className="space-y-3">
              <Link
                href="/api/health"
                className="block w-full text-left px-4 py-3 bg-blue-50 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-800"
              >
                🔍 Check API Health
              </Link>
              <Link
                href="/"
                className="block w-full text-left px-4 py-3 bg-green-50 dark:bg-green-900 text-green-700 dark:text-green-300 rounded-lg hover:bg-green-100 dark:hover:bg-green-800"
              >
                🏠 View Homepage
              </Link>
              <button
                onClick={() => alert('Creating new deployment...')}
                className="block w-full text-left px-4 py-3 bg-purple-50 dark:bg-purple-900 text-purple-700 dark:text-purple-300 rounded-lg hover:bg-purple-100 dark:hover:bg-purple-800"
              >
                🚀 New Deployment
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}