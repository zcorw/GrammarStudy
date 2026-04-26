from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticatedUser:
    id: int
    email: str
    access_state: str
    is_admin: bool


@dataclass(frozen=True)
class LoginDecision:
    user_id: int
    email: str
    access_state: str
    is_admin: bool
    approval_mode: str
    access_token: str
    token_type: str
    expires_in: int


@dataclass(frozen=True)
class RegistrationDecision:
    user_id: int
    email: str
    access_state: str
    is_admin: bool
    approval_mode: str
