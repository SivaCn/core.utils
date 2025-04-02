# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
import os

from typing import List, Optional, Any, Tuple
from cryptography.fernet import Fernet
from datetime import datetime, timedelta, UTC
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
import strawberry

from jose import jwt, JWTError
from fastapi import HTTPException
from passlib.context import CryptContext
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.helpers.utils import (
    json_safe,
)

from core.utils.constants import const_auth

from core.utils.helpers.environ import get_build_config
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


general_config = get_build_config(section='general')
is_prod_env = (general_config.environment.lower() == 'prod')


class JWT:

    def __init__(self):
        if not const_auth.JWT_SECRECT_KEY or not const_auth.JWT_ALGORITHM:
            raise Exception("CRITICAL: Unable to read JWT related details")

        # fernet_key = Fernet.generate_key()
        self.cipher_suite = Fernet(os.getenv('FERNET_KEY'))

    def create_access_token(self, custom_claims: dict) -> str:

        # Standard claims
        payload = {
            # "sub": "App Access",
            # "iss": "Get Yellow",
            # "aud": "End User",
            "exp": int(
                (
                    datetime.now(UTC) + timedelta(minutes=const_auth.JWT_TOKEN_EXPIRE_AFTER_MINUTES)
                 ).timestamp()
            ),
            "iat": int(datetime.now(UTC).timestamp()),
            "nbf": int(datetime.now(UTC).timestamp()),
            #
            # Add the Custom Claims as well.
            **custom_claims,
        }

        token = jwt.encode(
            json_safe(payload),
            os.getenv('JWT_SECRET_KEY'),
            algorithm=os.getenv('JWT_ALGORITHM')
        )

        if is_prod_env:
            # Encrypt the token for additional security
            encrypted_token = self.cipher_suite.encrypt(token.encode())
            return encrypted_token.decode()

        return token

    def decode_token(self, token: str) -> Any:

        from web.backend.common import BaseDataClass

        # JWT Authentication
        @strawberry.type
        class TokenData(BaseDataClass):
            email: str
            user_slug: str
            roles: Optional[List[str]]=None

            def __init__(self, **kwargs):
                super(TokenData, self).__init__(**kwargs)

        try:
            if is_prod_env:
                # Decrypt the token
                token = self.cipher_suite.decrypt(token.encode())

            payload = jwt.decode(
                token,
                os.getenv('JWT_SECRET_KEY'),
                algorithms=[os.getenv('JWT_ALGORITHM')]
            )

            if not payload.get('user_slug'):
                raise HTTPException(status_code=401, detail="Invalid token, required details are missing")

            return TokenData(**payload)

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")


class Password:

    def __init__(self):

        # Configure password hashing
        self.pwd_context = CryptContext(
            schemes=["argon2", "bcrypt"],   # Prefer argon2, fallback to bcrypt
            deprecated="auto",
            argon2__memory_cost=102400,     # 100MB memory usage
            argon2__time_cost=3,            # 3 iterations
            argon2__parallelism=4           # Use 4 cores
        )

    def hash(self, password: str) -> Tuple[str, str]:
        """
        Hash a password for storage in the database.

        Args:
            password: The plaintext password to hash

        Returns:
            Tuple of (hashed_password, algorithm_used)
        """
        hashed = self.pwd_context.hash(password)

        # Extract the algorithm name from the hash string
        algorithm = hashed.split("$")[0]
        if algorithm == "argon2":
            algorithm = "argon2id"  # Standardize naming

        return hashed, algorithm

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hashed version.

        Args:
            plain_password: The password to verify
            hashed_password: The stored hash to compare against

        Returns:
            bool: True if password matches, False otherwise
        """
        return self.pwd_context.verify(plain_password, hashed_password)

