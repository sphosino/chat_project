from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from django.views import View
from accounts.models import PushSubscription
import json
from . import models
from asgiref.sync import sync_to_async
from .utils import handle_chat_message
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


import logging
logger = logging.getLogger(__name__)

from django.contrib.auth.mixins import AccessMixin


class AsyncLoginRequiredMixin(AccessMixin):
    @method_decorator(login_required)
    async def dispatch(self, request, *args, **kwargs):
        
        return await super().dispatch(request,*args, **kwargs)

class LobbyView(AsyncLoginRequiredMixin, View):
    async def get(self, request, *args, **kwargs):
        return await sync_to_async(render)(
            request,
            "lobby.html",
            {
                "VAPID_PUBLIC_KEY": settings.VAPID_PUBLIC_KEY
            }
        )

    
    async def post(self, request, roomid):
        logger.info('lobby_post')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            result = await handle_chat_message(request, roomid)
            return JsonResponse(result)
        return JsonResponse({'success':False, 'errors': 'Unexpected request'})



class RoomView(AsyncLoginRequiredMixin,View):

    async def get(self, request, roomid):
        room = await sync_to_async(get_object_or_404)(models.ChatRoom, id = roomid)
        return await sync_to_async(render)(request, "room.html", {"room":room})
    
    async def post(self, request, roomid):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            result = await handle_chat_message(request, roomid)
            return JsonResponse(result)
        return JsonResponse({'success':False, 'errors': 'Unexpected request'})
        

#サービスワーカーからの購読情報を保存するためのビュー
@login_required
def save_subscription(request):
    
    if request.method == "POST":
        data = json.loads(request.body)

        endpoint = data.get("endpoint")
        keys = data.get("keys", {})

        PushSubscription.objects.update_or_create(
            endpoint=endpoint,
            defaults={
                "user": request.user,
                "p256dh": keys.get("p256dh"),
                "auth": keys.get("auth"),
            }
        )
        print("subscription saved:", endpoint)

        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "invalid"}, status=400)