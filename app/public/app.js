/**
 * Notification Center Frontend
 * Handles WebSocket connections and UI interactions
 */

class NotificationApp {
  constructor() {
    this.socket = null;
    this.currentUserId = null;
    this.notifications = [];
    
    this.initializeUI();
    this.bindEvents();
  }

  initializeUI() {
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        this.switchTab(e.target.dataset.tab);
      });
    });

    // Connection controls
    const connectBtn = document.getElementById('connectBtn');
    const userIdInput = document.getElementById('userId');
    
    connectBtn.addEventListener('click', () => {
      const userId = userIdInput.value.trim();
      if (userId) {
        this.connect(userId);
      }
    });

    // Auto-connect with default user
    if (userIdInput.value) {
      this.connect(userIdInput.value);
    }
  }

  bindEvents() {
    // Notifications tab
    document.getElementById('refreshBtn').addEventListener('click', () => this.loadNotifications());
    document.getElementById('unreadOnly').addEventListener('change', () => this.loadNotifications());
    document.getElementById('markAllReadBtn').addEventListener('click', () => this.markAllAsRead());

    // Preferences tab
    document.getElementById('savePreferencesBtn').addEventListener('click', () => this.savePreferences());

    // Test tab
    document.getElementById('sendTestBtn').addEventListener('click', () => this.sendTestNotification());
  }

  switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
      content.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');

    // Load data for specific tabs
    if (tabName === 'notifications' && this.currentUserId) {
      this.loadNotifications();
    } else if (tabName === 'preferences' && this.currentUserId) {
      this.loadPreferences();
    }
  }

  connect(userId) {
    this.currentUserId = userId;
    
    if (this.socket) {
      this.socket.disconnect();
    }

    this.socket = io();
    
    this.socket.on('connect', () => {
      console.log('Connected to notification server');
      this.updateConnectionStatus('connected');
      this.socket.emit('join_user', userId);
      this.loadNotifications();
      this.loadPreferences();
    });

    this.socket.on('disconnect', () => {
      console.log('Disconnected from notification server');
      this.updateConnectionStatus('disconnected');
    });

    this.socket.on('new_notification', (notification) => {
      console.log('New notification received:', notification);
      this.showToast(notification);
      this.loadNotifications(); // Refresh the list
    });

    this.socket.on('connect_error', (error) => {
      console.error('Connection error:', error);
      this.updateConnectionStatus('error');
    });
  }

  updateConnectionStatus(status) {
    const statusElement = document.getElementById('connectionStatus');
    statusElement.className = `status ${status}`;
    
    switch (status) {
      case 'connected':
        statusElement.textContent = 'Connected';
        break;
      case 'disconnected':
        statusElement.textContent = 'Disconnected';
        break;
      case 'error':
        statusElement.textContent = 'Error';
        break;
    }
  }

  async loadNotifications() {
    if (!this.currentUserId) return;

    const unreadOnly = document.getElementById('unreadOnly').checked;
    const url = `/api/v1/notifications?userId=${this.currentUserId}&unread_only=${unreadOnly}`;
    
    try {
      const response = await fetch(url);
      const data = await response.json();
      
      if (response.ok) {
        this.notifications = data.notifications;
        this.renderNotifications();
      } else {
        this.showToast({ title: 'Error', message: data.error || 'Failed to load notifications', type: 'error' });
      }
    } catch (error) {
      console.error('Error loading notifications:', error);
      this.showToast({ title: 'Error', message: 'Failed to load notifications', type: 'error' });
    }
  }

  renderNotifications() {
    const container = document.getElementById('notificationsList');
    
    if (this.notifications.length === 0) {
      container.innerHTML = '<div class="empty-state">📭 No notifications found</div>';
      return;
    }

    container.innerHTML = this.notifications.map(notification => {
      const time = new Date(notification.created_at).toLocaleString();
      const typeIcon = this.getTypeIcon(notification.type);
      const priorityClass = `priority-${notification.priority}`;
      const readClass = notification.read ? 'read' : 'unread';
      
      return `
        <div class="notification ${readClass} ${priorityClass}" data-id="${notification.id}">
          <div class="notification-icon">${typeIcon}</div>
          <div class="notification-content">
            <div class="notification-header">
              <h4 class="notification-title">${this.escapeHtml(notification.title)}</h4>
              <span class="notification-time">${time}</span>
            </div>
            <p class="notification-message">${this.escapeHtml(notification.message)}</p>
            <div class="notification-meta">
              <span class="type-badge type-${notification.type}">${notification.type}</span>
              <span class="priority-badge priority-${notification.priority}">${notification.priority}</span>
            </div>
          </div>
          <div class="notification-actions">
            ${!notification.read ? '<button class="mark-read-btn" onclick="app.markAsRead(\'' + notification.id + '\')">✓</button>' : ''}
            <button class="delete-btn" onclick="app.deleteNotification('${notification.id}')">🗑️</button>
          </div>
        </div>
      `;
    }).join('');
  }

  getTypeIcon(type) {
    const icons = {
      info: 'ℹ️',
      success: '✅',
      warning: '⚠️',
      error: '❌'
    };
    return icons[type] || 'ℹ️';
  }

  async markAsRead(notificationId) {
    try {
      const response = await fetch(`/api/v1/notifications/${notificationId}/read`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' }
      });

      if (response.ok) {
        this.loadNotifications();
      } else {
        const data = await response.json();
        this.showToast({ title: 'Error', message: data.error || 'Failed to mark as read', type: 'error' });
      }
    } catch (error) {
      console.error('Error marking as read:', error);
      this.showToast({ title: 'Error', message: 'Failed to mark as read', type: 'error' });
    }
  }

  async markAllAsRead() {
    const unreadNotifications = this.notifications.filter(n => !n.read);
    
    for (const notification of unreadNotifications) {
      await this.markAsRead(notification.id);
    }
  }

  async deleteNotification(notificationId) {
    if (!confirm('Are you sure you want to delete this notification?')) return;

    try {
      const response = await fetch(`/api/v1/notifications/${notificationId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        this.loadNotifications();
      } else {
        const data = await response.json();
        this.showToast({ title: 'Error', message: data.error || 'Failed to delete notification', type: 'error' });
      }
    } catch (error) {
      console.error('Error deleting notification:', error);
      this.showToast({ title: 'Error', message: 'Failed to delete notification', type: 'error' });
    }
  }

  async loadPreferences() {
    if (!this.currentUserId) return;

    try {
      const response = await fetch(`/api/v1/preferences/${this.currentUserId}`);
      const preferences = await response.json();
      
      if (response.ok) {
        this.populatePreferences(preferences);
      } else {
        this.showToast({ title: 'Error', message: preferences.error || 'Failed to load preferences', type: 'error' });
      }
    } catch (error) {
      console.error('Error loading preferences:', error);
      this.showToast({ title: 'Error', message: 'Failed to load preferences', type: 'error' });
    }
  }

  populatePreferences(preferences) {
    document.getElementById('emailInput').value = preferences.email || '';
    document.getElementById('emailNotifications').checked = !!preferences.email_notifications;
    document.getElementById('pushNotifications').checked = !!preferences.push_notifications;
    document.getElementById('inAppNotifications').checked = !!preferences.in_app_notifications;
    document.getElementById('notificationFrequency').value = preferences.notification_frequency || 'immediate';
  }

  async savePreferences() {
    if (!this.currentUserId) return;

    const preferences = {
      email: document.getElementById('emailInput').value,
      email_notifications: document.getElementById('emailNotifications').checked ? 1 : 0,
      push_notifications: document.getElementById('pushNotifications').checked ? 1 : 0,
      in_app_notifications: document.getElementById('inAppNotifications').checked ? 1 : 0,
      notification_frequency: document.getElementById('notificationFrequency').value
    };

    try {
      const response = await fetch(`/api/v1/preferences/${this.currentUserId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(preferences)
      });

      const result = await response.json();
      
      if (response.ok) {
        this.showToast({ title: 'Success', message: 'Preferences saved successfully', type: 'success' });
      } else {
        this.showToast({ title: 'Error', message: result.error || 'Failed to save preferences', type: 'error' });
      }
    } catch (error) {
      console.error('Error saving preferences:', error);
      this.showToast({ title: 'Error', message: 'Failed to save preferences', type: 'error' });
    }
  }

  async sendTestNotification() {
    if (!this.currentUserId) return;

    const notification = {
      userId: this.currentUserId,
      title: document.getElementById('testTitle').value,
      message: document.getElementById('testMessage').value,
      type: document.getElementById('testType').value,
      priority: document.getElementById('testPriority').value
    };

    try {
      const response = await fetch('/api/v1/notifications', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(notification)
      });

      const result = await response.json();
      
      if (response.ok) {
        this.showToast({ title: 'Success', message: 'Test notification sent', type: 'success' });
      } else {
        this.showToast({ title: 'Error', message: result.error || 'Failed to send notification', type: 'error' });
      }
    } catch (error) {
      console.error('Error sending test notification:', error);
      this.showToast({ title: 'Error', message: 'Failed to send notification', type: 'error' });
    }
  }

  showToast(notification) {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast toast-${notification.type || 'info'}`;
    
    toast.innerHTML = `
      <div class="toast-content">
        <strong>${this.escapeHtml(notification.title)}</strong>
        <p>${this.escapeHtml(notification.message)}</p>
      </div>
      <button class="toast-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    container.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
      if (toast.parentElement) {
        toast.remove();
      }
    }, 5000);
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Initialize app
const app = new NotificationApp();