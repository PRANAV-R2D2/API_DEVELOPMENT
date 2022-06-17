
from .. import models,schema,utils
from fastapi import  Depends,status,HTTPException ,APIRouter
from ..database import  get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post('/' , status_code=status.HTTP_201_CREATED ,response_model= schema.ResponseUser)
def create_user( user: schema.UserCreate, db : Session = Depends(get_db)):

    
    user.password = utils.hashh(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}',response_model= schema.ResponseUser)
def get_user(id: int , db : Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id {id} does not exist ")
    return user
