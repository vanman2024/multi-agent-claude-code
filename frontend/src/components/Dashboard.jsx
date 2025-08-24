import { useAuth } from '../hooks/useAuth';
import './Dashboard.css';

export function Dashboard() {
  const { user, signOut, loading } = useAuth();

  const handleSignOut = async () => {
    try {
      await signOut();
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Welcome to your Dashboard</h1>
        <button 
          onClick={handleSignOut}
          className="signout-button"
          disabled={loading}
        >
          {loading ? 'Signing out...' : 'Sign Out'}
        </button>
      </header>
      
      <main className="dashboard-content">
        <div className="user-info">
          <h2>User Information</h2>
          <p><strong>Email:</strong> {user?.email}</p>
          <p><strong>User ID:</strong> {user?.id}</p>
          <p><strong>Last Sign In:</strong> {
            user?.last_sign_in_at 
              ? new Date(user.last_sign_in_at).toLocaleString()
              : 'N/A'
          }</p>
        </div>
        
        <div className="session-info">
          <h2>Session Status</h2>
          <div className="status-indicator">
            <div className="status-dot active"></div>
            <span>Active Session</span>
          </div>
          <p>Your session will persist across page refreshes.</p>
        </div>
      </main>
    </div>
  );
}