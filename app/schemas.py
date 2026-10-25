from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserCreate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        hide_input_in_errors=True,
    )

    name: str = Field(
        min_length=1,
        max_length=100,
        pattern=r"\S",
    )
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)

class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(
        min_length=1,
        max_length=100,
        pattern=r"\S",
    )


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr