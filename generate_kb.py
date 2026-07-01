import os

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

documents = {
    "api_rate_limits.md": "# API Rate Limits\nTo ensure platform stability, all API requests are rate-limited to 1,000 requests per minute per IP address. Exceeding this limit will trigger a 429 Too Many Requests error. Enterprise customers can request a limit increase via their account manager.",
    "billing_refunds.md": "# Billing and Refunds\nWe offer a 14-day money-back guarantee for all new SaaS subscriptions. If you experience duplicate charges due to a system glitch, you are entitled to an immediate refund. Dispute processing takes 3-5 business days.",
    "sso_configuration.md": "# Configuring SAML SSO\nSingle Sign-On (SSO) is available for Enterprise tiers. We support Okta, Azure AD, and Google Workspace. You must map your Identity Provider's 'Email' attribute to our 'email_address' field. Contact support if your metadata XML fails to upload.",
    "webhook_setup.md": "# Webhook Integrations\nWebhooks allow your application to receive real-time POST requests when events occur. Payloads are sent in JSON format. You must secure your webhooks by validating the `X-Signature` header using your secret key.",
    "user_roles.md": "# User Roles and Permissions\n- **Admin:** Full access to billing, API keys, and user management.\n- **Editor:** Can create and edit project files but cannot delete projects.\n- **Viewer:** Read-only access to dashboards.",
    "troubleshoot_401.md": "# Troubleshooting 401 Unauthorized\nA 401 Unauthorized error means your Bearer token is missing, expired, or invalid. Navigate to Settings > Developer > API Keys to generate a new token. Never share your secret keys in public repositories.",
    "data_retention.md": "# Data Retention Policy\nInactive free-tier accounts are permanently deleted after 180 days of inactivity. Enterprise data backups are retained across multiple geographic zones for 7 years for compliance with SOC2 standards.",
    "supported_browsers.md": "# Supported Browsers\nOur web application is optimized for the latest versions of Google Chrome, Mozilla Firefox, and Microsoft Edge. Safari is supported on macOS 12 and above. Internet Explorer is strictly not supported.",
    "two_factor_auth.md": "# Two-Factor Authentication (2FA)\n2FA is highly recommended. We support Authenticator apps (Google, Authy) via TOTP. SMS-based 2FA has been deprecated due to security vulnerabilities.",
    "cancel_subscription.md": "# How to Cancel\nYou can cancel or downgrade your subscription at any time under Billing > Plan Details. Downgrades take effect at the end of your current billing cycle. No prorated refunds are issued for mid-month cancellations."
}

for filename, content in documents.items():
    filepath = os.path.join("data", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print(f"✅ Successfully generated {len(documents)} realistic SaaS documents in the /data folder!")