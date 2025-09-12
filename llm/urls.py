from django.urls import path
from .views import GymLLMView, gym_chat_page



urlpatterns = [
    path("chat/", gym_chat_page, name="gym_chat"),
    path("gym-llm/", GymLLMView.as_view(), name="gym-llm"),
]
