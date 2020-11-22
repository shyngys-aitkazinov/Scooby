from . import views
from rest_framework.routers import SimpleRouter
from django.urls import path

router = SimpleRouter()
router.register("posts", views.PostViewSet, "posts")

urlpatterns = [
    path('upload_file/', views.FileUploadView.as_view()),
]
urlpatterns += router.urls