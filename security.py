import json
from urllib.request import urlopen

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, APIRouter
from fastapi.openapi.docs import get_swagger_ui_oauth2_redirect_html, get_swagger_ui_html
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt
from pydantic import BaseModel
from pydantic.v1 import BaseSettings

# Load environment variables from .env file
load_dotenv()


class AuthenticationSettings(BaseSettings):
    token_url: str
    authorization_url: str
    jwks_uri: str
    issuer: str
    resource: str
    client_id: str
    client_secret: str
    scopes: str

    class Config:
        env_file = ".env"


class DocSettings(BaseSettings):
    swagger_js_url: str
    swagger_favicon_url: str

    class Config:
        env_file = ".env"


class SessionResponse(BaseModel):
    jti: str
    sub: str
    iat: int
    exp: int
    scope: str
    client_id: str
    iss: str
    aud: str


auth_settings = AuthenticationSettings()
doc_settings = DocSettings()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl=auth_settings.token_url,
    authorizationUrl=auth_settings.authorization_url,
    scopes={scope: scope for scope in auth_settings.scopes.split(',')}
)


async def get_current_session(token=Depends(oauth2_scheme)) -> SessionResponse:
    jwks_uri = urlopen(auth_settings.jwks_uri)
    jwks = json.loads(jwks_uri.read())

    try:
        user = jwt.decode(
            token,
            jwks,
            # The jwt encode algorithm retrieved along with jwks. ES384 by default
            algorithms=jwt.get_unverified_header(token).get('alg'),
            # The API's registered resource indicator in Logto
            audience=auth_settings.resource,
            issuer=auth_settings.issuer,
            options={'verify_at_hash': False}
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Token")

    return SessionResponse(**user)


class DocumentationRouter:
    def __init__(self, openapi_url: str, swagger_ui_oauth2_redirect_url: str, title):
        self.router = APIRouter()
        self.openapi_url = openapi_url
        self.swagger_ui_oauth2_redirect_url = swagger_ui_oauth2_redirect_url
        self.title = title

        @self.router.get("/docs", include_in_schema=False)
        async def custom_swagger_ui_html():
            return get_swagger_ui_html(
                openapi_url=self.openapi_url,
                title=self.title + " - Swagger UI",
                oauth2_redirect_url=self.swagger_ui_oauth2_redirect_url,
                swagger_js_url=doc_settings.swagger_js_url,
                swagger_favicon_url=doc_settings.swagger_favicon_url,
                init_oauth={
                    "clientId": auth_settings.client_id,
                    "clientSecret": auth_settings.client_secret,
                    "resource": auth_settings.resource,
                    "scopes": auth_settings.scopes.split(','),
                    "additionalQueryStringParams": {
                        "resource": auth_settings.resource
                    }
                },
                swagger_ui_parameters={
                    "persistAuthorization": False,
                },
            )

        @self.router.get(self.swagger_ui_oauth2_redirect_url, include_in_schema=False)
        async def custom_swagger_ui_html_redirect():
            return get_swagger_ui_oauth2_redirect_html()
