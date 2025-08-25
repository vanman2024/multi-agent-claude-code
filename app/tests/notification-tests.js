#!/usr/bin/env node

/**
 * Notification System Tests
 * Tests the notification system functionality
 */

const NotificationServer = require('../server');
const http = require('http');
const path = require('path');
const fs = require('fs');

class NotificationTests {
  constructor() {
    this.server = null;
    this.port = 3001; // Use different port for testing
    this.baseUrl = `http://localhost:${this.port}`;
  }

  async setup() {
    console.log('🔧 Setting up test environment...');
    
    // Clean up test database
    const testDbPath = path.join(__dirname, '..', 'data', 'test-notifications.db');
    if (fs.existsSync(testDbPath)) {
      fs.unlinkSync(testDbPath);
    }

    // Start test server
    this.server = new NotificationServer(this.port);
    
    return new Promise((resolve) => {
      this.server.start();
      
      // Wait a bit for server to fully start
      setTimeout(resolve, 1000);
    });
  }

  async teardown() {
    console.log('🧹 Cleaning up test environment...');
    
    if (this.server && this.server.server) {
      this.server.server.close();
    }
    
    if (this.server && this.server.db) {
      this.server.db.close();
    }
  }

  async makeRequest(endpoint, method = 'GET', body = null) {
    const url = `${this.baseUrl}${endpoint}`;
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    if (body) {
      options.body = JSON.stringify(body);
    }

    try {
      const response = await fetch(url, options);
      const data = await response.json().catch(() => null);
      return { status: response.status, data, ok: response.ok };
    } catch (error) {
      return { status: 0, data: { error: error.message }, ok: false };
    }
  }

  async testHealthCheck() {
    console.log('🏥 Testing health check...');
    
    const result = await this.makeRequest('/health');
    
    if (result.ok && result.data.status === 'healthy') {
      console.log('  ✅ Health check passed');
      return true;
    } else {
      console.log('  ❌ Health check failed');
      return false;
    }
  }

  async testCreateNotification() {
    console.log('📝 Testing notification creation...');
    
    const notification = {
      userId: 'test-user-1',
      title: 'Test Notification',
      message: 'This is a test notification',
      type: 'info',
      priority: 'normal'
    };

    const result = await this.makeRequest('/api/v1/notifications', 'POST', notification);
    
    if (result.ok && result.data.id) {
      console.log('  ✅ Notification created successfully');
      return result.data;
    } else {
      console.log('  ❌ Failed to create notification:', result.data);
      return null;
    }
  }

  async testGetNotifications() {
    console.log('📋 Testing notification retrieval...');
    
    const result = await this.makeRequest('/api/v1/notifications?userId=test-user-1');
    
    if (result.ok && Array.isArray(result.data.notifications)) {
      console.log(`  ✅ Retrieved ${result.data.notifications.length} notifications`);
      return result.data.notifications;
    } else {
      console.log('  ❌ Failed to retrieve notifications:', result.data);
      return [];
    }
  }

  async testMarkAsRead(notificationId) {
    console.log('✓ Testing mark as read...');
    
    const result = await this.makeRequest(`/api/v1/notifications/${notificationId}/read`, 'PUT');
    
    if (result.ok) {
      console.log('  ✅ Notification marked as read');
      return true;
    } else {
      console.log('  ❌ Failed to mark as read:', result.data);
      return false;
    }
  }

  async testUserPreferences() {
    console.log('⚙️ Testing user preferences...');
    
    // Test getting default preferences
    const getResult = await this.makeRequest('/api/v1/preferences/test-user-1');
    
    if (!getResult.ok) {
      console.log('  ❌ Failed to get preferences:', getResult.data);
      return false;
    }

    // Test updating preferences
    const preferences = {
      email: 'test@example.com',
      email_notifications: 1,
      push_notifications: 0,
      in_app_notifications: 1,
      notification_frequency: 'hourly'
    };

    const updateResult = await this.makeRequest('/api/v1/preferences/test-user-1', 'PUT', preferences);
    
    if (updateResult.ok) {
      console.log('  ✅ Preferences updated successfully');
      return true;
    } else {
      console.log('  ❌ Failed to update preferences:', updateResult.data);
      return false;
    }
  }

  async testDeleteNotification(notificationId) {
    console.log('🗑️ Testing notification deletion...');
    
    const result = await this.makeRequest(`/api/v1/notifications/${notificationId}`, 'DELETE');
    
    if (result.ok) {
      console.log('  ✅ Notification deleted successfully');
      return true;
    } else {
      console.log('  ❌ Failed to delete notification:', result.data);
      return false;
    }
  }

  async testFilteringAndPagination() {
    console.log('🔍 Testing filtering and pagination...');
    
    // Create multiple notifications
    const notifications = [];
    for (let i = 0; i < 5; i++) {
      const notification = await this.makeRequest('/api/v1/notifications', 'POST', {
        userId: 'test-user-2',
        title: `Test Notification ${i + 1}`,
        message: `Message ${i + 1}`,
        type: i % 2 === 0 ? 'info' : 'success',
        priority: 'normal'
      });
      
      if (notification.ok) {
        notifications.push(notification.data);
      }
    }

    // Mark some as read
    if (notifications.length > 2) {
      await this.makeRequest(`/api/v1/notifications/${notifications[0].id}/read`, 'PUT');
      await this.makeRequest(`/api/v1/notifications/${notifications[1].id}/read`, 'PUT');
    }

    // Test unread filter
    const unreadResult = await this.makeRequest('/api/v1/notifications?userId=test-user-2&unread_only=true');
    
    if (unreadResult.ok && unreadResult.data.notifications.length === 3) {
      console.log('  ✅ Unread filtering works correctly');
      return true;
    } else {
      console.log('  ❌ Unread filtering failed:', unreadResult.data);
      return false;
    }
  }

  async runAllTests() {
    console.log('🚀 Starting notification system tests...\n');
    
    const results = {
      setup: false,
      healthCheck: false,
      createNotification: false,
      getNotifications: false,
      markAsRead: false,
      userPreferences: false,
      deleteNotification: false,
      filteringAndPagination: false
    };

    try {
      // Setup
      await this.setup();
      results.setup = true;

      // Run tests
      results.healthCheck = await this.testHealthCheck();
      
      const createdNotification = await this.testCreateNotification();
      results.createNotification = !!createdNotification;
      
      results.getNotifications = await this.testGetNotifications();
      
      if (createdNotification) {
        results.markAsRead = await this.testMarkAsRead(createdNotification.id);
        results.deleteNotification = await this.testDeleteNotification(createdNotification.id);
      }
      
      results.userPreferences = await this.testUserPreferences();
      results.filteringAndPagination = await this.testFilteringAndPagination();

    } catch (error) {
      console.error('❌ Test error:', error);
    } finally {
      await this.teardown();
    }

    // Print results
    console.log('\n=== Test Results ===');
    const totalTests = Object.keys(results).length;
    const passedTests = Object.values(results).filter(Boolean).length;
    
    Object.entries(results).forEach(([test, passed]) => {
      console.log(`${passed ? '✅' : '❌'} ${test}: ${passed ? 'PASSED' : 'FAILED'}`);
    });
    
    console.log(`\nTotal: ${passedTests}/${totalTests} tests passed`);
    
    if (passedTests === totalTests) {
      console.log('🎉 All tests passed!');
      process.exit(0);
    } else {
      console.log('💥 Some tests failed');
      process.exit(1);
    }
  }
}

// Add fetch polyfill for Node.js if needed
if (typeof fetch === 'undefined') {
  global.fetch = require('node-fetch');
}

// Run tests if called directly
if (require.main === module) {
  const tests = new NotificationTests();
  tests.runAllTests();
}

module.exports = NotificationTests;