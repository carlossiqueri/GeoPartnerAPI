from pydantic import BaseModel

class UserLocation(BaseModel):
    log: str
    lat: str
