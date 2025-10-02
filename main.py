from pydantic import BaseModel
from fastapi import FastAPI
from fastmcp import FastMCP


class User(BaseModel):
    id: int
    name: str
    age: int


api_app = FastAPI()

users: dict[int, User] = {}


@api_app.post("/users")
def create_user(user: User):
    users[user.id] = user
    return users[user.id]


@api_app.get("/users")
def read_users():
    return list(users.values())


@api_app.get("/users/{user_id}")
def read_user(user_id: int):
    user = users[user_id]
    return {"id": user_id, "name": user.name, "age": user.age}


mcp = FastMCP.from_fastapi(app=api_app, name="E-commerce MCP")
mcp_app = mcp.http_app(path="/mcp")
app = FastAPI(
    title="E-commerce API with MCP",
    routes=[
        *mcp_app.routes,  # MCP routes
        *api_app.routes,  # Original API routes
    ],
    lifespan=mcp_app.lifespan,
)
