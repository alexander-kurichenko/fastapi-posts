from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import posts, users, auth, vote
from . import models, database

# Will create using alembic
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = ['*'] # TODO: Change to more specific ones!

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(vote.router)
app.include_router(auth.router)


# GET /
@app.get("/")
async def root():
    return {"message": "here's a message from API", "data": "data payload will be here"}


