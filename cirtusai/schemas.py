from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Agent(BaseModel):
    id: str
    name: Optional[str]
    did: Optional[str]
    state: Optional[Dict[str, Any]]

class Asset(BaseModel):
    id: str
    type: str
    details: Dict[str, Any]

class ChildAgent(BaseModel):
    id: str
    parent_id: Optional[str]
    name: Optional[str]
    permissions: Optional[Dict[str, Any]]
    state: Optional[Dict[str, Any]]

class Permissions(BaseModel):
    permissions: Dict[str, Any]

class DID(BaseModel):
    did: str
    info: Dict[str, Any]

class EmailAccount(BaseModel):
    id: str
    provider: str
    email_address: str
    config: Dict[str, Any]

class CredentialResponse(BaseModel):
    credential: Dict[str, Any]
