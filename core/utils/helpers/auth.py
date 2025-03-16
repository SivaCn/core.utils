# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
from copy import deepcopy

from datetime import datetime, timedelta, UTC
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
from jose import jwt, JWTError
from fastapi import HTTPException
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.helpers.utils import (
    DotDict,
    json_safe,
)

from core.utls.constants import const_auth
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


class JWT:

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

        return jwt.encode(json_safe(payload), const_auth.JWT_SECRECT_KEY, algorithm=const_auth.JWT_ALGORITHM)

    def decode_token(self, token: str) -> DotDict:

        try:
            payload = jwt.decode(token, const_auth.JWT_SECRECT_KEY, algorithms=[const_auth.JWT_ALGORITHM])

            if not payload.get("unique_id"):
                raise HTTPException(status_code=401, detail="Invalid token")

            return DotDict(payload)

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

