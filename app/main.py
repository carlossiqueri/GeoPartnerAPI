from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def api_health():
    """
        Endpoint to check if the api is up and running.
    """
    return {"message": "Welcome to GeoPartnerAPI"}
