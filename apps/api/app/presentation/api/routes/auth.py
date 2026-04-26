from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

from app.infrastructure.container import Container
from app.presentation.api.errors import ApiError

router = APIRouter()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    invite_code: str | None = None


class RegisterResponse(BaseModel):
    user_id: int
    email: EmailStr
    access_state: str
    is_admin: bool
    approval_mode: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    user_id: int
    email: EmailStr
    access_state: str
    is_admin: bool
    approval_mode: str
    access_token: str
    token_type: str
    expires_in: int


@router.post("/register", response_model=RegisterResponse)
def register(payload: RegisterRequest) -> RegisterResponse:
    try:
        decision = Container.register_with_email(
            email=payload.email,
            password=payload.password,
            invite_code=payload.invite_code,
        )
    except ValueError as exc:
        raise ApiError(409, "email_already_registered", "Email already registered.") from exc
    return RegisterResponse(**decision.__dict__)


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    try:
        decision = Container.login_with_email(
            email=payload.email,
            password=payload.password,
        )
    except ValueError as exc:
        raise ApiError(401, "invalid_credentials", "Invalid login credentials.") from exc
    return LoginResponse(**decision.__dict__)
