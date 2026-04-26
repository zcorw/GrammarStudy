from __future__ import annotations

import hashlib
import hmac
import secrets


class PasswordHasher:
    iterations = 600_000

    @classmethod
    def hash_password(cls, password: str) -> str:
        salt = secrets.token_hex(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            cls.iterations,
        )
        return f"pbkdf2_sha256${cls.iterations}${salt}${digest.hex()}"

    @classmethod
    def verify_password(cls, password: str, stored_hash: str | None) -> bool:
        if not stored_hash:
            return False

        try:
            algorithm, iterations_raw, salt, expected = stored_hash.split("$", 3)
        except ValueError:
            return False

        if algorithm != "pbkdf2_sha256":
            return False

        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            int(iterations_raw),
        )
        return hmac.compare_digest(digest.hex(), expected)
