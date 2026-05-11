from fastapi import FastAPI
from app.schemas import Review

reviews = []

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

# Add/Create review
@app.post("/reviews")
def create_review(review: Review):
    reviews.append(review)
    return review

# Read reviews
@app.get("/reviews")
def get_reviews():
    return reviews

# Update review
@app.put("/reviews")
def update_review(
    id: int,
    review: Review
):
    reviews[id] = review
    return review

# Delete review
@app.delete("/reviews/{id}")
def delete_review(id: int):
    reviews.pop(id)
    return {
        "message": "Review deleted"
    }