# Email Summarizer Agent

This agent uses the CirtusAI SDK and LangChain to read, summarize, and send emails.

## Setup

1.  **Set Environment Variables:**
    Create a file named `.env` in this directory and add the following:
    ```
    CIRTUS_API_URL="http://localhost:8000" # Or your CirtusAI backend URL
    CIRTUS_USERNAME="your_cirtus_username"
    CIRTUS_PASSWORD="your_cirtus_password"
    CIRTUS_AGENT_ID="your_child_agent_id" # Agent with 'email:read' and 'email:send' permissions
    DEEPSEEK_API_KEY="your_deepseek_api_key"
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start the interactive agent, run:

```bash
python run_agent.py
```

Once the agent is running, you can interact with it by typing commands:

*   **To read and summarize emails:**
    `read emails` or `summarize my inbox`

*   **To send an email:**
    `send an email to [recipient] with subject [subject] and body [body]`
    (e.g., `send an email to test@example.com with subject Hello and body This is a test.`) 

*   **To exit the session:**
    `exit` or `quit`

## Live Demo

Here is a demonstration of the agent's capabilities:

### Get Email Account Information

**Command:**

```bash
python run_agent.py get email account information
```

**Output:**

```
--- Initializing Email Summarizer Agent ---

> Entering new AgentExecutor chain...

Invoking: `get_email_account` with `{}`

Email accounts: [{'provider': 'imap', 'email_address': 'cirtus@cirtusai.com', 'config': {'host': 'imap.feishu.cn', 'port': 993, 'username': 'cirtus@cirtusai.com', 'password': 'xxxxxxxxxxx', 'use_ssl': True, 'smtp_host': 'smtp.feishu.cn', 'smtp_port': 465, 'smtp_user': 'cirtus@cirtusai.com', 'smtp_password': 'xxxxxxxxxxxx', 'smtp_use_tls': True}, 'id': '99ad4a79-f0bd-432d-bfc5-aaeb715c3616', 'user_id': '0e2f868c-7646-45c7-8fe1-d3589afc5c1d', 'created_at': '2025-07-14T04:32:25.495154Z', 'updated_at': '2025-07-24T07:01:19.617257Z'}]

> Finished chain.

Agent Response:
Here's your email account information:

**Email Account Details:**
- **Email Address:** cirtus@cirtusai.com
- **Provider:** IMAP
- **Account ID:** 99ad4a79-f0bd-432d-bfc5-aaeb715c3616

**IMAP Configuration:**
- **Host:** imap.feishu.cn
- **Port:** 993
- **SSL Enabled:** Yes

**SMTP Configuration:**
- **Host:** smtp.feishu.cn
- **Port:** 465
- **TLS Enabled:** Yes

**Account Status:**
- **Created:** July 14, 2025
- **Last Updated:** July 24, 2025

Your email account is configured to use Feishu's email service with both IMAP (for receiving emails) and SMTP (for sending emails) properly set up with secure connections.
```

### Send an Email

**Command:**

```bash
python run_agent.py send an email to demo@example.com with subject "CirtusAI SDK Demo" and body "This email was sent by an AI agent built with the CirtusAI SDK."
```

**Output:**

```
--- Initializing Email Summarizer Agent ---

> Entering new AgentExecutor chain...

Invoking: `send_email` with `{'recipient': 'demo@example.com', 'subject': 'CirtusAI SDK Demo', 'body': 'This email was sent by an AI agent built with the CirtusAI SDK.'}`

--- Authenticating with CirtusAI ---
Authentication successful.
--- Verifying Permissions for Agent: my-test-agent ---
Agent Permissions: ['email:read', 'email:send']
--- Permission Granted: Sending Email ---
Email sent successfully.

> Finished chain.

Agent Response:
The email has been sent successfully to demo@example.com with the subject "CirtusAI SDK Demo" and your specified message about the CirtusAI SDK.
```

### Summarize Inbox

**Command:**

```bash
python run_agent.py summarize my inbox
```

**Output:**

```
--- Initializing Email Summarizer Agent ---

> Entering new AgentExecutor chain...

Invoking: `read_and_summarize_emails` with `{}`

--- Authenticating with CirtusAI ---
Authentication successful.
--- Verifying Permissions for Agent: my-test-agent ---
Agent Permissions: ['email:read', 'email:send']
--- Permission Granted: Reading Inbox ---
--- Found 1 messages to summarize ---
--- Formatting Summary ---
Sender,Subject,Summary
<mailer-daemon@feishu.cn>,邮件退信,The email to demo@example.com failed to deliver.

> Finished chain.

Agent Response:
Based on your inbox, here's a summary:

**Email Summary:**
- **From:** mailer-daemon@feishu.cn
- **Subject:** 邮件退信 (Email Return/Bounce)
- **Summary:** The email to demo@example.com failed to deliver.

You have one email in your inbox, which appears to be a delivery failure notification (bounce message) from Feishu's mail system. It indicates that an email you sent to demo@example.com could not be delivered successfully.
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.