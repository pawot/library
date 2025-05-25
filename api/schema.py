import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension
from strawberry_django import field
from django.shortcuts import get_object_or_404

from accounts.models import User
from accounts.types import UserType, create_user, update_user, delete_user


@strawberry.type
class Query:
    users: list[UserType] = field()

    @strawberry.field
    def user(self, id: strawberry.ID) -> UserType:
        return get_object_or_404(User, id=id)


@strawberry.type
class Mutation:
    create_user = create_user
    update_user = update_user
    delete_user = delete_user


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
