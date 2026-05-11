from fastapi import FastAPI

# Create the app
app = FastAPI()

# Endpoints
@app.get("/")
def root():
    return {
        "message": "Movie Review API"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }