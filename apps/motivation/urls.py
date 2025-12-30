from django.urls import path
from .views import MotivationFeedView, MotivationDetailView

urlpatterns = [
    path("motivation/", MotivationFeedView.as_view()),
    path("motivation/<int:pk>/", MotivationDetailView.as_view()),
]
