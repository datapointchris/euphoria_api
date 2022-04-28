from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routes import tasks

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()


app.include_router(tasks.router)
# app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    # dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    print('BROKEN')
    return {"message": "This is the API"}


