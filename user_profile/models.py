from django.db import models
from django.contrib.auth import get_user_model
# CloudinaryFieldをインポート
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.TextField(default="よろしくお願いします", verbose_name="自己紹介")
    
    # ImageFieldからCloudinaryFieldに変更
    # transformationでリサイズ条件を指定（例：500x500の枠に収める）
    avatar = CloudinaryField(
        resource_type='image', 
        null=True, 
        blank=True, 
        folder='avatars/',
        transformation=[
            {'width': 200, 'height': 200, 'crop': 'limit'}
        ],
        verbose_name="アバター"
    )

    # 追加
    allow_notification = models.BooleanField(
        default=True,
        verbose_name="通知を受け取る"
    )
    
    def __str__(self):
        return self.user.account_id
        
