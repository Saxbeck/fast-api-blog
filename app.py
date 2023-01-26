from fastapi import FastAPI, Request ,HTTPException, Depends
from typing import List, Optional
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy import desc, asc
from sqlmodel import Field,Session,SQLModel,create_engine,select
from database import create_tables,engine
from database import Post, PostCreate, PostWithTopic, PostUpdate
from database import Topic, TopicRead

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="./templates")


def get_session():
    with Session(engine) as session:
        yield session



@app.on_event("startup") 
async def on_startup():
    create_tables()
 

@app.get("/api/posts", response_model=List[Post], tags=["Api Posts"])
def read_posts(*, session:Session = Depends(get_session)):
    with session:
        posts = session.exec(select(Post).order_by(desc(Post.id))).all()
        print(posts)
    return posts

@app.post("/api/posts", response_model=Post, tags=["Api Posts"])
def make_post(*, session:Session = Depends(get_session), post: PostCreate):
    with session:
        db_post = Post.from_orm(post)
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
        #print(db_post)
    return db_post

@app.patch("/api/posts/{post_id}", response_model=Post, tags=["Api Posts"])
def update_post(*, session:Session = Depends(get_session),post:PostUpdate, post_id:int):
    with session:
        db_post = session.get(Post, post_id)
        if not post_id:
            raise HTTPException(status_code=404, detail="Post not found")
        post_data = post.dict(exclude_unset=True)
        for key, value in post_data.items():
            setattr(db_post,key,value)
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
        return db_post

@app.delete("/api/posts/{post_id}", response_model=Post, tags=["Api Posts"])
def delete_post(*, session:Session = Depends(get_session), post_id):
    with session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        else:
            session.delete(post)
            session.commit()
            return post
###########################################################

@app.get("/api/topics", response_model=List[Topic], tags=["Api Topics"])
def read_topics(*, session:Session = Depends(get_session)):
    topics = session.exec(select(Topic)).all()
    print(topics)
    return topics

#############################################################

@app.get("/", response_class=HTMLResponse, tags=["HTML Pages"])
def index(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})

@app.get("/posts/", response_class=HTMLResponse, tags=["HTML Pages"])
def read_posts(*, session:Session = Depends(get_session), request: Request):
    posts = session.exec(select(Post)).all()
    print(posts)
    # context = {'request': request, 'posts': posts}
    return templates.TemplateResponse("posts.html", {'request': request, 'posts': posts})


@app.get("/posts/{id}", response_class=HTMLResponse,tags=["HTML Pages"])
def read_post(*, session:Session = Depends(get_session), request: Request, id:str):
    post = session.get(Post, id)
    context = {'request': request, 'post': post}
    print(post)
    return templates.TemplateResponse("post.html", context)


@app.get("/topics/", response_class=HTMLResponse, tags=['HTML Pages'])
def read_topics(*, session:Session = Depends(get_session), request: Request):
    topics = session.exec(select(Topic)).all()
    return templates.TemplateResponse("topics.html", {'request': request, 'topics': topics})