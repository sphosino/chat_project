# chat/signals.py
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import ChatMessage, ChatRoom, ChatImage
import os
import threading

@receiver(post_save, sender=ChatMessage)
def my_model_post_save(sender, instance, created, **kwargs):
    if created:
        print(f"新しい ChatMessage オブジェクトが作成されました: {instance}")
    else:
        print(f"ChatMessage オブジェクトが更新されました: {instance}")

@receiver(post_delete, sender=ChatImage)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        print("画像あり")
        try:
            instance.image.delete(save=False)
        except Exception as e:
            print("画像削除失敗（無視）:", e)

    if hasattr(instance, "thumbnail") and instance.thumbnail:
        print("サムネあり")
        try:
            instance.thumbnail.delete(save=False)
        except Exception as e:
            print("サムネ削除失敗（無視）:", e)

@receiver(post_delete, sender=ChatMessage)
def delete_chatMessage(sender, instance, **kwargs):
    print("メッセージ削除")
    if instance.image:
        try:
            instance.image.delete()
        except Exception as e:
            print("ChatImage削除失敗:", e)
        
@receiver(post_delete, sender= ChatRoom)
def delete_chat_room(sender, instance, **kwargs):
    print("部屋が削除された")