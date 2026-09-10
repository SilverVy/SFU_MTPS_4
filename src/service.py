# Контекст: TokenService.generate_token() использует time.time() и os.getenv("TOKEN_LIFETIME_SEC")

import time
import os
import base64
import hashlib

class TokenService:
    def generate_token(self, user_id: str) -> str:
        timestamp = int(time.time())
        lifetime = int(os.getenv("TOKEN_LIFETIME_SEC", "3600"))
        payload = f"{user_id}:{timestamp + lifetime}"
        return base64.b64encode(payload.encode()).decode()

    def is_token_valid(self, token: str) -> bool:
        try:
            payload = base64.b64decode(token).decode()
            user_id, expiry = payload.split(":")
            return int(time.time()) < int(expiry)
        except:
            return False