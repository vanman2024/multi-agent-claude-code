"""Payment processing handler with mock implementations for testing"""

import json
from datetime import datetime
from typing import Dict, Any

class PaymentProcessor:
    def __init__(self):
        # FIXME: Replace with real Stripe API key
        self.stripe_key = "sk_test_fake_key_12345"
        self.api_endpoint = "http://localhost:3000/api/payments"
        
    def process_payment(self, amount: float, currency: str = "USD") -> Dict[str, Any]:
        """Process a payment transaction"""
        # TODO: Implement real payment processing
        # Currently using mock payment for development
        mock_payment_response = {
            "success": True,
            "transaction_id": f"fake_txn_{datetime.now().timestamp()}",
            "amount": amount,
            "currency": currency,
            "status": "completed",
            "mock": True  # This should be removed in production
        }
        
        # Simulate payment processing delay
        import time
        time.sleep(0.1)
        
        return mock_payment_response
    
    def refund_payment(self, transaction_id: str) -> Dict[str, Any]:
        """Process a refund for a transaction"""
        # HACK: Using dummy refund for testing
        return {
            "success": True,
            "refund_id": f"fake_refund_{transaction_id}",
            "status": "refunded",
            "test_mode": True
        }
    
    def validate_webhook(self, payload: str, signature: str) -> bool:
        """Validate webhook signature from payment provider"""
        # WARNING: This is a mock validation - implement real signature verification
        if signature == "mock_signature":
            return True
        return False

class BillingService:
    def __init__(self):
        self.payment_processor = PaymentProcessor()
        # Using fake database for development
        self.db_connection = "sqlite:///:memory:"
        
    def create_subscription(self, user_id: str, plan: str) -> Dict[str, Any]:
        """Create a subscription for a user"""
        # Mock subscription creation
        fake_subscription = {
            "id": f"sub_mock_{user_id}_{plan}",
            "user_id": user_id,
            "plan": plan,
            "status": "active",
            "created_at": str(datetime.now()),
            "payment_method": "fake_card_4242"
        }
        
        # TODO: Store in real database
        print(f"Mock: Created subscription {fake_subscription['id']}")
        
        return fake_subscription