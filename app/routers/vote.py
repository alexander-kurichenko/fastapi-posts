from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(vote: schemas.Vote, user: object = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user.id)
    found_vote = vote_query.first()
    if vote.like:
        # Adding vote
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {user.id} has already voted")
        new_vote = models.Vote(post_id=vote.post_id, user_id=user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        # Deleting vote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}

