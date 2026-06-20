# API Troubleshooting Guide
If you receive a 401 Unauthorized error, it means your API key is invalid or has expired. 
To resolve this:
1. Log into your developer dashboard.
2. Navigate to "Security" > "API Keys".
3. Generate a new Bearer Token.
Ensure your HTTP headers include: `Authorization: Bearer <YOUR_NEW_TOKEN>`.