
from fastapi import Body, Depends, FastAPI,Response,status,HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from requests import Session
from . import models
from .database import engine , get_db



models.Base.metadata.create_all(bind = engine)

#dependency

app = FastAPI()

class posts(BaseModel):
    title: str
    content: str
    published: bool = True



while True:


    try:
        conne = psycopg2.connect(host='localhost',database='fastapi_db',user='postgres',password='postgress123',cursor_factory=RealDictCursor)
        cursors = conne.cursor()
        print("database connected")
        break
    except Exception as error:
        print("connecting to database failed")
        print("Error :",error)
        time.sleep(5)











my_post = [{"title":"post1","content":"content1","id":1},{"title":"post2","content":"content2","id":2}]

def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_post):
        if p['id'] == id:
            return i
 
    
@app.get('/')
def first():

    return{"message":"helloo world"}




@app.get("/sql")
def test_posts(db : Session = Depends(get_db)):
    return{"status":"success"}




@app.get('/post')
def getpost(payloadd : dict = Body()):
    return {"data": payloadd}

@app.post('/createpost')
def getpost(payloadd : posts):
    print(payloadd.title)
    my_post.append(payloadd.dict())
    return {"data": payloadd.title}


@app.get('/posts')
def get_posts():
    cursors.execute("""SELECT * FROM posts""")
    posts = cursors.fetchall()
    print(posts)
    return{"data":posts}




@app.post('/posts' , status_code=status.HTTP_201_CREATED)
def create_posts(payloadd : posts):
    #not using 
    # cursors.execute(f"INSERT INTO post (title,content,published) VaLUES (%s,%s,%s)" )
    #because that leds to open for S&L injection
    cursors.execute("""INSERT INTO posts (title,content,published) VaLUES (%s,%s,%s) RETURNING *""",(payloadd.title,payloadd.content,payloadd.published))
    new_post = cursors.fetchone()
    conne.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def retrive_post(id: int , response : Response):
    cursors.execute(""" SELECT * FROM posts where id = %s""",(str(id)))
    post = cursors.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} NOT FOUND")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'message': f"post with id :{id}"}
    return{"details":post}




@app.get("/latestpost")
def get_latest_post():
   post =  my_post[len(my_post)-1]

   return{"details": post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    cursors.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    deleted_post = cursors.fetchone()
    conne.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist ")

    
    # return{'message':"post was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id :int, post:posts):


    cursors.execute("""UPDATE posts SET title = %s, content = %s , published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    updated_post = cursors.fetchone()
    

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist ")
    conne.commit()
    return{'message': updated_post}
