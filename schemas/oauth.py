from pydantic import BaseModel

class AccessToken(BaseModel):
    active: bool
    scope: str | None= None
    exp: int | None= None
    client_id: str | None= None
    authorities: list[str] | None= None
    projects: list[str] | None = []
    segments: list[str] | None = []
    token: str | None = None
    name: str | None = None