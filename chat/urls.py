from django.urls import path
from .views import LobbyView,RoomView, save_subscription

app_name = "chat"

urlpatterns = [
	path('<int:roomid>/', RoomView.as_view(), name = "room"),
	path('lobby/', LobbyView.as_view(), name="lobby"),
	path('api/save-subscription/', save_subscription, name='save_subscription'),
]
