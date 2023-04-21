from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional #opcional es para que también pueda recibir valores nulos
from datetime import datetime
from uuid import uuid4 as uuid #es para generar id aleatorios y con más caracteres
app = FastAPI()

posts = [] #base de datos en una lista

# Post Model
class Post(BaseModel): # clase post que hereda BaseModel que viene de pydantic
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now() #es para que cuando se genere el post, guardé la fecha de ese momento (fecha de creación)
    published_at: Optional[datetime]
    published: bool = False #puede haber sido publicado o no y su valor por defecto es False

@app.get('/')
def read_root():
    return{"welcome":"Welcome to my REST API"}
@app.get('/posts')
def get_posts():
    return posts
@app.post('/posts')
def save_post(post: Post): # el parámetro post es de tipo Post que definimos arriba
    post.id = str(uuid()) #hacemos que devuelva un string, sino devolverá una clase
    posts.append(post.dict()) #convierte el parámetro en un diccionario y lo añade al arreglo posts
    return posts[-1] #retorna el último elemento que he añadido a la lista posts
@app.get('/posts/{post_id}') #el {} significa que puede ser cualquier id y post_id es solo un nombre genérico para que se entienda que ahí van IDs
def get_post(post_id: str):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")