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
        return session.query(Post).order_by(Post.created_date.desc()).limit(limit).offset(offset).all()

    def paginate(page):
        # if page is string
        if isinstance(page, str):
            page = int(page)
        offset = (page - 1) * 10
        return session.query(Post).limit(10).offset(offset).all()

    def filter(page,search,status=None):
        # if page is string
        if isinstance(page, str):
            page = int(page)
        offset = (page - 1) * 10
        next = False
        prev = False
        datas = session.query(Post)
        if search:
            datas = datas.filter(Post.title.like(f"%{search}%"))
        
        if status:
            datas = datas.filter(Post.status == status)
        count = datas.count()

        # order by created_date
        datas = datas.order_by(Post.created_date.desc())

        if count > offset + 10:
            next = True
        
        if offset > 0:
            prev = True

        datas = datas.limit(10).offset(offset)
        return {
            "data":datas.all(),
            "count":count,
            "prev":prev,
            "next":next
        }

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
        if post:
            post.title = title
            post.content = content
            post.category = category
            post.status = status
            post.updated_date = now
            session.commit()
        else:
            raise Exception("Post not found")
        
        return post
    
    def trash(id):
        post = session.query(Post).filter(Post.id == id).first()
        if post:
             post.status = "thrash"
             session.commit()
        else:
            raise Exception("Post not found")
        return post
    
    def delete(id):
        post = session.query(Post).filter(Post.id == id).first()
        if post:
            session.delete(post)
            session.commit()
        else:
            raise Exception("Post not found")
        return post

Base.metadata.create_all(db)