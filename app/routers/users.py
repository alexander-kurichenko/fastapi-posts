from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Create new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash password - user.password
    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get user by id
@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: object = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'user with id {user_id} does not exist'})
    return user
