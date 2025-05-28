from pydantic import BaseModel


class LoginSchema(BaseModel):
    login: str
    password: str


class ResetPasswordSchema(BaseModel):
    password: str
    password2: str


class EmailSchema(BaseModel):
    email: str
