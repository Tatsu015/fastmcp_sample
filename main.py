from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Header
from fastmcp import FastMCP


class User(BaseModel):
    id: int
    name: str
    age: int


api_app = FastAPI()

users: dict[int, User] = {}


@api_app.post("/users", operation_id="create_users")
def create_user(user: User, x_token: str = Header(None)):
    if x_token != "very-important-token":
        raise HTTPException(status_code=401, detail="Invalid request")
    users[user.id] = user
    return users[user.id]


@api_app.get("/users", operation_id="read_users")
def read_users():
    return list(users.values())


@api_app.get("/users/{user_id}", operation_id="read_user")
def read_user(user_id: int):
    user = users[user_id]
    return {"id": user_id, "name": user.name, "age": user.age}


@asynccontextmanager
async def app_lifespan(api_app: FastAPI):
    print("Starting up the app!🛫")
    yield
    print("Shutting down the app...🛬")


@asynccontextmanager
async def combined_lifespan(api_app: FastAPI):
    # Run both lifespans
    async with app_lifespan(api_app):
        async with mcp_app.lifespan(api_app):
            yield


mcp = FastMCP.from_fastapi(app=api_app, name="E-commerce MCP")
mcp_app = mcp.http_app(path="/mcp")
app = FastAPI(
    title="E-commerce API with MCP",
    routes=[
        *mcp_app.routes,  # MCP routes
        *api_app.routes,  # Original API routes
    ],
    lifespan=combined_lifespan,
)
