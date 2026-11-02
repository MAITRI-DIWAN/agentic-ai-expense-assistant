from django.urls import path

from assistant.views import ExpenseAssistantView


urlpatterns = [
    path(
        "chat/",
        ExpenseAssistantView.as_view(),
        name="assistant-chat",
    ),
]