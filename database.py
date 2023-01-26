from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel, create_engine

class TopicBase(SQLModel):
    topic_name: str = Field(nullable=False)

class Topic(TopicBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    posts: List["Post"] = Relationship(back_populates="topic")

class TopicRead(TopicBase):
    id:int

class TopicCreate(TopicBase):
    pass

class PostBase(SQLModel):
    post_title: str = Field(nullable=False)
    post_body: str = Field(nullable=True)
    post_visible: bool = Field(default=True, nullable=False)
    post_topic_fk: Optional[int] = Field(default=1, foreign_key="topic.id")

class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic: Optional[Topic] = Relationship(back_populates="posts")

class PostRead(PostBase):
    id:int

#https://github.com/tiangolo/sqlmodel/issues/224
#https://github.com/tiangolo/sqlmodel/issues/342
#https://github.com/tiangolo/sqlmodel/issues/6
## Relationship is never created because the object is missing ?
class PostCreate(PostBase):
    #topic: Optional[Topic] = None
    pass
    
class PostUpdate(SQLModel):
    post_title: Optional[str] = Field(nullable=False)
    post_body: Optional[str] = Field(nullable=True)
    post_visible: Optional[bool] = Field(default=True, nullable=False)
    post_topic_fk: Optional[int] = Field(default=1, foreign_key="topic.id")

class PostWithTopic(PostRead):
    topic: Optional[TopicRead] = None

class TopicsWithPosts(TopicRead):
    posts: List[Post] = []


sqlite_file_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)

def create_tables():
    SQLModel.metadata.create_all(engine)