from cms_app.API.views import UserAPIView, PostAPIView, LikeAPIView, GetPostsListAPI
from django.urls import path

app_name = 'cms_app'
urlpatterns = [
    path("user/add", UserAPIView.as_view(), name = "add-user"),
    path("user/get/<int:id>/", UserAPIView.as_view(), name = "get-user"),
    path("user/update/<int:id>/", UserAPIView.as_view(), name = "update-user"),
    path("user/delete/<int:id>/", UserAPIView.as_view(), name = "delete-user"),

    path("post/add", PostAPIView.as_view(), name = "add-post"),
    path("post/get/<int:id>/", PostAPIView.as_view(), name = "get-post"),
    path("post/<int:post_id>/update/<int:user_id>/", PostAPIView.as_view(), name = "update-post"),
    path("post/<int:post_id>/delete/<int:user_id>/", PostAPIView.as_view(), name = "delete-post"),

    path("like/add", LikeAPIView.as_view(), name = "add-like"),
    path("like/get/<int:id>/", LikeAPIView.as_view(), name = "get-like"),
    path("like/update/<int:id>/", LikeAPIView.as_view(), name = "update-like"),
    path("like/delete/<int:id>/", LikeAPIView.as_view(), name = "delete-like"),

    path("posts-list/get/<int:user_id>/", GetPostsListAPI.as_view(), name = "get-posts-list"),
   
]
