from pydantic import BaseModel
from fastapi import FastAPI


class User(BaseModel):
    id: int
    name: str
    age: int


app = FastAPI()

users: dict[int, User] = {}


@app.post("/users")
def create_user(user: User):
    users[user.id] = user
    return users[user.id]


@app.get("/users")
def read_users():
    return list(users.values())


@app.get("/users/{user_id}")
def read_user(user_id: int):
    user = users[user_id]
    return {"id": user_id, "name": user.name, "age": user.age}
