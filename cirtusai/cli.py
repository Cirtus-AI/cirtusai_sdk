import os
import json
import click
from .client import CirtusAIClient

@click.group()
@click.option('--api-url', default=lambda: os.getenv('CIRTUSAI_API_URL', 'http://localhost:8000'), help='Base URL for CirtusAI API')
@click.option('--token', envvar='CIRTUSAI_TOKEN', help='JWT access token')
@click.option('--agent-id', envvar='CIRTUSAI_AGENT_ID', help='Child agent ID for asset provisioning and agent-specific commands')
@click.pass_context
def main(ctx, api_url, token, agent_id):
    """CirtusAI SDK CLI"""
    client = CirtusAIClient(api_url, token=token)
    ctx.obj = {'client': client, 'agent_id': agent_id}

# Authentication commands
@main.group()
@click.pass_context
def auth(ctx):
    """Authentication commands"""

@auth.command()
@click.argument('email')
@click.argument('password')
@click.pass_context
def login(ctx, email, password):
    """Login and obtain access token"""
    result = ctx.obj['client'].auth.login(email, password)
    output = result.dict() if hasattr(result, 'dict') else result
    click.echo(json.dumps(output, indent=2))

@auth.command()
@click.argument('username')
@click.argument('email')
@click.argument('password')
@click.option('--2fa-method', 'two_fa_method', default='totp', help='Preferred 2FA method')
@click.pass_context
def register(ctx, username, email, password, two_fa_method):
    """Register a new user and setup 2FA"""
    result = ctx.obj['client'].auth.register(username, email, password, preferred_2fa_method=two_fa_method)
    click.echo(json.dumps(result.dict(), indent=2))

@auth.command()
@click.argument('refresh_token')
@click.pass_context
def refresh(ctx, refresh_token):
    """Refresh access token"""
    result = ctx.obj['client'].auth.refresh(refresh_token)
    click.echo(json.dumps(result, indent=2))

@auth.command(name='verify-2fa')
@click.argument('temporary_token')
@click.argument('totp_code')
@click.pass_context
def verify_2fa(ctx, temporary_token, totp_code):
    """Verify TOTP code and complete login"""
    result = ctx.obj['client'].auth.verify_2fa(temporary_token, totp_code)
    click.echo(json.dumps(result, indent=2))

# Agent management commands
@main.group()
@click.pass_context
def agents(ctx):
    """Agent management commands"""

@agents.command(name='list')
@click.pass_context
def list_agents(ctx):
    """List master agents"""
    # compact JSON output for list
    click.echo(json.dumps(ctx.obj['client'].agents.list_agents()))

@agents.command()
@click.argument('agent_id')
@click.pass_context
def get(ctx, agent_id):
    """Get agent details"""
    # compact JSON output for get
    click.echo(json.dumps(ctx.obj['client'].agents.get_agent(agent_id)))

@agents.command(name='create-child')
@click.argument('parent_id')
@click.argument('name')
@click.pass_context
def create_child(ctx, parent_id, name):
    """Create a child agent"""
    click.echo(json.dumps(ctx.obj['client'].agents.create_child_agent(parent_id, name), indent=2))

@agents.command(name='delete')
@click.argument('agent_id')
@click.pass_context
def delete(ctx, agent_id):
    """Delete an agent"""
    ctx.obj['client'].agents.delete_agent(agent_id)
    click.echo(f"Agent {agent_id} deleted.")

@agents.command(name='children')
@click.pass_context
def list_children(ctx):
    """List child agents"""
    # compact JSON output for children list
    click.echo(json.dumps(ctx.obj['client'].agents.get_children()))

@agents.command(name='provision-email')
@click.argument('child_id', required=False)
@click.pass_context
def provision_email(ctx, child_id):
    """Provision email asset for a child agent"""
    cid = child_id or ctx.obj['agent_id']
    click.echo(json.dumps(ctx.obj['client'].agents.provision_email(cid), indent=2))

@agents.command(name='provision-wallet')
@click.argument('child_id', required=False)
@click.option('--chain', default='ethereum')
@click.pass_context
def provision_wallet(ctx, child_id, chain):
    """Provision wallet asset for a child agent"""
    cid = child_id or ctx.obj['agent_id']
    click.echo(json.dumps(ctx.obj['client'].agents.provision_wallet(cid, chain), indent=2))

@agents.command(name='update-permissions')
@click.argument('child_id')
@click.argument('permissions')
@click.pass_context
def update_permissions(ctx, child_id, permissions):
    """Update permissions for a child agent (comma-separated list)"""
    # permissions is a JSON string; parse to dict
    try:
        perms_dict = json.loads(permissions)
    except json.JSONDecodeError:
        raise click.BadParameter('permissions must be a valid JSON object')
    result = ctx.obj['client'].agents.update_child_permissions(child_id, perms_dict)
    # compact JSON output
    click.echo(json.dumps(result))

@agents.command(name='unlink')
@click.argument('child_id')
@click.pass_context
def unlink(ctx, child_id):
    """Unlink a child agent"""
    ctx.obj['client'].agents.unlink_child_agent(child_id)
    # match expected CLI test message
    click.echo(f"Unlinked child agent {child_id}")
    
@main.group()
@click.pass_context
def compliance(ctx):
    """Compliance commands (KYC etc.)"""

@compliance.command(name='get-kyc-status')
@click.pass_context
def get_kyc_status(ctx):
    """Get KYC status for the current user"""
    click.echo(json.dumps(ctx.obj['client'].compliance.get_kyc_status(), indent=2))

@compliance.command(name='initiate-kyc')
@click.pass_context
def cli_initiate_kyc(ctx):
    """Initiate the KYC verification flow for the current user"""
    click.echo(json.dumps(ctx.obj['client'].compliance.initiate_kyc(), indent=2))

@compliance.command(name='auto-submit-kyc')
@click.pass_context
def auto_submit_kyc(ctx):
    """One-click KYC: pull docs from S3, OCR, and submit for KYC"""
    click.echo(json.dumps(ctx.obj['client'].compliance.auto_submit_kyc(), indent=2))
    
@compliance.command(name='bulk-auto-submit-kyc')
@click.argument('user_ids', type=str)
@click.pass_context
def bulk_auto_submit_kyc_cmd(ctx, user_ids):
    """Bulk one-click KYC: process multiple user IDs (comma-separated)."""
    ids = [uid.strip() for uid in user_ids.split(',')]
    click.echo(json.dumps(ctx.obj['client'].compliance.bulk_auto_submit_kyc(ids), indent=2))

# Wallet commands
@main.group()
@click.pass_context
def wallets(ctx):
    """Wallet and email account commands"""

@wallets.command(name='list-assets')
@click.pass_context
def list_assets(ctx):
    """List wallet assets"""
    click.echo(json.dumps(ctx.obj['client'].wallets.list_assets(), indent=2))

@wallets.command(name='list-email')
@click.pass_context
def list_email(ctx):
    """List email accounts"""
    click.echo(json.dumps(ctx.obj['client'].wallets.list_email_accounts(), indent=2))

@wallets.command(name='create-email')
@click.argument('provider')
@click.argument('email_address')
@click.argument('config', type=str)
@click.pass_context
def create_email(ctx, provider, email_address, config):
    """Create email account (config JSON string)"""
    cfg = json.loads(config)
    click.echo(json.dumps(ctx.obj['client'].wallets.create_email_account(provider, email_address, cfg), indent=2))

@wallets.command(name='get-email')
@click.argument('account_id')
@click.pass_context
def get_email(ctx, account_id):
    """Get email account details"""
    click.echo(json.dumps(ctx.obj['client'].wallets.get_email_account(account_id), indent=2))

@wallets.command(name='update-email')
@click.argument('account_id')
@click.argument('provider')
@click.argument('email_address')
@click.argument('config', type=str)
@click.pass_context
def update_email(ctx, account_id, provider, email_address, config):
    """Update email account (config JSON string)"""
    cfg = json.loads(config)
    click.echo(json.dumps(ctx.obj['client'].wallets.update_email_account(account_id, provider, email_address, cfg), indent=2))

@wallets.command(name='delete-email')
@click.argument('account_id')
@click.pass_context
def delete_email(ctx, account_id):
    """Delete an email account"""
    ctx.obj['client'].wallets.delete_email_account(account_id)
    click.echo(f"Email account {account_id} deleted.")

@wallets.command(name='refresh-email-token')
@click.argument('account_id')
@click.pass_context
def refresh_email_token(ctx, account_id):
    """Refresh email account token"""
    click.echo(json.dumps(ctx.obj['client'].wallets.refresh_email_token(account_id), indent=2))

@wallets.command(name='add-crypto')
@click.option('--chain', default='ethereum')
@click.pass_context
def add_crypto(ctx, chain):
    """Provision a crypto wallet asset"""
    click.echo(json.dumps(ctx.obj['client'].wallets.add_crypto(chain), indent=2))

# Identity commands
@main.group()
@click.pass_context
def identity(ctx):
    """DID and credential commands"""

@identity.command(name='get-did')
@click.argument('agent_id')
@click.pass_context
def get_did(ctx, agent_id):
    """Retrieve DID record"""
    click.echo(json.dumps(ctx.obj['client'].identity.get_did(agent_id), indent=2))

@identity.command(name='issue-credential')
@click.argument('subject_id')
@click.argument('types', type=str)
@click.argument('claim', type=str)
@click.pass_context
def issue_credential(ctx, subject_id, types, claim):
    """Issue a verifiable credential"""
    tlist = types.split(',')
    cl = json.loads(claim)
    click.echo(json.dumps(ctx.obj['client'].identity.issue_credential(subject_id, tlist, cl), indent=2))

@identity.command(name='verify-credential')
@click.argument('jwt_token')
@click.pass_context
def verify_credential(ctx, jwt_token):
    """Verify a credential token"""
    click.echo(json.dumps(ctx.obj['client'].identity.verify_credential(jwt_token), indent=2))

# Governance commands
@main.group()
@click.pass_context
def governance(ctx):
    """Governance proposal and voting commands"""

@governance.command(name='create-proposal')
@click.argument('targets', type=str)
@click.argument('values', type=str)
@click.argument('calldatas', type=str)
@click.argument('description')
@click.pass_context
def create_proposal(ctx, targets, values, calldatas, description):
    """Create a governance proposal (comma-separated lists)"""
    tgt = targets.split(',')
    vals = [int(v) for v in values.split(',')]
    data = calldatas.split(',')
    click.echo(json.dumps(ctx.obj['client'].governance.create_proposal(tgt, vals, data, description), indent=2))

@governance.command(name='cast-vote')
@click.argument('proposal_id', type=int)
@click.argument('support', type=int)
@click.pass_context
def cast_vote(ctx, proposal_id, support):
    """Cast vote on a proposal"""
    click.echo(json.dumps(ctx.obj['client'].governance.cast_vote(proposal_id, support), indent=2))

@governance.command(name='get-proposal-state')
@click.argument('proposal_id', type=int)
@click.pass_context
def proposal_state(ctx, proposal_id):
    """Get state of a proposal"""
    click.echo(json.dumps(ctx.obj['client'].governance.get_proposal_state(proposal_id), indent=2))

# Reputation commands
@main.group()
@click.pass_context
def reputation(ctx):
    """Soulbound token commands"""

@reputation.command(name='issue-sbt')
@click.argument('to_address')
@click.argument('token_uri')
@click.pass_context
def issue_sbt(ctx, to_address, token_uri):
    """Issue a soulbound token"""
    click.echo(json.dumps(ctx.obj['client'].reputation.issue_sbt(to_address, token_uri), indent=2))

@reputation.command(name='get-sbt-owner')
@click.argument('token_id', type=int)
@click.pass_context
def get_sbt_owner(ctx, token_id):
    """Get owner of a soulbound token"""
    click.echo(ctx.obj['client'].reputation.get_sbt_owner(token_id))

# Bridge and asset commands
@main.group()
@click.pass_context
def bridge(ctx):
    """Cross-chain bridge commands"""

@bridge.command(name='get-quote')
@click.argument('from_chain')
@click.argument('to_chain')
@click.argument('from_token')
@click.argument('to_token')
@click.argument('amount', type=int)
@click.pass_context
def bridge_quote(ctx, from_chain, to_chain, from_token, to_token, amount):
    """Get bridge transfer quote"""
    click.echo(json.dumps(ctx.obj['client'].bridge.get_quote(from_chain, to_chain, from_token, to_token, amount), indent=2))

@bridge.command(name='transfer')
@click.argument('provider')
@click.argument('from_chain')
@click.argument('to_chain')
@click.argument('from_token')
@click.argument('to_token')
@click.argument('amount', type=int)
@click.argument('recipient_address')
@click.pass_context
def bridge_transfer(ctx, provider, from_chain, to_chain, from_token, to_token, amount, recipient_address):
    """Execute a bridge transfer"""
    click.echo(json.dumps(ctx.obj['client'].bridge.bridge_transfer(provider, from_chain, to_chain, from_token, to_token, amount, recipient_address), indent=2))

@main.group()
@click.pass_context
def assets(ctx):
    """Multi-chain asset view commands"""

@assets.command(name='view')
@click.pass_context
def view_assets(ctx):
    """Get multi-chain asset view"""
    click.echo(json.dumps(ctx.obj['client'].assets.get_multi_chain_asset_view(), indent=2))

@assets.command(name='refresh')
@click.pass_context
def refresh_assets(ctx):
    """Refresh multi-chain asset view"""
    click.echo(json.dumps(ctx.obj['client'].assets.refresh_multi_chain_asset_view(), indent=2))

# Marketplace commands
@main.group()
@click.pass_context
def marketplace(ctx):
    """Marketplace listing and bid commands"""

@marketplace.command(name='create-listing')
@click.argument('listing_data', type=str)
@click.pass_context
def create_listing(ctx, listing_data):
    """Create a marketplace listing (JSON)"""
    data = json.loads(listing_data)
    click.echo(json.dumps(ctx.obj['client'].marketplace.create_listing(data), indent=2))

@marketplace.command(name='list-listings')
@click.argument('filters', required=False, type=str)
@click.pass_context
def list_listings(ctx, filters):
    """List marketplace listings (JSON filters)"""
    flt = json.loads(filters) if filters else {}
    click.echo(json.dumps(ctx.obj['client'].marketplace.list_listings(flt), indent=2))

@marketplace.command(name='get-listing')
@click.argument('listing_id')
@click.pass_context
def get_listing(ctx, listing_id):
    """Get a specific listing"""
    click.echo(json.dumps(ctx.obj['client'].marketplace.get_listing(listing_id), indent=2))

@marketplace.command(name='update-listing')
@click.argument('listing_id')
@click.argument('listing_data', type=str)
@click.pass_context
def update_listing(ctx, listing_id, listing_data):
    """Update a listing (JSON)"""
    data = json.loads(listing_data)
    click.echo(json.dumps(ctx.obj['client'].marketplace.update_listing(listing_id, data), indent=2))

@marketplace.command(name='cancel-listing')
@click.argument('listing_id')
@click.pass_context
def cancel_listing(ctx, listing_id):
    """Cancel a listing"""
    ctx.obj['client'].marketplace.cancel_listing(listing_id)
    click.echo(f"Listing {listing_id} canceled.")

@marketplace.command(name='place-bid')
@click.argument('listing_id')
@click.argument('bid_data', type=str)
@click.pass_context
def place_bid(ctx, listing_id, bid_data):
    """Place a bid on a listing (JSON)"""
    data = json.loads(bid_data)
    click.echo(json.dumps(ctx.obj['client'].marketplace.place_bid(listing_id, data), indent=2))

@marketplace.command(name='list-bids')
@click.argument('listing_id')
@click.pass_context
def list_bids(ctx, listing_id):
    """List bids for a listing"""
    click.echo(json.dumps(ctx.obj['client'].marketplace.list_bids(listing_id), indent=2))

@marketplace.command(name='accept-bid')
@click.argument('listing_id')
@click.argument('bid_id')
@click.pass_context
def accept_bid(ctx, listing_id, bid_id):
    """Accept a bid"""
    click.echo(json.dumps(ctx.obj['client'].marketplace.accept_bid(listing_id, bid_id), indent=2))

# Swap commands
@main.group()
@click.pass_context
def swap(ctx):
    """Token swap commands"""

@swap.command(name='get-quote')
@click.argument('from_chain')
@click.argument('to_chain')
@click.argument('from_token')
@click.argument('to_token')
@click.argument('amount', type=float)
@click.pass_context
def swap_quote(ctx, from_chain, to_chain, from_token, to_token, amount):
    """Get swap quote"""
    click.echo(json.dumps(ctx.obj['client'].swap.get_quote(from_chain, to_chain, from_token, to_token, amount), indent=2))

@swap.command(name='execute')
@click.argument('swap_data', type=str)
@click.pass_context
def execute_swap(ctx, swap_data):
    """Execute a swap (JSON)"""
    data = json.loads(swap_data)
    click.echo(json.dumps(ctx.obj['client'].swap.execute_swap(data), indent=2))

@swap.command(name='cancel')
@click.argument('swap_id')
@click.pass_context
def cancel_swap(ctx, swap_id):
    """Cancel a swap"""
    ctx.obj['client'].swap.cancel_swap(swap_id)
    click.echo(f"Swap {swap_id} canceled.")

# NFT commands
@main.group()
@click.pass_context
def nfts(ctx):
    """NFT management commands"""

@nfts.command(name='list')
@click.argument('wallet_id')
@click.pass_context
def list_nfts(ctx, wallet_id):
    """List NFTs in a wallet"""
    click.echo(json.dumps(ctx.obj['client'].nfts.list_nfts(wallet_id), indent=2))

@nfts.command(name='get-metadata')
@click.argument('contract_address')
@click.argument('token_id')
@click.pass_context
def get_metadata(ctx, contract_address, token_id):
    """Get NFT metadata"""
    click.echo(json.dumps(ctx.obj['client'].nfts.get_nft_metadata(contract_address, token_id), indent=2))

@nfts.command(name='mint')
@click.argument('contract_address')
@click.argument('to_address')
@click.argument('metadata_uri')
@click.pass_context
def mint_nft(ctx, contract_address, to_address, metadata_uri):
    """Mint a new NFT"""
    click.echo(json.dumps(ctx.obj['client'].nfts.mint_nft(contract_address, to_address, metadata_uri), indent=2))

@nfts.command(name='batch-transfer')
@click.argument('contract_address')
@click.argument('transfers')
@click.pass_context
def batch_transfer(ctx, contract_address, transfers):
    """Batch transfer NFTs (JSON list)"""
    data = json.loads(transfers)
    click.echo(json.dumps(ctx.obj['client'].nfts.batch_transfer(contract_address, data), indent=2))

@nfts.command(name='burn')
@click.argument('contract_address')
@click.argument('token_id')
@click.pass_context
def burn_nft(ctx, contract_address, token_id):
    """Burn an NFT"""
    ctx.obj['client'].nfts.burn_nft(contract_address, token_id)
    click.echo(f"NFT {contract_address}:{token_id} burned.")

# Child assets commands
@main.group()
@click.pass_context
def child_assets(ctx):
    """Child asset management commands"""

@child_assets.command(name='list')
@click.argument('child_id')
@click.pass_context
def list_child_assets(ctx, child_id):
    """List assets for a child agent"""
    click.echo(json.dumps(ctx.obj['client'].child_assets.list_child_assets(child_id), indent=2))

@child_assets.command(name='get')
@click.argument('asset_id')
@click.pass_context
def get_child_asset(ctx, asset_id):
    """Get a specific child asset"""
    click.echo(json.dumps(ctx.obj['client'].child_assets.get_child_asset(asset_id), indent=2))

@child_assets.command(name='create')
@click.argument('child_id')
@click.argument('asset_data', type=str)
@click.pass_context
def create_child_asset(ctx, child_id, asset_data):
    """Create a child asset (JSON)"""
    data = json.loads(asset_data)
    click.echo(json.dumps(ctx.obj['client'].child_assets.create_child_asset(child_id, data), indent=2))

@child_assets.command(name='update')
@click.argument('asset_id')
@click.argument('asset_data', type=str)
@click.pass_context
def update_child_asset(ctx, asset_id, asset_data):
    """Update a child asset (JSON)"""
    data = json.loads(asset_data)
    click.echo(json.dumps(ctx.obj['client'].child_assets.update_child_asset(asset_id, data), indent=2))

@child_assets.command(name='delete')
@click.argument('asset_id')
@click.pass_context
def delete_child_asset(ctx, asset_id):
    """Delete a child asset"""
    ctx.obj['client'].child_assets.delete_child_asset(asset_id)
    click.echo(f"Child asset {asset_id} deleted.")

# Child services commands
@main.group()
@click.pass_context
def child_services(ctx):
    """Child service management commands"""

@child_services.command(name='list')
@click.argument('child_id')
@click.pass_context
def list_services(ctx, child_id):
    """List services for a child agent"""
    click.echo(json.dumps(ctx.obj['client'].child_services.list_services(child_id), indent=2))

# ================================
# Compliance Commands (v0.3.0)
# ================================

@main.group()
@click.pass_context
def compliance(ctx):
    """Advanced compliance and monitoring commands"""

@compliance.command(name='kyc-check')
@click.argument('user_id')
@click.option('--identity-check', is_flag=True, help='Perform identity verification')
@click.option('--document-scan', is_flag=True, help='Scan documents for compliance')
@click.pass_context
def kyc_check(ctx, user_id, identity_check, document_scan):
    """Perform KYC verification for a user"""
    result = ctx.obj['client'].compliance.kyc_verification(
        user_id, 
        identity_check=identity_check, 
        document_scan=document_scan
    )
    click.echo(json.dumps(result, indent=2))

@compliance.command(name='process-document')
@click.argument('file_path')
@click.option('--document-type', required=True, help='Type of document (passport, driver_license, utility_bill, bank_statement)')
@click.option('--user-id', required=True, help='User ID for document association')
@click.pass_context
def process_document(ctx, file_path, document_type, user_id):
    """Process and validate compliance documents"""
    with open(file_path, 'rb') as f:
        result = ctx.obj['client'].compliance.process_document(
            f, document_type, user_id
        )
    click.echo(json.dumps(result, indent=2))

@compliance.command(name='audit-trail')
@click.option('--user-id', help='Filter by user ID')
@click.option('--action-type', help='Filter by action type')
@click.option('--start-date', help='Start date (YYYY-MM-DD)')
@click.option('--end-date', help='End date (YYYY-MM-DD)')
@click.option('--limit', default=100, help='Number of records to retrieve')
@click.pass_context
def audit_trail(ctx, user_id, action_type, start_date, end_date, limit):
    """Retrieve audit trail records"""
    result = ctx.obj['client'].compliance.get_audit_trail(
        user_id=user_id,
        action_type=action_type,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )
    click.echo(json.dumps(result, indent=2))

@compliance.command(name='webhook-status')
@click.option('--webhook-id', help='Specific webhook ID to check')
@click.pass_context
def webhook_status(ctx, webhook_id):
    """Check webhook delivery status and retry queue"""
    if webhook_id:
        result = ctx.obj['client'].compliance.get_webhook_status(webhook_id)
    else:
        result = ctx.obj['client'].compliance.list_webhook_deliveries()
    click.echo(json.dumps(result, indent=2))

@compliance.command(name='retry-webhook')
@click.argument('webhook_id')
@click.pass_context
def retry_webhook(ctx, webhook_id):
    """Manually retry a failed webhook delivery"""
    result = ctx.obj['client'].compliance.retry_webhook(webhook_id)
    click.echo(json.dumps(result, indent=2))

@compliance.command(name='rate-limit-status')
@click.option('--user-id', help='Check rate limits for specific user')
@click.pass_context
def rate_limit_status(ctx, user_id):
    """Check current rate limiting status"""
    result = ctx.obj['client'].compliance.get_rate_limit_status(user_id)
    click.echo(json.dumps(result, indent=2))

# Advanced Compliance Commands (Enterprise)
@compliance.group(name='advanced')
@click.pass_context
def compliance_advanced(ctx):
    """Advanced compliance features for enterprise users"""

@compliance_advanced.command(name='bulk-process')
@click.argument('directory_path')
@click.option('--document-type', required=True, help='Type of documents to process')
@click.option('--batch-size', default=10, help='Number of documents per batch')
@click.pass_context
def bulk_process_documents(ctx, directory_path, document_type, batch_size):
    """Bulk process multiple compliance documents"""
    import os
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    if not hasattr(ctx.obj['client'], 'compliance_advanced'):
        click.echo("Error: Advanced compliance features not available. Please upgrade your plan.")
        return
    
    result = ctx.obj['client'].compliance_advanced.bulk_process_documents(
        directory_path, document_type, batch_size
    )
    click.echo(json.dumps(result, indent=2))

@compliance_advanced.command(name='compliance-dashboard')
@click.option('--export-format', type=click.Choice(['json', 'csv']), default='json')
@click.pass_context
def compliance_dashboard(ctx, export_format):
    """Generate compliance dashboard data"""
    if not hasattr(ctx.obj['client'], 'compliance_advanced'):
        click.echo("Error: Advanced compliance features not available. Please upgrade your plan.")
        return
    
    result = ctx.obj['client'].compliance_advanced.get_dashboard_data()
    
    if export_format == 'csv':
        import csv
        import sys
        writer = csv.writer(sys.stdout)
        if 'metrics' in result:
            writer.writerow(['Metric', 'Value'])
            for key, value in result['metrics'].items():
                writer.writerow([key, value])
    else:
        click.echo(json.dumps(result, indent=2))

@compliance_advanced.command(name='risk-assessment')
@click.argument('user_id')
@click.pass_context
def risk_assessment(ctx, user_id):
    """Perform comprehensive risk assessment for a user"""
    if not hasattr(ctx.obj['client'], 'compliance_advanced'):
        click.echo("Error: Advanced compliance features not available. Please upgrade your plan.")
        return
    
    result = ctx.obj['client'].compliance_advanced.perform_risk_assessment(user_id)
    click.echo(json.dumps(result, indent=2))
