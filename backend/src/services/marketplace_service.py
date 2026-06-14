from typing import List, Dict, Any, Optional


class MarketplaceService:
    INTEGRATIONS = [
        {
            "id": "openai",
            "name": "OpenAI",
            "description": "GPT-4, GPT-3.5, DALL-E, Whisper",
            "category": "ai",
            "icon": "brain",
            "auth_type": "api_key",
            "status": "available",
        },
        {
            "id": "anthropic",
            "name": "Anthropic",
            "description": "Claude 3.5 Sonnet, Claude 3 Opus, Haiku",
            "category": "ai",
            "icon": "sparkles",
            "auth_type": "api_key",
            "status": "available",
        },
        {
            "id": "google",
            "name": "Google AI",
            "description": "Gemini Pro, Gemini Ultra",
            "category": "ai",
            "icon": "globe",
            "auth_type": "api_key",
            "status": "available",
        },
        {
            "id": "github",
            "name": "GitHub",
            "description": "Repository management, code search, issues",
            "category": "developer",
            "icon": "code",
            "auth_type": "oauth",
            "status": "available",
        },
        {
            "id": "slack",
            "name": "Slack",
            "description": "Send messages, manage channels",
            "category": "communication",
            "icon": "message-square",
            "auth_type": "oauth",
            "status": "available",
        },
        {
            "id": "discord",
            "name": "Discord",
            "description": "Bot integration, server management",
            "category": "communication",
            "icon": "headphones",
            "auth_type": "oauth",
            "status": "coming_soon",
        },
        {
            "id": "notion",
            "name": "Notion",
            "description": "Pages, databases, content management",
            "category": "productivity",
            "icon": "book-open",
            "auth_type": "oauth",
            "status": "available",
        },
        {
            "id": "jira",
            "name": "Jira",
            "description": "Issue tracking, project management",
            "category": "productivity",
            "icon": "layout",
            "auth_type": "oauth",
            "status": "available",
        },
        {
            "id": "stripe",
            "name": "Stripe",
            "description": "Payment processing, billing",
            "category": "finance",
            "icon": "credit-card",
            "auth_type": "api_key",
            "status": "coming_soon",
        },
        {
            "id": "hubspot",
            "name": "HubSpot",
            "description": "CRM, marketing, sales automation",
            "category": "crm",
            "icon": "users",
            "auth_type": "oauth",
            "status": "coming_soon",
        },
        {
            "id": "salesforce",
            "name": "Salesforce",
            "description": "Enterprise CRM, analytics",
            "category": "crm",
            "icon": "cloud",
            "auth_type": "oauth",
            "status": "coming_soon",
        },
        {
            "id": "tavily",
            "name": "Tavily Search",
            "description": "AI-powered web search",
            "category": "search",
            "icon": "search",
            "auth_type": "api_key",
            "status": "available",
        },
    ]

    async def list_integrations(
        self, category: Optional[str] = None, status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        results = self.INTEGRATIONS
        if category:
            results = [i for i in results if i["category"] == category]
        if status:
            results = [i for i in results if i["status"] == status]
        return results

    async def get_integration(self, integration_id: str) -> Optional[Dict[str, Any]]:
        for integration in self.INTEGRATIONS:
            if integration["id"] == integration_id:
                return integration
        return None


marketplace_service = MarketplaceService()
