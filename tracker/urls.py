from django.urls import path

from .views import GetTweetsView

urlpatterns = [
    path('get-user-tweets/<str:username>', GetTweetsView.as_view()),
]
