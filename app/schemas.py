from pydantic import BaseModel

class Review(BaseModel):
    movie: str
    rating: int
    comment: str