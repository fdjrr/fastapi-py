from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from .auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
  def __init__(self, auto_error: bool = True):
    super(JWTBearer, self).__init__(auto_error=auto_error)

  async def __call__(self, request: Request):
    credentials: OAuth2PasswordBearer = await super(JWTBearer, self).__call__(request)
    if (credentials):
      if (not credentials.scheme == 'Bearer'):
        raise HTTPException(
          status_code=403, detail='Invalid authentication scheme.')
      if (not self.verify_jwt(credentials.credentials)):
        raise HTTPException(
          status_code=403, detail='Invalid token or expired token.')
      return credentials.credentials
    else:
      raise HTTPException(status_code=403, detail='Invalid authorization code.')

  def verify_jwt(self, access_token: str) -> bool:
    isTokenValid: bool = False

    try:
      payload = decodeJWT(access_token)
    except:
      payload = None
    if payload:
      isTokenValid = True
    return isTokenValid
