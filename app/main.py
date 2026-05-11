from fastapi import FastAPI
from app.schemas import Review
from app.database import SessionLocal
from app import models

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
    db = SessionLocal()
    db_review = models.Review(
        movie=review.movie,
        rating=review.rating,
        comment=review.comment
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review

# Read reviews
@app.get("/reviews")
def get_reviews():
    db = SessionLocal()
    return db.query(models.Review).all()

# Update review
@app.put("/reviews")
def update_review(
    id: int,
    review: Review
):
    db = SessionLocal()

    db_review = db.query(models.Review).filter(models.Review.id == id).first()

    db_review.movie = review.movie
    db_review.rating = review.rating
    db_review.comment = review.comment

    db.commit()
    db.refresh(db_review)

    return db_review

# Delete review
@app.delete("/reviews/{id}")
def delete_review(id: int):
    db = SessionLocal()

    db_review = db.query(models.Review).filter(models.Review.id == id).first()

    db.delete(db_review)
    db.commit()

    return {
        "message": f"Review of ID {id} has been deleted."
    }