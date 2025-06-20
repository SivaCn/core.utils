# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
import os

from typing import List, Optional, Any, Tuple
from datetime import datetime, timedelta, UTC
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
import strawberry

from jwcrypto import jwk, jwe
from jose import JWTError
from fastapi import HTTPException
from passlib.context import CryptContext

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.helpers.utils import (
    json_serialize,
    json_deserialize,
)

from core.utils.constants import const_secrets

from core.utils.helpers.environ import get_build_path

from core.utils.helpers.store import set_to_store, fetch_from_store
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


build_path = get_build_path()
STORE_PUBLIC_PEM_KEY = 'JWT-RSA-PUBLIC-PEM-KEY'
STORE_PRIVATE_PEM_KEY = 'JWT-RSA-PRIVATE-PEM-KEY'


class RSA:

    @classmethod
    def generate_keys(cls):

        # Generate a new RSA key pair (2048-bit for strong security)
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        # Serialize private key (PEM format)
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Serialize public key (PEM format)
        public_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        #
        # Set the Public and Private keys to store, which expires after 7 days (i.e., 604800 seconds)
        set_to_store(public_pem, key=STORE_PUBLIC_PEM_KEY, expires_after=604800)
        set_to_store(private_pem, key=STORE_PRIVATE_PEM_KEY, expires_after=604800)

        return private_pem, public_pem

    @classmethod
    def load_or_generate_keys(cls):

        public_pem = fetch_from_store(key=STORE_PUBLIC_PEM_KEY)
        private_pem = fetch_from_store(key=STORE_PRIVATE_PEM_KEY)

        if not public_pem or not private_pem:
            private_pem, public_pem = cls.generate_keys()

        return private_pem.encode(), public_pem.encode()

    @classmethod
    def get_rsa_keys(cls):
        return cls.load_or_generate_keys()


class JWT:

    # Prepare protected header
    PROTECTED_HEADER = {
        "alg": "RSA-OAEP-256",      # Key encryption algorithm
        "enc": "A256GCM",           # Content encryption
        "typ": "JWT",               # Token type
        "cty": "application/json"   # Content type
    }

    def __init__(self):

        private_pem, public_pem = RSA.get_rsa_keys()

        self.private_key = jwk.JWK.from_pem(private_pem)
        self.public_key = jwk.JWK.from_pem(public_pem)

    def json_to_compact(self, jwe_as_dict):
        return (
            f"{jwe_as_dict['protected']}."
            f"{jwe_as_dict['encrypted_key']}."
            f"{jwe_as_dict['iv']}."
            f"{jwe_as_dict['ciphertext']}."
            f"{jwe_as_dict['tag']}"
        )

    def create_access_token(self, custom_claims: dict) -> str:

        # Standard claims
        payload = {
            # "sub": "App Access",
            # "iss": "Get Yellow",
            # "aud": "End User",
            "exp": int(
                (
                    datetime.now(UTC) + timedelta(minutes=const_secrets.JWT_TOKEN_EXPIRE_AFTER_MINUTES)
                 ).timestamp()
            ),
            "iat": int(datetime.now(UTC).timestamp()),
            "nbf": int(datetime.now(UTC).timestamp()),
            #
            # Add the Custom Claims as well.
            **custom_claims,
        }

        # Create JWE token
        token = jwe.JWE(
            plaintext=json_serialize(payload).encode('utf-8'),
            protected=self.PROTECTED_HEADER,
            recipient=self.public_key
        )

        return self.json_to_compact(
            json_deserialize(
                token.serialize()
            )
        )

    def decode_token(self, token: str) -> Any:

        from web.backend.common import BaseDataClass

        # JWT Authentication
        @strawberry.type
        class TokenData(BaseDataClass):
            admin_slug: Optional[str] = None
            user_slug: Optional[str] = None
            email: Optional[str] = None
            roles: Optional[List[str]] = None

            def __init__(self, **kwargs):
                super(TokenData, self).__init__(**kwargs)

        jwe_token = jwe.JWE()
        jwe_token.deserialize(token)
        jwe_token.decrypt(self.private_key)
        jwe_token.payload.decode('utf-8')

        payload = json_deserialize(jwe_token.payload.decode('utf-8'))

        if 'admin_slug' not in payload and 'user_slug' not in payload:
            raise HTTPException(status_code=401, detail="Invalid token, required user details are missing")

        return TokenData(**payload)


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

