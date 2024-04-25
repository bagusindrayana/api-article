from app.models.DB import db,session
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import declarative_base
import datetime
Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'

    id = Column("id",Integer, primary_key=True)
    title = Column("title",String)
    content = Column("content",String)
    category = Column("category",String)
    created_date = Column("created_date",TIMESTAMP)
    updated_date = Column("updated_date",TIMESTAMP)
    status = Column("status",String)

    def get_all():
        datas = session.query(Post).all()
        if len(datas) > 0:
            return datas
        return []
    
    def get_data(offset, limit):
        return session.query(Post).limit(limit).offset(offset).all()

    def paginate(page):
        offset = (page - 1) * 10
        return session.query(Post).limit(10).offset(offset).all()

    def get_by_id(id):
        return session.query(Post).filter(Post.id == id).first()
    
    def create(title, content, category, status):
        # current timestamp
        now = datetime.datetime.now()
        post = Post(title=title, content=content, category=category, status=status,created_date=now,updated_date=now)
        session.add(post)
        session.commit()
        return post
    
    def update(id, title, content, category, status):
        now = datetime.datetime.now()
        post = session.query(Post).filter(Post.id == id).first()
        post.title = title
        post.content = content
        post.category = category
        post.status = status
        post.updated_date = now
        session.commit()
        return post
    
    def delete(id):
        post = session.query(Post).filter(Post.id == id).first()
        session.delete(post)
        session.commit()
        return post

Base.metadata.create_all(db)