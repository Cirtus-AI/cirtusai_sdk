from typing import Dict, Any, List, Optional
from requests import Session
import io

class MonitoringClient:
    def __init__(self, session: Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def watch_address(self, address: str, chain: str, provider: str = "blocknative") -> Dict[str, Any]:
        """Watch a given address on a specific chain for real-time transaction updates."""
        url = f"{self.base_url}/monitoring/watch-address"
        params = {"address": address, "chain": chain, "provider": provider}
        response = self.session.post(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_tx_status(self, tx_hash: str, provider: str = "blocknative") -> Dict[str, Any]:
        """Get the status of a transaction from the specified monitoring provider."""
        url = f"{self.base_url}/monitoring/tx-status/{tx_hash}"
        params = {"provider": provider}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_transaction_status(self, tx_hash: str, provider: str = "blocknative") -> Dict[str, Any]:
        """Alias for get_tx_status, matching SDK naming."""
        return self.get_tx_status(tx_hash, provider)
    
    def list_watches(self) -> List[Dict[str, Any]]:
        """List all active address watches."""
        url = f"{self.base_url}/monitoring/watches"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()
    
    def get_alerts(self) -> List[Dict[str, Any]]:
        """Retrieve all generated alerts."""
        url = f"{self.base_url}/monitoring/alerts"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

class ComplianceClient:
    """
    Advanced compliance client with enterprise-grade features:
    - Webhook persistence & retry logic
    - Asynchronous processing with task tracking
    - Tamper-evident audit logging
    - Rate limiting & permission enforcement
    """
    
    def __init__(self, session: Session, base_url: str):
        self.session = session
        self.base_url = base_url

    # Core KYC Operations
    def get_kyc_status(self) -> Dict[str, Any]:
        """Get the KYC status for the current user."""
        url = f"{self.base_url}/compliance/kyc-status"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def initiate_kyc(self) -> Dict[str, Any]:
        """Initiate the KYC verification flow for the current user."""
        url = f"{self.base_url}/compliance/initiate-kyc"
        response = self.session.post(url)
        response.raise_for_status()
        return response.json()

    def auto_submit_kyc(self) -> Dict[str, Any]:
        """One-click auto-submit KYC: pull docs from S3, OCR, and submit for KYC."""
        url = f"{self.base_url}/compliance/auto-submit-kyc"
        response = self.session.post(url)
        response.raise_for_status()
        return response.json()

    def bulk_auto_submit_kyc(self, user_ids: List[str]) -> Dict[str, Any]:
        """
        Bulk one-click KYC: process multiple user IDs asynchronously.
        Returns task ID for tracking progress.
        """
        url = f"{self.base_url}/compliance/bulk-auto-submit-kyc"
        payload = {"user_ids": user_ids}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    # Document Processing
    def process_document(self, document_file, document_type: str) -> Dict[str, Any]:
        """
        Process KYC document asynchronously with OCR and validation.
        
        Args:
            document_file: File-like object or bytes of the document
            document_type: Type of document (passport, drivers_license, utility_bill, etc.)
        
        Returns:
            Dict with task_id for tracking processing status
        """
        url = f"{self.base_url}/compliance/process-document"
        
        # Handle different input types
        if isinstance(document_file, bytes):
            files = {"document": ("document.pdf", io.BytesIO(document_file))}
        elif hasattr(document_file, 'read'):
            files = {"document": document_file}
        else:
            raise ValueError("document_file must be bytes or file-like object")
        
        data = {"document_type": document_type}
        response = self.session.post(url, files=files, data=data)
        response.raise_for_status()
        return response.json()

    # Webhook Management
    def submit_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a webhook event for KYC provider callbacks."""
        url = f"{self.base_url}/compliance/kyc-webhook"
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_webhook_statistics(self) -> Dict[str, Any]:
        """
        Get webhook processing statistics.
        Requires compliance:webhook_admin permission.
        """
        url = f"{self.base_url}/compliance/webhook-statistics"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def retry_failed_webhooks(self, max_retries: int = 3) -> Dict[str, Any]:
        """
        Manually retry failed webhook events.
        Requires compliance:webhook_admin permission.
        """
        url = f"{self.base_url}/compliance/webhook-retry"
        params = {"max_retries": max_retries}
        response = self.session.post(url, params=params)
        response.raise_for_status()
        return response.json()

    # Audit Trail & Integrity
    def get_audit_trail(self, 
                       user_id: Optional[str] = None,
                       action: Optional[str] = None, 
                       start_date: Optional[str] = None,
                       end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get filtered audit trail for compliance reporting.
        
        Args:
            user_id: Filter by user ID (optional)
            action: Filter by action type (optional)
            start_date: Start date in ISO format (optional)
            end_date: End date in ISO format (optional)
        
        Returns:
            List of audit log entries with timestamps and metadata
        """
        url = f"{self.base_url}/compliance/audit-trail"
        params = {}
        if user_id:
            params["user_id"] = user_id
        if action:
            params["action"] = action
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def verify_audit_integrity(self) -> Dict[str, Any]:
        """
        Verify the integrity of the audit log chain.
        Requires compliance:audit_admin permission.
        
        Returns:
            Dict with audit_chain_valid boolean and verification timestamp
        """
        url = f"{self.base_url}/compliance/audit-integrity"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    # Legacy Methods (for backward compatibility)
    def generate_report(self, start_date: str, end_date: str, report_type: str) -> Dict[str, Any]:
        """Generate a compliance report over a date range."""
        url = f"{self.base_url}/compliance/report"
        params = {"start_date": start_date, "end_date": end_date, "report_type": report_type}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def get_audit_trail_legacy(self, entity_id: str, entity_type: str) -> Dict[str, Any]:
        """
        Retrieve audit trail for a given entity (legacy method).
        Use get_audit_trail() for enhanced filtering capabilities.
        """
        url = f"{self.base_url}/compliance/audit/{entity_type}/{entity_id}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    # Task Tracking Utilities
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of an async compliance task.
        Note: This would typically be part of a general task management system.
        """
        # This might be implemented as part of a general task API
        # For now, we'll provide a placeholder
        raise NotImplementedError("Task status tracking not yet implemented in backend API")

    # Rate Limiting Information
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """
        Get current rate limiting status for the user.
        Note: Rate limiting information is typically in response headers.
        """
        # Rate limiting info is usually in headers, not a dedicated endpoint
        # This is a utility method to help developers understand their limits
        raise NotImplementedError("Rate limit status endpoint not implemented")

class AdvancedComplianceClient(ComplianceClient):
    """
    Extended compliance client with additional enterprise features.
    Provides enhanced methods for enterprise compliance workflows.
    """
    
    def __init__(self, session: Session, base_url: str):
        super().__init__(session, base_url)
        
    def bulk_document_processing(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process multiple documents in batch.
        
        Args:
            documents: List of dicts with 'file', 'document_type', and optional 'user_id'
        
        Returns:
            List of task IDs for each document processing job
        """
        results = []
        for doc in documents:
            try:
                result = self.process_document(doc['file'], doc['document_type'])
                results.append({
                    'success': True,
                    'task_id': result.get('task_id'),
                    'document_type': doc['document_type']
                })
            except Exception as e:
                results.append({
                    'success': False,
                    'error': str(e),
                    'document_type': doc['document_type']
                })
        return results
    
    def compliance_dashboard_data(self) -> Dict[str, Any]:
        """
        Get comprehensive compliance dashboard data.
        Combines multiple API calls into a single dashboard view.
        """
        try:
            # Gather data from multiple endpoints
            kyc_status = self.get_kyc_status()
            audit_trail = self.get_audit_trail()  # Recent entries
            
            # Try to get webhook stats (admin only)
            webhook_stats = None
            try:
                webhook_stats = self.get_webhook_statistics()
            except:
                pass  # User may not have admin permissions
            
            # Try to get audit integrity (admin only)
            audit_integrity = None
            try:
                audit_integrity = self.verify_audit_integrity()
            except:
                pass  # User may not have admin permissions
            
            return {
                'kyc_status': kyc_status,
                'recent_audit_entries': audit_trail[-10:] if audit_trail else [],
                'webhook_statistics': webhook_stats,
                'audit_integrity': audit_integrity
            }
        except Exception as e:
            return {'error': str(e)}
    
    def export_compliance_data(self, format: str = 'json', **filters) -> Dict[str, Any]:
        """
        Export compliance data in various formats.
        
        Args:
            format: Export format ('json', 'csv', 'pdf')
            **filters: Filters to apply to audit trail export
        
        Returns:
            Exported data or download information
        """
        if format not in ['json', 'csv', 'pdf']:
            raise ValueError("Format must be 'json', 'csv', or 'pdf'")
        
        # Get audit trail with filters
        audit_data = self.get_audit_trail(**filters)
        
        if format == 'json':
            return {'data': audit_data, 'format': 'json'}
        else:
            # For CSV and PDF, we'd typically trigger a backend export job
            # For now, return the data with format indication
            return {
                'data': audit_data, 
                'format': format,
                'note': f'{format.upper()} export would be processed by backend'
            }
