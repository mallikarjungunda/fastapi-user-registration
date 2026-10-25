from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.database import SessionDependency
from app.models import User
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.security import hash_password


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def find_user(user_id: int, session: Session) -> User:
    user = session.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    payload: UserCreate,
    session: SessionDependency,
):
    # This application treats email addresses as case-insensitive.
    user = User(
        name=payload.name.strip(),
        email=str(payload.email).lower(),
        password_hash=hash_password(payload.password),
    )

    session.add(user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    session.refresh(user)
    return user


@router.get("", response_model=list[UserResponse])
def list_users(
    session: SessionDependency,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    statement = (
        select(User)
        .order_by(User.id)
        .offset(offset)
        .limit(limit)
    )

    return session.exec(statement).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    session: SessionDependency,
):
    return find_user(user_id, session)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserUpdate,
    session: SessionDependency,
):
    user = find_user(user_id, session)
    user.name = payload.name.strip()

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    session: SessionDependency,
):
    user = find_user(user_id, session)

    session.delete(user)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)