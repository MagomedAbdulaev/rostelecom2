import jwt
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model

User = get_user_model()

def jwt_required(view_func):
    """Проверка JWT токена из cookies и установка пользователя"""
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('access_token')
        if not token:
            return HttpResponseRedirect('/login_user/')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('user_id')
            
            # Получаем пользователя из базы данных
            try:
                user = User.objects.get(id=user_id)
                request.user = user  # Устанавливаем пользователя в request
            except User.DoesNotExist:
                return HttpResponseRedirect('/login_user/')
                
        except jwt.ExpiredSignatureError:
            return HttpResponseRedirect('/login_user/')
        except jwt.InvalidTokenError:
            return HttpResponseRedirect('/login_user/')
            
        return view_func(request, *args, **kwargs)
    return wrapper