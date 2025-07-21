# CirtusAI SDK Security & Compliance Guide

## Overview

The CirtusAI SDK provides comprehensive security and compliance features including transaction monitoring, KYC verification, audit trails, compliance reporting, and regulatory adherence tools. The security system integrates with multiple providers and offers enterprise-grade compliance management.

## Features

- **Transaction Monitoring**: Real-time blockchain transaction surveillance
- **KYC/AML Compliance**: Identity verification and anti-money laundering checks
- **Audit Trails**: Comprehensive activity logging and integrity verification
- **Compliance Reporting**: Automated regulatory report generation
- **Document Processing**: AI-powered compliance document analysis
- **Webhook Management**: Real-time compliance event notifications
- **Risk Assessment**: Automated risk scoring and alerts

## Transaction Monitoring

### Address Monitoring

```python
from cirtusai import CirtusAIClient

client = CirtusAIClient("https://api.cirtusai.com")
client.set_token("your_access_token")

# Watch specific address for suspicious activity
watch_result = client.security.watch_address(
    address="0x742d35Cc6635C0532925a3b8D",
    chain="ethereum",
    provider="blocknative"
)

print(f"Watch ID: {watch_result['watch_id']}")
print(f"Status: {watch_result['status']}")
print(f"Alert threshold: {watch_result['alert_threshold']}")

# List all active watches
watches = client.security.list_watches()
for watch in watches:
    print(f"Watch ID: {watch['watch_id']}")
    print(f"Address: {watch['address']}")
    print(f"Chain: {watch['chain']}")
    print(f"Status: {watch['status']}")
```

### Transaction Status Monitoring

```python
# Get transaction status and risk assessment
tx_status = client.security.get_tx_status(
    tx_hash="0x1234567890abcdef",
    provider="blocknative"
)

print(f"Transaction status: {tx_status['status']}")
print(f"Risk score: {tx_status['risk_score']}")
print(f"AML alerts: {tx_status['aml_alerts']}")

# Alternative method
status = client.security.get_transaction_status("0x1234567890abcdef")
print(f"Confirmation status: {status}")
```

### Security Alerts

```python
# Get security alerts for monitored addresses
alerts = client.security.get_alerts()
for alert in alerts:
    print(f"Alert ID: {alert['alert_id']}")
    print(f"Type: {alert['alert_type']}")
    print(f"Severity: {alert['severity']}")
    print(f"Address: {alert['address']}")
    print(f"Description: {alert['description']}")
    print(f"Timestamp: {alert['timestamp']}")
```

## KYC/AML Compliance

### KYC Status Management

```python
# Check current KYC status
kyc_status = client.security.get_kyc_status()
print(f"KYC Status: {kyc_status['status']}")
print(f"Verification level: {kyc_status['verification_level']}")
print(f"Required documents: {kyc_status['required_documents']}")

# Initiate KYC process
kyc_init = client.security.initiate_kyc()
print(f"KYC session ID: {kyc_init['session_id']}")
print(f"Upload URL: {kyc_init['upload_url']}")
print(f"Instructions: {kyc_init['instructions']}")
```

### Automated KYC Processing

```python
# Auto-submit KYC for single user
auto_kyc = client.security.auto_submit_kyc()
print(f"Submission status: {auto_kyc['status']}")
print(f"Processing time: {auto_kyc['estimated_processing_time']}")

# Bulk auto-submit KYC for multiple users
user_ids = ["user_123", "user_456", "user_789"]
bulk_kyc = client.security.bulk_auto_submit_kyc(user_ids)
print(f"Batch ID: {bulk_kyc['batch_id']}")
print(f"Submitted: {bulk_kyc['submitted_count']}")
print(f"Failed: {bulk_kyc['failed_count']}")
```

### Document Processing

```python
# Process compliance document
with open("passport.pdf", "rb") as doc_file:
    document_result = client.security.process_document(
        document_file=doc_file,
        document_type="passport"
    )

print(f"Document ID: {document_result['document_id']}")
print(f"Verification status: {document_result['verification_status']}")
print(f"Extracted data: {document_result['extracted_data']}")
print(f"Confidence score: {document_result['confidence_score']}")

# Bulk document processing
documents = [
    {"file": "passport.pdf", "type": "passport"},
    {"file": "utility_bill.pdf", "type": "proof_of_address"},
    {"file": "bank_statement.pdf", "type": "proof_of_income"}
]

bulk_results = client.security.bulk_document_processing(documents)
for result in bulk_results:
    print(f"Document: {result['document_type']}")
    print(f"Status: {result['verification_status']}")
    print(f"Issues: {result.get('issues', 'None')}")
```

## Audit Trail Management

### Comprehensive Audit Logging

```python
# Get detailed audit trail
audit_trail = client.security.get_audit_trail(
    start_date="2024-01-01",
    end_date="2024-01-31",
    entity_types=["user", "transaction", "document"],
    action_types=["create", "update", "delete", "verify"],
    user_ids=["user_123"],
    limit=100
)

print(f"Total entries: {len(audit_trail['entries'])}")
for entry in audit_trail['entries']:
    print(f"Timestamp: {entry['timestamp']}")
    print(f"Action: {entry['action_type']}")
    print(f"Entity: {entry['entity_type']} - {entry['entity_id']}")
    print(f"User: {entry['user_id']}")
    print(f"Details: {entry['details']}")
```

### Audit Integrity Verification

```python
# Verify audit trail integrity
integrity_check = client.security.verify_audit_integrity()
print(f"Integrity status: {integrity_check['status']}")
print(f"Total entries checked: {integrity_check['entries_checked']}")
print(f"Hash verification: {integrity_check['hash_verification']}")
print(f"Timestamp verification: {integrity_check['timestamp_verification']}")

if integrity_check['issues']:
    print("Integrity issues found:")
    for issue in integrity_check['issues']:
        print(f"  - {issue['type']}: {issue['description']}")
```

### Legacy Audit Trail Access

```python
# Access legacy audit trail for specific entity
legacy_audit = client.security.get_audit_trail_legacy(
    entity_id="transaction_123",
    entity_type="transaction"
)

print(f"Entity: {legacy_audit['entity_id']}")
print(f"Audit entries: {len(legacy_audit['audit_entries'])}")
for entry in legacy_audit['audit_entries']:
    print(f"  {entry['timestamp']}: {entry['action']} by {entry['user_id']}")
```

## Compliance Reporting

### Automated Report Generation

```python
# Generate compliance report
report = client.security.generate_report(
    start_date="2024-01-01",
    end_date="2024-01-31",
    report_type="aml_summary"
)

print(f"Report ID: {report['report_id']}")
print(f"Status: {report['status']}")
print(f"Download URL: {report['download_url']}")
print(f"Expires: {report['expires_at']}")

# Available report types: "aml_summary", "kyc_status", "transaction_monitoring", "risk_assessment"
```

### Compliance Dashboard

```python
# Get compliance dashboard data
dashboard = client.security.compliance_dashboard_data()

print(f"KYC Statistics:")
print(f"  - Verified users: {dashboard['kyc_stats']['verified_users']}")
print(f"  - Pending verification: {dashboard['kyc_stats']['pending_verification']}")
print(f"  - Rejected applications: {dashboard['kyc_stats']['rejected']}")

print(f"Transaction Monitoring:")
print(f"  - Transactions monitored: {dashboard['monitoring_stats']['transactions_monitored']}")
print(f"  - Alerts generated: {dashboard['monitoring_stats']['alerts_generated']}")
print(f"  - High-risk transactions: {dashboard['monitoring_stats']['high_risk_transactions']}")

print(f"Compliance Score: {dashboard['compliance_score']}/100")
```

### Data Export

```python
# Export compliance data
export_result = client.security.export_compliance_data(
    format="json",  # or "csv", "xml"
    date_range={"start": "2024-01-01", "end": "2024-01-31"},
    data_types=["kyc", "transactions", "audit_logs"],
    include_pii=False  # Exclude personally identifiable information
)

print(f"Export ID: {export_result['export_id']}")
print(f"Download URL: {export_result['download_url']}")
print(f"File size: {export_result['file_size_mb']} MB")
```

## Webhook Management

### Webhook Configuration

```python
# Submit webhook for compliance events
webhook_payload = {
    "event_type": "kyc_status_change",
    "user_id": "user_123",
    "old_status": "pending",
    "new_status": "verified",
    "timestamp": "2024-01-15T10:30:00Z",
    "verification_details": {
        "documents_verified": ["passport", "proof_of_address"],
        "risk_score": 15
    }
}

webhook_result = client.security.submit_webhook(webhook_payload)
print(f"Webhook submitted: {webhook_result['webhook_id']}")
print(f"Status: {webhook_result['status']}")
```

### Webhook Analytics

```python
# Get webhook statistics
webhook_stats = client.security.get_webhook_statistics()
print(f"Total webhooks: {webhook_stats['total_webhooks']}")
print(f"Successful deliveries: {webhook_stats['successful_deliveries']}")
print(f"Failed deliveries: {webhook_stats['failed_deliveries']}")
print(f"Average response time: {webhook_stats['avg_response_time_ms']}ms")

# Retry failed webhooks
retry_result = client.security.retry_failed_webhooks(max_retries=3)
print(f"Retried webhooks: {retry_result['retried_count']}")
print(f"Successful retries: {retry_result['successful_retries']}")
```

## Task Management

### Asynchronous Task Monitoring

```python
# Get status of long-running compliance tasks
task_status = client.security.get_task_status("task_123")
print(f"Task ID: {task_status['task_id']}")
print(f"Status: {task_status['status']}")
print(f"Progress: {task_status['progress']}%")
print(f"Started: {task_status['started_at']}")
if task_status['status'] == 'completed':
    print(f"Result: {task_status['result']}")
```

### Rate Limiting

```python
# Check API rate limit status
rate_limit = client.security.get_rate_limit_status()
print(f"Remaining requests: {rate_limit['remaining_requests']}")
print(f"Reset time: {rate_limit['reset_time']}")
print(f"Rate limit window: {rate_limit['window_seconds']} seconds")

if rate_limit['remaining_requests'] < 10:
    print("Warning: Approaching rate limit")
```

## Advanced Security Workflows

### Comprehensive Risk Assessment

```python
def perform_risk_assessment(client, address, transaction_history_days=30):
    """Perform comprehensive risk assessment for an address"""
    
    # Start monitoring the address
    watch_result = client.security.watch_address(
        address=address,
        chain="ethereum"
    )
    
    # Get recent alerts
    alerts = client.security.get_alerts()
    address_alerts = [alert for alert in alerts if alert.get('address') == address]
    
    # Calculate risk score
    risk_factors = {
        "alert_count": len(address_alerts),
        "high_severity_alerts": len([a for a in address_alerts if a.get('severity') == 'high']),
        "monitoring_duration": transaction_history_days
    }
    
    # Generate risk assessment report
    risk_score = min(100, (risk_factors["alert_count"] * 10) + (risk_factors["high_severity_alerts"] * 25))
    
    assessment = {
        "address": address,
        "risk_score": risk_score,
        "risk_level": "high" if risk_score > 70 else "medium" if risk_score > 30 else "low",
        "factors": risk_factors,
        "alerts": address_alerts,
        "watch_id": watch_result.get('watch_id')
    }
    
    return assessment

# Usage
risk_assessment = perform_risk_assessment(
    client, 
    "0x742d35Cc6635C0532925a3b8D",
    transaction_history_days=60
)

print(f"Risk Assessment for {risk_assessment['address']}:")
print(f"Risk Score: {risk_assessment['risk_score']}/100")
print(f"Risk Level: {risk_assessment['risk_level'].upper()}")
```

### Automated Compliance Workflow

```python
def automated_compliance_check(client, user_id):
    """Automated compliance verification workflow"""
    
    workflow_results = {
        "user_id": user_id,
        "kyc_status": None,
        "document_verification": None,
        "risk_assessment": None,
        "compliance_score": 0
    }
    
    try:
        # Step 1: Check KYC status
        kyc_status = client.security.get_kyc_status()
        workflow_results["kyc_status"] = kyc_status
        
        if kyc_status['status'] == 'not_started':
            # Initiate KYC if not started
            kyc_init = client.security.initiate_kyc()
            workflow_results["kyc_initiated"] = kyc_init
        
        # Step 2: Auto-submit KYC if applicable
        if kyc_status['status'] in ['pending', 'documents_required']:
            auto_kyc = client.security.auto_submit_kyc()
            workflow_results["auto_kyc"] = auto_kyc
        
        # Step 3: Get audit trail for user
        audit_trail = client.security.get_audit_trail(
            user_ids=[user_id],
            limit=50
        )
        workflow_results["audit_entries"] = len(audit_trail.get('entries', []))
        
        # Step 4: Calculate compliance score
        score = 0
        if kyc_status['status'] == 'verified':
            score += 50
        if workflow_results["audit_entries"] > 0:
            score += 20
        if kyc_status.get('verification_level') == 'enhanced':
            score += 30
        
        workflow_results["compliance_score"] = score
        
    except Exception as e:
        workflow_results["error"] = str(e)
    
    return workflow_results

# Usage
compliance_check = automated_compliance_check(client, "user_123")
print(f"Compliance Score: {compliance_check['compliance_score']}/100")
```

### Regulatory Reporting Pipeline

```python
def generate_regulatory_reports(client, reporting_period):
    """Generate all required regulatory reports for a period"""
    
    report_types = [
        "aml_summary",
        "kyc_status", 
        "transaction_monitoring",
        "risk_assessment"
    ]
    
    generated_reports = []
    
    for report_type in report_types:
        try:
            report = client.security.generate_report(
                start_date=reporting_period["start"],
                end_date=reporting_period["end"],
                report_type=report_type
            )
            
            generated_reports.append({
                "type": report_type,
                "report_id": report["report_id"],
                "status": report["status"],
                "download_url": report.get("download_url")
            })
            
            print(f"Generated {report_type} report: {report['report_id']}")
            
        except Exception as e:
            print(f"Failed to generate {report_type} report: {e}")
    
    # Export compliance data
    try:
        export = client.security.export_compliance_data(
            format="json",
            date_range=reporting_period,
            data_types=["kyc", "transactions", "audit_logs"]
        )
        
        generated_reports.append({
            "type": "data_export",
            "export_id": export["export_id"],
            "download_url": export["download_url"],
            "file_size_mb": export["file_size_mb"]
        })
        
    except Exception as e:
        print(f"Failed to export compliance data: {e}")
    
    return generated_reports

# Usage
reporting_period = {
    "start": "2024-01-01",
    "end": "2024-01-31"
}

reports = generate_regulatory_reports(client, reporting_period)
print(f"Generated {len(reports)} reports and exports")
```

## Error Handling and Best Practices

### Robust Error Handling

```python
def safe_compliance_operation(client, operation, *args, **kwargs):
    """Safely execute compliance operations with proper error handling"""
    
    try:
        result = getattr(client.security, operation)(*args, **kwargs)
        return {"success": True, "result": result}
    
    except requests.exceptions.HTTPError as e:
        error_code = e.response.status_code
        error_detail = e.response.json().get("detail", str(e))
        
        if error_code == 403:
            return {"success": False, "error": "Insufficient permissions for compliance operation"}
        elif error_code == 429:
            return {"success": False, "error": "Rate limit exceeded", "retry_after": e.response.headers.get("Retry-After")}
        else:
            return {"success": False, "error": f"HTTP {error_code}: {error_detail}"}
    
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}

# Usage
result = safe_compliance_operation(client, "get_kyc_status")
if result["success"]:
    print(f"KYC Status: {result['result']['status']}")
else:
    print(f"Operation failed: {result['error']}")
```

### Compliance Monitoring Best Practices

```python
class ComplianceMonitor:
    """Best practices for compliance monitoring"""
    
    def __init__(self, client):
        self.client = client
    
    def setup_monitoring(self, addresses):
        """Setup comprehensive monitoring for multiple addresses"""
        watch_ids = []
        
        for address in addresses:
            try:
                watch = self.client.security.watch_address(
                    address=address,
                    chain="ethereum"
                )
                watch_ids.append(watch['watch_id'])
                print(f"Monitoring setup for {address}: {watch['watch_id']}")
            except Exception as e:
                print(f"Failed to setup monitoring for {address}: {e}")
        
        return watch_ids
    
    def daily_compliance_check(self):
        """Daily compliance status check"""
        alerts = self.client.security.get_alerts()
        high_priority = [a for a in alerts if a.get('severity') == 'high']
        
        if high_priority:
            print(f"⚠️  {len(high_priority)} high-priority alerts found!")
            for alert in high_priority:
                print(f"   - {alert['alert_type']}: {alert['description']}")
        
        # Check webhook delivery status
        webhook_stats = self.client.security.get_webhook_statistics()
        failure_rate = (webhook_stats['failed_deliveries'] / webhook_stats['total_webhooks']) * 100
        
        if failure_rate > 5:  # 5% failure threshold
            print(f"⚠️  High webhook failure rate: {failure_rate:.1f}%")
            # Retry failed webhooks
            self.client.security.retry_failed_webhooks()
    
    def monthly_audit(self):
        """Monthly compliance audit"""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        # Generate comprehensive audit trail
        audit = self.client.security.get_audit_trail(
            start_date=start_date,
            end_date=end_date,
            limit=1000
        )
        
        # Verify audit integrity
        integrity = self.client.security.verify_audit_integrity()
        
        # Generate compliance reports
        reports = generate_regulatory_reports(self.client, {
            "start": start_date,
            "end": end_date
        })
        
        return {
            "audit_entries": len(audit.get('entries', [])),
            "integrity_status": integrity['status'],
            "reports_generated": len(reports)
        }

# Usage
monitor = ComplianceMonitor(client)
monitor.daily_compliance_check()
```

## API Reference

### SecurityClient Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `watch_address()` | Monitor address for suspicious activity | address, chain, provider | Dict |
| `get_tx_status()` | Get transaction status and risk assessment | tx_hash, provider | Dict |
| `get_transaction_status()` | Get transaction confirmation status | tx_hash, provider | Dict |
| `list_watches()` | List all active address watches | - | List[Dict] |
| `get_alerts()` | Get security alerts | - | List[Dict] |
| `get_kyc_status()` | Get KYC verification status | - | Dict |
| `initiate_kyc()` | Start KYC verification process | - | Dict |
| `auto_submit_kyc()` | Auto-submit KYC for current user | - | Dict |
| `bulk_auto_submit_kyc()` | Bulk auto-submit KYC | user_ids | Dict |
| `process_document()` | Process compliance document | document_file, document_type | Dict |
| `submit_webhook()` | Submit compliance webhook | payload | Dict |
| `get_webhook_statistics()` | Get webhook delivery stats | - | Dict |
| `retry_failed_webhooks()` | Retry failed webhook deliveries | max_retries | Dict |
| `get_audit_trail()` | Get comprehensive audit trail | start_date, end_date, filters | Dict |
| `verify_audit_integrity()` | Verify audit trail integrity | - | Dict |
| `generate_report()` | Generate compliance report | start_date, end_date, report_type | Dict |
| `get_audit_trail_legacy()` | Get legacy audit trail | entity_id, entity_type | Dict |
| `get_task_status()` | Get async task status | task_id | Dict |
| `get_rate_limit_status()` | Get API rate limit status | - | Dict |
| `bulk_document_processing()` | Process multiple documents | documents | List[Dict] |
| `compliance_dashboard_data()` | Get compliance dashboard data | - | Dict |
| `export_compliance_data()` | Export compliance data | format, filters | Dict |

### Compliance Data Models

#### KYC Status Response
```json
{
    "status": "verified" | "pending" | "not_started" | "rejected",
    "verification_level": "basic" | "enhanced",
    "required_documents": ["passport", "proof_of_address"],
    "submission_date": "2024-01-15T10:30:00Z",
    "verification_date": "2024-01-16T14:20:00Z"
}
```

#### Security Alert
```json
{
    "alert_id": "alert_123",
    "alert_type": "suspicious_transaction" | "high_value_transfer" | "blacklist_match",
    "severity": "low" | "medium" | "high" | "critical",
    "address": "0x742d35Cc6635C0532925a3b8D",
    "description": "Large transaction to high-risk address",
    "timestamp": "2024-01-15T10:30:00Z",
    "risk_score": 85
}
```
