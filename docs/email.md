# CirtusAI SDK Email Services Guide

## Overview

The CirtusAI SDK provides comprehensive email services with AI-powered features including inbox management, email sending, automated summarization, and integration with agent-based workflows. The email system supports multiple providers and includes advanced LangChain integration for intelligent email processing.

## Features

- **Multi-Provider Support**: Gmail, Outlook, and other email providers
- **Agent-Based Access**: Permission-controlled email access for child agents
- **AI-Powered Summarization**: Automated email content analysis and summarization
- **LangChain Integration**: Advanced email processing tools
- **Real-Time Processing**: Live email monitoring and processing
- **Secure Authentication**: OAuth2 and secure token management

## Basic Email Operations

### Reading Emails

```python
from cirtusai import CirtusAIClient

client = CirtusAIClient("https://api.cirtusai.com")
client.set_token("your_access_token")

# Read inbox for a specific agent
agent_id = "child_agent_123"
messages = client.email.read_inbox(agent_id)

for message in messages:
    print(f"From: {message.get('from', 'Unknown')}")
    print(f"Subject: {message.get('subject', 'No Subject')}")
    print(f"Date: {message.get('date')}")
    print(f"Body: {message.get('text_body', '')[:200]}...")
    print("-" * 50)
```

### Sending Emails

```python
# Send email from agent
email_result = client.email.send_email(
    agent_id="child_agent_123",
    recipient="recipient@example.com",
    subject="Automated Email from CirtusAI Agent",
    body="This is an automated email sent using the CirtusAI SDK."
)

print(f"Email sent: {email_result['success']}")
print(f"Message ID: {email_result.get('message_id')}")
```

## AI-Powered Email Processing

### Email Summarization Tool

The SDK includes a powerful LangChain-based email summarization tool:

```python
from cirtusai.email import EmailSummarizerTool
from langchain_deepseek import ChatDeepSeek

# Setup the email summarizer
llm = ChatDeepSeek(
    api_key="your_deepseek_api_key",
    model="deepseek-chat"
)

email_tool = EmailSummarizerTool(
    llm=llm,
    client=client,
    agent_id="child_agent_123",
    username="your_username",
    password="your_password"
)

# Execute email summarization
summary_result = email_tool._run()
print(summary_result)
```

### Custom Email Processing

```python
def process_emails_with_ai(client, agent_id, llm):
    """Custom email processing with AI analysis"""
    
    # Read recent emails
    messages = client.email.read_inbox(agent_id)
    
    if not messages:
        return "No new emails to process"
    
    processed_emails = []
    
    for message in messages:
        email_content = message.get('text_body', '')
        sender = message.get('from', 'Unknown')
        subject = message.get('subject', 'No Subject')
        
        # AI-powered analysis
        analysis_prompt = f"""
        Analyze the following email and provide:
        1. Sentiment (positive/negative/neutral)
        2. Priority level (high/medium/low)
        3. Action required (yes/no)
        4. Category (business/personal/marketing/support)
        
        Email:
        From: {sender}
        Subject: {subject}
        Content: {email_content}
        """
        
        analysis = llm.invoke(analysis_prompt).content
        
        # Generate summary
        summary_prompt = f"Summarize this email in one sentence: {email_content}"
        summary = llm.invoke(summary_prompt).content
        
        processed_emails.append({
            "from": sender,
            "subject": subject,
            "summary": summary,
            "analysis": analysis,
            "original_content": email_content[:500]  # First 500 chars
        })
    
    return processed_emails

# Usage
from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(api_key="your_deepseek_api_key")
processed = process_emails_with_ai(client, "child_agent_123", llm)

for email in processed:
    print(f"From: {email['from']}")
    print(f"Subject: {email['subject']}")
    print(f"Summary: {email['summary']}")
    print(f"Analysis: {email['analysis']}")
    print("-" * 50)
```

## Advanced Email Workflows

### Automated Email Response System

```python
def setup_auto_responder(client, agent_id, llm, response_templates):
    """Setup automated email response system"""
    
    def classify_email(content, subject):
        """Classify email to determine response template"""
        classification_prompt = f"""
        Classify this email into one of these categories:
        - support_request
        - business_inquiry  
        - appointment_request
        - general_question
        - spam
        
        Email Subject: {subject}
        Content: {content}
        
        Return only the category name.
        """
        
        category = llm.invoke(classification_prompt).content.strip().lower()
        return category
    
    def generate_response(category, original_content, sender):
        """Generate personalized response based on category"""
        
        if category not in response_templates:
            category = "general_question"
        
        template = response_templates[category]
        
        personalization_prompt = f"""
        Personalize this email template based on the original email:
        
        Template: {template}
        Original Email: {original_content}
        Sender: {sender}
        
        Make it sound natural and address specific points from the original email.
        """
        
        personalized_response = llm.invoke(personalization_prompt).content
        return personalized_response
    
    # Main processing loop
    messages = client.email.read_inbox(agent_id)
    
    for message in messages:
        content = message.get('text_body', '')
        subject = message.get('subject', '')
        sender = message.get('from', '')
        
        # Skip if already processed (you'd implement this logic)
        if message.get('processed'):
            continue
        
        # Classify and generate response
        category = classify_email(content, subject)
        
        if category != 'spam':
            response = generate_response(category, content, sender)
            
            # Send automated response
            client.email.send_email(
                agent_id=agent_id,
                recipient=sender,
                subject=f"Re: {subject}",
                body=response
            )
            
            print(f"Auto-responded to {sender} - Category: {category}")

# Response templates
templates = {
    "support_request": "Thank you for reaching out. We've received your support request and will respond within 24 hours.",
    "business_inquiry": "Thank you for your business inquiry. We'll review your request and get back to you shortly.",
    "appointment_request": "We've received your appointment request. Please check your calendar for available slots.",
    "general_question": "Thank you for your email. We'll review your question and provide a response soon."
}

# Setup auto-responder
setup_auto_responder(client, "child_agent_123", llm, templates)
```

### Email Analytics and Reporting

```python
def analyze_email_patterns(client, agent_id, llm, days=30):
    """Analyze email patterns and generate insights"""
    
    # Get emails (in a real implementation, you'd filter by date)
    messages = client.email.read_inbox(agent_id)
    
    if not messages:
        return {"error": "No emails found for analysis"}
    
    # Collect email data
    email_data = []
    for message in messages:
        email_data.append({
            "sender": message.get('from', ''),
            "subject": message.get('subject', ''),
            "content": message.get('text_body', ''),
            "date": message.get('date', ''),
            "length": len(message.get('text_body', ''))
        })
    
    # Generate analytics
    analysis_prompt = f"""
    Analyze these {len(email_data)} emails and provide insights:
    
    1. Most common email types/categories
    2. Busiest senders
    3. Average email length
    4. Common themes or topics
    5. Response time requirements
    
    Email subjects: {[email['subject'] for email in email_data[:10]]}
    
    Provide a structured analysis report.
    """
    
    insights = llm.invoke(analysis_prompt).content
    
    # Basic statistics
    total_emails = len(email_data)
    avg_length = sum(email['length'] for email in email_data) / total_emails
    unique_senders = len(set(email['sender'] for email in email_data))
    
    return {
        "total_emails": total_emails,
        "unique_senders": unique_senders,
        "average_length": avg_length,
        "ai_insights": insights,
        "period_days": days
    }

# Usage
analytics = analyze_email_patterns(client, "child_agent_123", llm)
print(f"Email Analytics Report:")
print(f"Total Emails: {analytics['total_emails']}")
print(f"Unique Senders: {analytics['unique_senders']}")
print(f"Average Length: {analytics['average_length']:.0f} characters")
print(f"\nAI Insights:\n{analytics['ai_insights']}")
```

### Email-Driven Task Automation

```python
def setup_email_task_automation(client, agent_id, llm):
    """Setup email-driven task automation"""
    
    def extract_tasks_from_email(content, subject, sender):
        """Extract actionable tasks from email content"""
        
        task_extraction_prompt = f"""
        Extract actionable tasks from this email. Return as a JSON list of tasks.
        Each task should have: description, priority (high/medium/low), deadline (if mentioned).
        
        From: {sender}
        Subject: {subject}
        Content: {content}
        
        Example format:
        [
            {
                "description": "Schedule meeting with client",
                "priority": "high",
                "deadline": "this week"
            }
        ]
        """
        
        tasks_json = llm.invoke(task_extraction_prompt).content
        
        try:
            # Parse JSON (you'd want better error handling)
            import json
            tasks = json.loads(tasks_json)
            return tasks
        except:
            return []
    
    def create_calendar_event(task):
        """Create calendar event for task (mock implementation)"""
        print(f"📅 Created calendar event: {task['description']}")
        return {"event_id": f"event_{hash(task['description'])}", "status": "created"}
    
    def send_task_confirmation(sender, tasks):
        """Send confirmation email with extracted tasks"""
        
        task_list = "\n".join([f"- {task['description']} (Priority: {task['priority']})" for task in tasks])
        
        confirmation_body = f"""
        Thank you for your email. I've extracted the following tasks:
        
        {task_list}
        
        I'll work on these and update you on progress.
        
        Best regards,
        CirtusAI Assistant
        """
        
        client.email.send_email(
            agent_id=agent_id,
            recipient=sender,
            subject="Task Confirmation - Action Items Extracted",
            body=confirmation_body
        )
    
    # Process emails for task extraction
    messages = client.email.read_inbox(agent_id)
    
    for message in messages:
        content = message.get('text_body', '')
        subject = message.get('subject', '')
        sender = message.get('from', '')
        
        # Extract tasks
        tasks = extract_tasks_from_email(content, subject, sender)
        
        if tasks:
            print(f"Extracted {len(tasks)} tasks from email from {sender}")
            
            # Create calendar events
            for task in tasks:
                create_calendar_event(task)
            
            # Send confirmation
            send_task_confirmation(sender, tasks)

# Setup task automation
setup_email_task_automation(client, "child_agent_123", llm)
```

## Integration with Other SDK Components

### Email + Wallet Integration

```python
def setup_financial_email_monitoring(client, agent_id, llm):
    """Monitor emails for financial information and trigger wallet actions"""
    
    messages = client.email.read_inbox(agent_id)
    
    for message in messages:
        content = message.get('text_body', '')
        subject = message.get('subject', '')
        
        # Check for financial keywords
        financial_keywords = ['payment', 'invoice', 'transfer', 'crypto', 'wallet', 'transaction']
        
        if any(keyword in content.lower() or keyword in subject.lower() for keyword in financial_keywords):
            
            # Extract financial information using AI
            financial_prompt = f"""
            Extract financial information from this email:
            - Amount (if mentioned)
            - Currency/Token
            - Transaction type (payment/receipt/request)
            - Wallet address (if any)
            
            Email: {content}
            
            Return as structured data.
            """
            
            financial_info = llm.invoke(financial_prompt).content
            print(f"Financial email detected from {message.get('from')}:")
            print(f"Analysis: {financial_info}")
            
            # You could trigger wallet operations here
            # For example, check balances, prepare transactions, etc.
            try:
                wallets = client.wallets.list_wallets()
                print(f"Available wallets: {len(wallets)}")
            except Exception as e:
                print(f"Could not access wallet info: {e}")

# Setup financial monitoring
setup_financial_email_monitoring(client, "child_agent_123", llm)
```

### Email + Agent Management

```python
def email_driven_agent_creation(client, master_agent_id, llm):
    """Create child agents based on email requests"""
    
    messages = client.email.read_inbox(master_agent_id)
    
    for message in messages:
        content = message.get('text_body', '')
        subject = message.get('subject', '')
        sender = message.get('from', '')
        
        # Check if email is requesting agent creation
        if 'create agent' in content.lower() or 'new agent' in content.lower():
            
            # Extract agent requirements using AI
            agent_prompt = f"""
            Extract agent creation requirements from this email:
            - Agent name/purpose
            - Required permissions
            - Needed assets (email/wallet)
            
            Email content: {content}
            
            Return as structured requirements.
            """
            
            requirements = llm.invoke(agent_prompt).content
            print(f"Agent creation request from {sender}:")
            print(f"Requirements: {requirements}")
            
            # Create child agent (simplified)
            try:
                child_agent = client.agents.create_child_agent(
                    parent_id=master_agent_id,
                    name=f"Agent for {sender}",
                    permissions_granted=["email:read", "email:send"]
                )
                
                # Send confirmation
                client.email.send_email(
                    agent_id=master_agent_id,
                    recipient=sender,
                    subject="Agent Created Successfully",
                    body=f"Your requested agent has been created with ID: {child_agent['id']}"
                )
                
            except Exception as e:
                print(f"Failed to create agent: {e}")

# Setup agent creation automation
email_driven_agent_creation(client, "master_agent_123", llm)
```

## Error Handling and Best Practices

### Robust Email Processing

```python
def safe_email_operation(client, operation, *args, **kwargs):
    """Safely execute email operations with proper error handling"""
    
    try:
        result = getattr(client.email, operation)(*args, **kwargs)
        return {"success": True, "result": result}
    
    except requests.exceptions.HTTPError as e:
        error_code = e.response.status_code
        
        if error_code == 403:
            return {"success": False, "error": "Permission denied - check agent email permissions"}
        elif error_code == 404:
            return {"success": False, "error": "Agent not found or email not configured"}
        else:
            return {"success": False, "error": f"HTTP {error_code}: {e}"}
    
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}

# Usage
result = safe_email_operation(client, "read_inbox", "child_agent_123")
if result["success"]:
    messages = result["result"]
    print(f"Retrieved {len(messages)} messages")
else:
    print(f"Email operation failed: {result['error']}")
```

### Email Processing Best Practices

```python
class EmailManager:
    """Best practices for email management"""
    
    def __init__(self, client, llm=None):
        self.client = client
        self.llm = llm
        self.processed_emails = set()  # Track processed emails
    
    def batch_process_emails(self, agent_id, batch_size=10):
        """Process emails in batches to avoid overload"""
        
        messages = self.client.email.read_inbox(agent_id)
        
        # Process in batches
        for i in range(0, len(messages), batch_size):
            batch = messages[i:i + batch_size]
            
            for message in batch:
                message_id = message.get('id', hash(message.get('subject', '')))
                
                if message_id in self.processed_emails:
                    continue
                
                try:
                    self.process_single_email(agent_id, message)
                    self.processed_emails.add(message_id)
                except Exception as e:
                    print(f"Failed to process email {message_id}: {e}")
    
    def process_single_email(self, agent_id, message):
        """Process a single email with full error handling"""
        
        sender = message.get('from', '')
        subject = message.get('subject', '')
        content = message.get('text_body', '')
        
        print(f"Processing email from {sender}: {subject}")
        
        # Add your processing logic here
        if self.llm:
            summary = self.llm.invoke(f"Summarize: {content}").content
            print(f"Summary: {summary}")
    
    def cleanup_old_emails(self, days=30):
        """Clean up old processed email records"""
        # In a real implementation, you'd clean up old entries
        # based on timestamps
        pass

# Usage
email_manager = EmailManager(client, llm)
email_manager.batch_process_emails("child_agent_123")
```

## API Reference

### EmailClient Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `read_inbox()` | Read email inbox for agent | agent_id | List[Dict] |
| `send_email()` | Send email from agent | agent_id, recipient, subject, body | Dict |

### EmailSummarizerTool

| Property | Description | Type |
|----------|-------------|------|
| `name` | Tool identifier | str |
| `description` | Tool description | str |
| `llm` | LangChain LLM instance | ChatDeepSeek |
| `client` | CirtusAI client instance | CirtusAIClient |
| `agent_id` | Agent ID for email access | str |
| `username` | Authentication username | str |
| `password` | Authentication password | str |

### Email Message Structure

```python
{
    "id": "message_123",
    "from": "sender@example.com",
    "to": "recipient@example.com",
    "subject": "Email Subject",
    "text_body": "Email content...",
    "html_body": "<html>Email content...</html>",
    "date": "2024-01-15T10:30:00Z",
    "attachments": [],
    "processed": false
}
```

### Required Permissions

- `email:read` - Required to read inbox
- `email:send` - Required to send emails

### LangChain Integration

The email system integrates seamlessly with LangChain for advanced AI processing:

```python
from langchain_core.tools import BaseTool
from langchain_deepseek import ChatDeepSeek

# The EmailSummarizerTool extends BaseTool
# and can be used in LangChain agent workflows
```
