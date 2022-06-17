from sqlalchemy import func
from app import oauth
from .. import models,schema
from fastapi import Body, Depends,Response,status,HTTPException ,APIRouter
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import List, Optional


router =APIRouter(
    prefix="/posts",
    tags= ['posts']
)                    

@router.get('/' ,response_model=List[schema.Responsepost2])
#@router.get('/' )

def get_posts(db : Session = Depends(get_db),current_user:int  = Depends(oauth.get_current_user),Limit: int = 10,skip :int = 0,search : Optional[str]=""):
    # cursors.execute("""SELECT * FROM posts""")
    # posts = cursors.fetchall()
    #print(posts)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    

    ##if we want to return only the posts from the user
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_  user.id).all()
    return results




@router.post('/' , status_code=status.HTTP_201_CREATED,response_model=schema.Responsepost)
def create_posts(payloadd : schema.PostCreate,db : Session = Depends(get_db), current_user :int  = Depends(oauth.get_current_user)):

    #print(current_user.email) 
    new_post = models.Post(owner_id = current_user.id,**payloadd.dict())
    new_post
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post

@router.get("/{id}",response_model=schema.Responsepost2)
def retrive_post(id: int , db : Session = Depends(get_db),current_user:int  = Depends(oauth.get_current_user)):
    # cursors.execute(""" SELECT * FROM posts where id = %s""",(str(id)))
    # post = cursors.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} NOT FOUND")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'message': f"post with id :{id}"}
    return post






@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db : Session = Depends(get_db),current_user:int  = Depends(oauth.get_current_user)):
    # cursors.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # deleted_post = cursors.fetchone()
    # conne.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist ")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,detail="not authorised to perform the requested action")
    post_query.delete(synchronize_session = False)
    db.commit()
    
    # return{'message':"post was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schema.Responsepost)
def update_post(id :int, updated_post:schema.PostCreate, db : Session = Depends(get_db),current_user:int  = Depends(oauth.get_current_user)):


    # cursors.execute("""UPDATE posts SET title = %s, content = %s , published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # updated_post = cursors.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist ")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,detail="not authorised to perform the requested action")
    
    post_query.update(updated_post.dict(),synchronize_session = False)
    db.commit()  
#    conne.commit()
    return  post
 