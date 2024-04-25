from fastapi import FastAPI, Response, status, HTTPException, Request
import os
import uvicorn
from pydantic import BaseModel,model_validator
import json

from app.models.Post import Post

app = FastAPI()


class PostRequest(BaseModel):
    title: str
    content: str
    category: str
    status: str = "draft"

    @model_validator(mode='before')
    @classmethod
    # Title: required, minimal 20 karakter
    # Content: required, minimal 200 karakter
    # Category: required, minimal 3 karakter
    # Status: required, enum (“publish”, “draft”, “thrash”)
    def validate_field(cls, v):
        # empty string validation
        if not v:
            raise ValueError("Field tidak boleh kosong")
        
        if "title" in v:
            if len(v['title']) < 20:
                raise ValueError("Title minimal 20 karakter")
        if "content" in v:
            if len(v['content']) < 200:
                raise ValueError("Content minimal 200 karakter")
        if "category" in v:
            if len(v['category']) < 3:
                raise ValueError("Category minimal 3 karakter")
        if "status" in v:
            if v['status'] not in ["publish", "draft", "thrash"]:
                raise ValueError("Status harus diantara publish, draft, thrash")
        
        return v

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/article")
def get_article(request: Request):
    page = request.query_params.get("page") or 1
    return Post.paginate(page)

@app.get("/article/{limit}/{offset}")
def get_article_offset(limit: int, offset: int):
    
    return Post.get_data(offset, limit)


@app.get("/article/{id}")
def get_article_by_id(id: int):
    post = Post.get_by_id(id)
    if post:
        return post
    raise HTTPException(status_code=404, detail="Post not found")

@app.post("/article")
def create_article(post: PostRequest, request: Request):
    try:
        validated_item = PostRequest(**post.dict())
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    post = Post.create(validated_item.title, validated_item.content, validated_item.category, validated_item.status)
    return "success"

# put method
@app.put("/article/{id}")
def update_article(id: int, post: PostRequest, request: Request):
    try:
        validated_item = PostRequest(**post.dict())
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    post = Post.update(id,validated_item.title, validated_item.content, validated_item.category, validated_item.status)
    return "success"

# delete method
@app.delete("/article/{id}")
def delete_article(id: int):
    post = Post.delete(id)
    return "success"

default_port = "8111"
try:
    port = int(float(os.getenv("PORT", default_port)))
except TypeError:
    port = int(default_port)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)