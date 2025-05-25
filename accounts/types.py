import strawberry_django
from strawberry import auto
from django.shortcuts import get_object_or_404

from accounts.models import User


@strawberry_django.type(User, only=["id", "first_name", "last_name", "email", "username"])
class UserType:
    id: auto
    first_name: auto
    last_name: auto
    email: auto
    username: auto


@strawberry_django.input(User)
class CreateUserInput:
    first_name: auto
    last_name: auto
    email: auto
    username: auto
    password: auto


@strawberry_django.mutation
def create_user(input: CreateUserInput) -> UserType:
    return User.objects.create_user(**input.__dict__)


@strawberry_django.input(User, partial=True)
class UpdateUserInput:
    id: auto
    first_name: auto
    last_name: auto
    email: auto
    username: auto
    password: auto


@strawberry_django.mutation
def update_user(input: UpdateUserInput) -> UserType:
    user = get_object_or_404(User, id=input.id)
    for field, value in input.__dict__.items():
        if field != "password" and value is not None:
            setattr(user, field, value)

    if input.password:
        user.set_password(input.password)

    user.save()
    return user


@strawberry_django.input(User)
class DeleteUserInput:
    id: auto


@strawberry_django.mutation
def delete_user(input: DeleteUserInput) -> bool:
    user = get_object_or_404(User, id=input.id)
    user.delete()
    return True



