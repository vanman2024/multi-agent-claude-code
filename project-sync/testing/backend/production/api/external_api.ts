// External API integration with mock implementations

interface ApiResponse {
    success: boolean;
    data?: any;
    error?: string;
}

class ExternalAPIClient {
    private apiKey: string;
    private baseUrl: string;
    private useMockData: boolean;
    
    constructor() {
        // TODO: Replace with production API configuration
        this.apiKey = 'test_api_key_123456';
        this.baseUrl = 'http://localhost:8080/api';
        this.useMockData = true; // Should be false in production
    }
    
    async fetchUserData(userId: string): Promise<ApiResponse> {
        // FIXME: Implement real API call
        if (this.useMockData) {
            // Return fake API response
            return {
                success: true,
                data: {
                    id: userId,
                    name: 'Mock User',
                    email: 'mock@example.com',
                    subscription: 'fake_premium_plan',
                    mockData: true
                }
            };
        }
        
        // Production code would make actual HTTP request
        throw new NotImplementedError('Real API not implemented');
    }
    
    async sendNotification(userId: string, message: string): Promise<ApiResponse> {
        // Mock notification service
        console.log(`MOCK: Sending notification to ${userId}: ${message}`);
        
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 100));
        
        return {
            success: true,
            data: {
                notificationId: `fake_notification_${Date.now()}`,
                status: 'sent',
                testMode: true
            }
        };
    }
}

// Mock third-party service integration
class ThirdPartyService {
    private serviceUrl: string = 'http://127.0.0.1:9000/service';
    private authToken: string = 'dummy_auth_token';
    
    async syncData(data: any): Promise<boolean> {
        // HACK: Using dummy sync for development
        console.log('Mock: Syncing data with third-party service');
        
        // Placeholder for real implementation
        if (data) {
            return true;
        }
        
        return false;
    }
    
    async validateWebhook(payload: string, signature: string): boolean {
        // Mock webhook validation
        if (signature === 'test_signature_123') {
            return true;
        }
        
        // TODO: Implement real signature verification
        console.warn('Using mock webhook validation - not secure!');
        return false;
    }
}

export { ExternalAPIClient, ThirdPartyService };