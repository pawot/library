from django.db import models

from shared.models import BaseModel
from accounts.models import User


class Author(BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class Publisher(BaseModel):
    name = models.CharField(max_length=255)


class Book(BaseModel):
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name="books")
    title = models.CharField(max_length=255)
    published_on = models.DateField()
    is_available = models.BooleanField(default=True)


class Borrowing(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowings")
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["book"],
                condition=models.Q(returned_at__isnull=True),
                name="unique_unreturned_borrowing_per_book"
            )
        ]
