import datetime
import hashlib
import hmac
import time
import json
import base64
from typing import Optional
from django.apps import apps

# c.f. https://thuse-course.github.io/course-index/basic/jwt/#jwt
# !Important! Change this to your own salt, better randomly generated!"
SALT = ("KawaiiNana" + datetime.datetime.now().strftime("%Y%m%d%H%M")).encode("utf-8")
EXPIRE_IN_SECONDS = 60 * 60  * 24 * 1  # 1 day
REFRESH_EXPIRE_IN_SECONDS = 60 * 60 * 24 * 7  # 7 days for refresh token

ALT_CHARS = "-_".encode("utf-8")


def b64url_encode(s):
    if isinstance(s, str):
        return base64.b64encode(s.encode("utf-8"), altchars=ALT_CHARS).decode("utf-8")
    else:
        return base64.b64encode(s, altchars=ALT_CHARS).decode("utf-8")

def b64url_decode(s: str, decode_to_str=True):
    if decode_to_str:
        return base64.b64decode(s, altchars=ALT_CHARS).decode("utf-8")
    else:
        return base64.b64decode(s, altchars=ALT_CHARS)


def generate_jwt_token(userID: int):
    # * header
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    # dump to str. remove `\n` and space after `:`
    header_str = json.dumps(header, separators=(",", ":"))
    # use base64url to encode, instead of base64
    header_b64 = b64url_encode(header_str)
    
    # * payload
    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + EXPIRE_IN_SECONDS,
        "data": {
            "userID": userID
            # And more data for your own usage
        }
    }
    payload_str = json.dumps(payload, separators=(",", ":"))
    payload_b64 = b64url_encode(payload_str)
    
    # * signature
    signature_raw = header_b64 + "." + payload_b64
    signature = hmac.new(SALT, signature_raw.encode("utf-8"), digestmod=hashlib.sha256).digest()
    signature_b64 = b64url_encode(signature)
    
    return header_b64 + "." + payload_b64 + "." + signature_b64


def check_jwt_token(token: str) -> Optional[dict]:
    # * Split token
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except:
        return None

    payload_str = b64url_decode(payload_b64)
    #TokenBlacklist = apps.get_model('users', 'TokenBlacklist')
    #if TokenBlacklist.objects.filter(token=token).exists():
    #    return None  # 令牌无效
    # * Check signature
    signature_str_check = header_b64 + "." + payload_b64
    signature_check = hmac.new(SALT, signature_str_check.encode("utf-8"), digestmod=hashlib.sha256).digest()
    signature_b64_check = b64url_encode(signature_check)
    
    if signature_b64_check != signature_b64:
        return None
    
    # Check expire
    payload = json.loads(payload_str)
    if payload["exp"] < time.time():
        return None
    
    return payload["data"]
    
# def generate_token(userID: str, token_type: str = "access"):
#     # Determine expiration based on token type
#     if token_type == "access":
#         expire_in_seconds = EXPIRE_IN_SECONDS
#     elif token_type == "refresh":
#         expire_in_seconds = REFRESH_EXPIRE_IN_SECONDS
#     else:
#         raise ValueError("Unsupported token type")
    
#     # Common payload
#     payload = {
#         "iat": int(time.time()),
#         "exp": int(time.time()) + expire_in_seconds,
#         "data": {"userID": userID},
#         "type": token_type  # Add token type in the payload
#     }
#     payload_str = json.dumps(payload, separators=(",", ":"))
#     payload_b64 = b64url_encode(payload_str)
    
#     # Signature
#     signature_raw = payload_b64
#     signature = hmac.new(SALT, signature_raw.encode("utf-8"), digestmod=hashlib.sha256).digest()
#     signature_b64 = b64url_encode(signature)
    
#     return payload_b64 + "." + signature_b64

# def generate_jwt_tokens(userID: str):
#     access_token = generate_token(userID, "access")
#     refresh_token = generate_token(userID, "refresh")
#     return access_token, refresh_token

# def check_jwt_token(token: str, expected_type: str = "access") -> Optional[dict]:
#     try:
#         payload_b64, signature_b64 = token.split(".")
#     except ValueError:
#         return None

#     signature_check = hmac.new(SALT, payload_b64.encode("utf-8"), digestmod=hashlib.sha256).digest()
#     signature_b64_check = b64url_encode(signature_check)
    
#     if signature_b64_check != signature_b64:
#         return None
    
#     payload_str = b64url_decode(payload_b64)
#     payload = json.loads(payload_str)
    
#     # Check token type and expiration
#     if payload.get("type") != expected_type or payload["exp"] < time.time():
#         return None
    
#     return payload["data"]
