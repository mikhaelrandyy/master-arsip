
import httpx
from httpx import Response
from fastapi import Request
from functools import wraps
from jose import jwt # type: ignore
import fastapi
from schemas.oauth_sch import AccessToken
from configs.config import settings

tenant_id = settings.AZURE_TENANT_ID
client_id = settings.AZURE_CLIENT_ID

class AuthError(Exception):
    def __init__(self, error_msg: str, status_code: int):
        super().__init__(error_msg)

        self.error_msg = error_msg
        self.status_code = status_code

class AzureAuthService:
    def get_token_auth_header(self, request: Request):
        auth = request.headers.get("Authorization", None)
        if not auth:
            raise AuthError(
                "Authentication error: Authorization header is missing", 401)

        parts = auth.split()

        if parts[0].lower() != "bearer":
            raise AuthError(
                "Authentication error: Authorization header must start with ' Bearer'", 401)
        elif len(parts) == 1:
            raise AuthError("Authentication error: Token not found", 401)
        elif len(parts) > 2:
            raise AuthError(
                "Authentication error: Authorization header must be 'Bearer <token>'", 401)

        token = parts[1]
        return token


    def get_token_claims(self, request: Request):
        token = self.get_token_auth_header(request)
        unverified_claims = jwt.get_unverified_claims(token)
        return unverified_claims


    def validate_scope(self, required_scope: str, request: Request):
        has_valid_scope = False
        token = self.get_token_auth_header(request)
        unverified_claims = jwt.get_unverified_claims(token)
        # check to ensure that either a valid scope or a role is present in the token
        if unverified_claims.get("scp") is None and unverified_claims.get("roles") is None:
            raise AuthError(
                "IDW10201: No scope or app permission (role) claim was found in the bearer token", 403)

        is_app_permission = True if unverified_claims.get(
            "roles") is not None else False

        if is_app_permission:
            if unverified_claims.get("roles"):
                # the roles claim is an array
                for scope in unverified_claims["roles"]:
                    if scope.lower() == required_scope.lower():
                        has_valid_scope = True
            else:
                raise AuthError(
                    "IDW10201: No app permissions (role) claim was found in the bearer token", 403)
        else:
            if unverified_claims.get("scp"):
                # the scp claim is a space delimited string
                token_scopes = unverified_claims["scp"].split()
                for token_scope in token_scopes:
                    if token_scope.lower() == required_scope.lower():
                        has_valid_scope = True
            else:
                raise AuthError(
                    "IDW10201: No scope claim was found in the bearer token", 403)

        if is_app_permission and not has_valid_scope:
            raise AuthError(
                f'IDW10203: The "role" claim does not contain role {required_scope} or was not found', 403)
        elif not has_valid_scope:
            raise AuthError(
                f'IDW10203: The "scope" or "scp" claim does not contain scopes {required_scope} or was not found', 403)
        
    async def check_token(self, token):
        try:
            url = f'https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys'

            async with httpx.AsyncClient() as client:
                resp: Response = await client.get(url)
                if resp.status_code != 200:
                    raise AuthError(
                        "Problem with Azure AD discovery URL", status_code=404)

                jwks = resp.json()
                unverified_header = jwt.get_unverified_header(token)
                rsa_key = {}
                for key in jwks["keys"]:
                    if key["kid"] == unverified_header["kid"]:
                        rsa_key = {
                            "kty": key["kty"],
                            "kid": key["kid"],
                            "use": key["use"],
                            "n": key["n"],
                            "e": key["e"]
                        }
        except Exception as e:
            raise e
            # return fastapi.Response(content="Invalid_header: Unable to parse authentication", status_code=401)
        if rsa_key:
            try:
                token_version = self.__get_token_version(token)
                decoded = self.__decode_JWT(token_version, token, rsa_key)
                roles = []
                if "roles" in decoded:
                    roles = decoded["roles"]
                    # raise AuthError("IDW10201: No roles was found in the bearer token", 403)
                if "user_projects" in decoded:
                    projects = [decoded['user_projects']] if isinstance(decoded['user_projects'], str) else decoded['user_projects']
                else:
                    projects = []

                if "user_segments" in decoded:
                    segments = [decoded['user_segments']] if isinstance(decoded['user_segments'], str) else decoded['user_segments']
                else:
                    segments = []
                
                if "user_authorities" in decoded:
                    authorities = [decoded['user_authorities']] if isinstance(decoded['user_authorities'], str) else decoded['user_authorities']
                else:
                    authorities= [] if "preferred_username" in decoded else ['superadmin']

                return AccessToken(
                        active=True,
                        client_id=decoded["preferred_username"] if "preferred_username" in decoded else decoded["azp"],
                        scope=decoded["scp"] if "scp" in decoded else "",
                        authorities= authorities,
                        exp=decoded["exp"],
                        projects=projects,
                        token=token,
                        name=decoded["name"] if "name" in decoded else "",
                        segment=segments
                        ), "SUCCESS"
            except AuthError as auth_err:
                raise auth_err
        return fastapi.Response(content="Invalid header error: Unable to find appropriate key", status_code=401)


    def requires_auth(self, f):
        @wraps(f)
        async def decorated(*args, **kwargs):
            try:
                token = self.get_token_auth_header(kwargs["request"])
                url = f'https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys'

                async with httpx.AsyncClient() as client:
                    resp: Response = await client.get(url)
                    if resp.status_code != 200:
                        raise AuthError(
                            "Problem with Azure AD discovery URL", status_code=404)

                    jwks = resp.json()
                    unverified_header = jwt.get_unverified_header(token)
                    rsa_key = {}
                    for key in jwks["keys"]:
                        if key["kid"] == unverified_header["kid"]:
                            rsa_key = {
                                "kty": key["kty"],
                                "kid": key["kid"],
                                "use": key["use"],
                                "n": key["n"],
                                "e": key["e"]
                            }
            except Exception:
                return fastapi.Response(content="Invalid_header: Unable to parse authentication", status_code=401)
            if rsa_key:
                try:
                    token_version = self.__get_token_version(token)
                    self.__decode_JWT(token_version, token, rsa_key)
                    return await f(*args, **kwargs)
                except AuthError as auth_err:
                    fastapi.Response(content=auth_err.error_msg,
                                    status_code=auth_err.status_code)
            return fastapi.Response(content="Invalid header error: Unable to find appropriate key", status_code=401)
        return decorated

    def __decode_JWT(self, token_version, token, rsa_key):
        if token_version == "1.0":
            _issuer = f'https://sts.windows.net/{tenant_id}/'
            _audience = f'{client_id}'
        else:
            _issuer = f'https://login.microsoftonline.com/{tenant_id}/v2.0'
            _audience = f'{client_id}'
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=_audience,
                issuer=_issuer
            )
            print(payload)
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError("Token error: The token has expired", 401)
        except jwt.JWTClaimsError:
            raise AuthError(
                "Token error: Please check the audience and issuer", 401)
        except Exception as e:
            raise AuthError("Token error: Unable to parse authentication", 401)


    def __get_token_version(self, token):
        unverified_claims = jwt.get_unverified_claims(token)
        if unverified_claims.get("ver"):
            return unverified_claims["ver"]
        else:
            raise AuthError(
                "Missing version claim from token. Unable to validate", 403)