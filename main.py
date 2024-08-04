from fastapi import FastAPI, Depends
from starlette.staticfiles import StaticFiles

from security import DocumentationRouter, get_current_session, SessionResponse

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json",
    swagger_js_url="/static/swagger-ui-bundle.js",
    title="GeoSPEAR API",
    swagger_favicon_url="/static/favicon.ico",

)

documentation = DocumentationRouter(
    openapi_url=app.openapi_url,
    swagger_ui_oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
    title=app.title
)

app.mount(
    path="/static",
    app=StaticFiles(
        directory="static"
    ),
    name="static"
)

app.include_router(
    router=documentation.router,
    tags=["Documentation"]
)


@app.get("/session", response_model=SessionResponse)
async def session(session: str = Depends(get_current_session)):
    return session


@app.get("/private_endpoint", dependencies=[Depends(get_current_session)])
async def private_endpoint():
    return {"message": "This is a private endpoint"}


@app.get("/")
async def public_endpoint():
    return {"message": "This is a public endpoint"}
