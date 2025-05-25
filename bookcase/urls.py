from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bookcase import views

router = DefaultRouter()
router.register("books", views.BookViewSet, basename="books")
router.register("borrowings", views.BorrowingViewSet, basename="borrowings")
router.register("authors", views.AuthorViewSet, basename="authors")
router.register("publishers", views.PublisherViewSet, basename="publishers")


urlpatterns = [
    path('', include(router.urls)),
]
