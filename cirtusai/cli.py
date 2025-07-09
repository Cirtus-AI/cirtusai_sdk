import os
import click
import json
from .client import CirtusAIClient

@click.group()
@click.option('--api-url', default=lambda: os.getenv('CIRTUSAI_API_URL', 'http://localhost:8000'), help='Base URL for CirtusAI API')
@click.option('--token', envvar='CIRTUSAI_TOKEN', help='JWT access token (or set CIRTUSAI_TOKEN)')
@click.option('--agent-id', envvar='CIRTUSAI_AGENT_ID', help='Child agent ID for asset provisioning (or set CIRTUSAI_AGENT_ID)')
@click.pass_context
def main(ctx, api_url, token, agent_id):
    """
    CirtusAI CLI: manage agents, assets, credentials, etc.
    """
    if not token:
        click.echo('Error: Missing JWT token. Provide via --token or CIRTUSAI_TOKEN', err=True)
        ctx.exit(1)
    if not agent_id:
        click.echo('Warning: No agent_id provided. Some commands may require it.', err=True)
    client = CirtusAIClient(base_url=api_url, token=token)
    ctx.obj = client
    # store optional child agent id
    ctx.agent_id = agent_id

@main.group()
@click.pass_context
def auth(ctx):
    """Authentication commands"""
    pass

@auth.command('login')
@click.argument('email')
@click.argument('password')
@click.pass_context
def login(ctx, email, password):
    """Login with email and password"""
    data = ctx.obj.auth.login(email, password)
    click.echo(data)

@auth.command('refresh')
@click.argument('refresh_token')
@click.pass_context
def refresh(ctx, refresh_token):
    """Refresh JWT token using refresh token"""
    data = ctx.obj.auth.refresh(refresh_token)
    click.echo(data)

@main.group()
@click.pass_context
def agents(ctx):
    """Agent management commands"""
    pass

@agents.command('list')
@click.pass_context
def list_agents(ctx):
    """List master agents"""
    data = ctx.obj.agents.list_agents()
    click.echo(json.dumps(data))

@agents.command('get')
@click.argument('agent_id')
@click.pass_context
def get_agent(ctx, agent_id):
    """Retrieve a specific agent by ID or DID"""
    data = ctx.obj.agents.get_agent(agent_id)
    click.echo(json.dumps(data))

@agents.command('children')
@click.pass_context
def get_children(ctx):
    """List all child agents"""
    data = ctx.obj.agents.get_children()
    click.echo(json.dumps(data))

@agents.command('create-child')
@click.argument('parent_id')
@click.argument('name')
@click.pass_context
def create_child(ctx, parent_id, name):
    """Create a new child agent"""
    data = ctx.obj.agents.create_child_agent(parent_id, name)
    click.echo(json.dumps(data))

@agents.command('update-permissions')
@click.argument('child_id')
@click.argument('permissions', type=str)
@click.pass_context
def update_permissions(ctx, child_id, permissions):
    """Update permissions for a child agent, JSON string"""
    perms = json.loads(permissions)
    data = ctx.obj.agents.update_child_permissions(child_id, perms)
    click.echo(json.dumps(data))

@agents.command('unlink')
@click.argument('child_id')
@click.pass_context
def unlink_child(ctx, child_id):
    """Unlink (delete) a child agent"""
    ctx.obj.agents.unlink_child_agent(child_id)
    click.echo(f"Unlinked child agent {child_id}")

@main.group()
@click.pass_context
def wallets(ctx):
    """Wallet and asset management commands"""
    pass

@wallets.command('list-assets')
@click.pass_context
def list_assets(ctx):
    """List all wallet assets"""
    data = ctx.obj.wallets.list_assets()
    click.echo(json.dumps(data))

@wallets.command('add-asset')
@click.argument('asset_key')
@click.argument('asset_value')
@click.pass_context
def add_asset(ctx, asset_key, asset_value):
    """Add a vault asset"""
    ctx.obj.wallets.add_asset(asset_key, asset_value)
    click.echo('Asset added')

@wallets.command('bulk-add')
@click.argument('assets', type=str)
@click.pass_context
def bulk_add(ctx, assets):
    """Bulk add vault assets (JSON)"""
    items = json.loads(assets)
    ctx.obj.wallets.bulk_add_assets(items)
    click.echo('Bulk added')

@wallets.command('add-crypto')
@click.option('--chain', default='ethereum')
@click.pass_context
def add_crypto(ctx, chain):
    """Provision crypto wallet"""
    click.echo(ctx.obj.wallets.add_crypto(chain))

@wallets.command('list-email')
@click.pass_context
def list_email(ctx):
    """List linked email accounts"""
    data = ctx.obj.wallets.list_email_accounts()
    click.echo(json.dumps(data))

@wallets.command('get-email')
@click.argument('account_id')
@click.pass_context
def get_email(ctx, account_id):
    """Get email account detail"""
    click.echo(ctx.obj.wallets.get_email_account(account_id))

@wallets.command('create-email')
@click.argument('provider')
@click.argument('email_address')
@click.argument('config', type=str)
@click.pass_context
def create_email(ctx, provider, email_address, config):
    """Create a new email account (JSON config)"""
    cfg = json.loads(config)
    click.echo(ctx.obj.wallets.create_email_account(provider, email_address, cfg))

@wallets.command('update-email')
@click.argument('account_id')
@click.argument('provider')
@click.argument('email_address')
@click.argument('config', type=str)
@click.pass_context
def update_email(ctx, account_id, provider, email_address, config):
    """Update email account (JSON config)"""
    cfg = json.loads(config)
    click.echo(ctx.obj.wallets.update_email_account(account_id, provider, email_address, cfg))

@wallets.command('delete-email')
@click.argument('account_id')
@click.pass_context
def delete_email(ctx, account_id):
    """Delete an email account"""
    ctx.obj.wallets.delete_email_account(account_id)
    click.echo('Deleted')

@wallets.command('refresh-email-token')
@click.argument('account_id')
@click.pass_context
def refresh_email_token(ctx, account_id):
    """Refresh email OAuth token"""
    click.echo(ctx.obj.wallets.refresh_email_token(account_id))

@main.group()
@click.pass_context
def identity(ctx):
    """DID & credentials commands"""
    pass

@identity.command('get-did')
@click.argument('agent_id')
@click.pass_context
def get_did(ctx, agent_id):
    """Resolve a DID"""
    click.echo(ctx.obj.identity.get_did(agent_id))

@identity.command('issue-credential')
@click.argument('subject_id')
@click.argument('claim', type=str)
@click.pass_context
def issue_credential(ctx, subject_id, claim):
    """Issue a Verifiable Credential"""
    c = json.loads(claim)
    data = ctx.obj.identity.issue_credential(subject_id=subject_id, types=['VerifiableCredential'], claim=c)
    click.echo(json.dumps(data))

@identity.command('verify-credential')
@click.argument('jwt_token')
@click.pass_context
def verify_cred(ctx, jwt_token):
    """Verify a Verifiable Credential token"""
    click.echo(ctx.obj.identity.verify_credential(jwt_token))

@main.group()
@click.pass_context
def command(ctx):
    """Command bus operations"""
    pass

@command.command('send')
@click.argument('text')
@click.pass_context
def send_command(ctx, text):
    """Send a raw command text"""
    click.echo(ctx.obj.command.send(text))

if __name__ == '__main__':
    main()
