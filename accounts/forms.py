from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class SignUpForm(UserCreationForm):
	class Meta:
		model = CustomUser
		fields = (
			'account_id',
		)
	def __init__(self, *args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['password1'].help_text = "あなたの他の個人情報と似ているパスワードにはできません。\nパスワードは最低 8 文字以上必要です。\nよく使われるパスワードにはできません。\n数字だけのパスワードにはできません。"
		self.fields['account_id'].help_text = "アカウント名"

class LoginForm(AuthenticationForm):
	class Meta:
		model = CustomUser