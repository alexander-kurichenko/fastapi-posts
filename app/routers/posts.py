from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# GET all posts
@router.get("/", response_model=List[schemas.PostOut])
def get_all_posts(db: Session = Depends(get_db), current_user: object = Depends(oauth2.get_current_user),
                  limit: int = 100, skip: int = 0, search: Optional[str] = ""):
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # added likes in new query
    posts = db.query(models.Post, func.count(models.Vote.user_id).label("votes"))\
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id) \
        .filter(models.Post.title.contains(search))\
        .limit(limit)\
        .offset(skip)\
        .all()
    return posts


# GET post by id
@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db), current_user: object = Depends(oauth2.get_current_user)):
    #post = db.query(models.Post).filter(models.Post.id == post_id).first()

    post = db.query(models.Post, func.count(models.Vote.user_id).label("votes"))\
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.id == post_id)\
        .first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'post with id {post_id} does not exist'})
    return post


# Create new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db),
                current_user: object = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id,  **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Update specific post
@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db),
                current_user: object = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'post with id {post_id} does not exist'})
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail={'message': 'Not authorised to perform requested action'})
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


# DELETE specific post
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, response: Response, db: Session = Depends(get_db),
                current_user: object = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'post with id {post_id} does not exist'})
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail={'message': 'Not authorised to perform requested action'})
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
