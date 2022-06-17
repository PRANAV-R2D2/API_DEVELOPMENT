from os import access
from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models

from .. import database ,schema,utils,oauth

router = APIRouter(tags= ['Authentication'])

@router.post("/login",response_model=schema.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends() ,db: Session =  Depends(database.get_db)):


    user_query =db.query(models.User).filter(models.User.email== user_credentials.username)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credentials")

    if not utils.verifyy(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,detail="invalid credentials")
        
    #creating token
    #returntoken
    access_token = oauth.create_access_token(data = {"user_id": user.id})

    return {"access_token":access_token ,"token_type": "bearer"}