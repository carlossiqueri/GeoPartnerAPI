from fastapi import FastAPI

from app.api.routes import partner_route

app = FastAPI()

app.include_router(partner_route.router)

@app.get("/health")
def api_health():
    """
        Endpoint to check if the api is up and running.
    """
    return {"message": "Welcome to GeoPartnerAPI"}
