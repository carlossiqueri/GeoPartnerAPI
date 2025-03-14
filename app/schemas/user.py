from pydantic import BaseModel


class UserLocation(BaseModel):
    lon: float
    lat: float
