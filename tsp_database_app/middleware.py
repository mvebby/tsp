import jwt
from datetime import datetime, timezone
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in [reverse('login'), reverse('logout')]:
            return self.get_response(request)
        # Пропускаем для эндпоинтов аутентификации и статики
        if request.path in [reverse('token_obtain_pair'), 
                          reverse('token_refresh'),
                          '/static/',
                          '/favicon.ico']:
            return self.get_response(request)

        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        # Если нет токенов - редирект на логин
        if not access_token and not refresh_token:
            return self._redirect_to_login(request)

        try:
            # Если есть access token - проверяем его
            if access_token:
                try:
                    decoded = jwt.decode(
                        access_token,
                        api_settings.SIGNING_KEY,
                        algorithms=[api_settings.ALGORITHM]
                    )
                    exp = decoded.get('exp')
                    
                    # Если токен не истек - добавляем в заголовок
                    if exp and datetime.now(timezone.utc) < datetime.fromtimestamp(exp, tz=timezone.utc):
                        request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
                        return self.get_response(request)
                    
                except jwt.ExpiredSignatureError:
                    logger.debug("Access token expired")
                except jwt.InvalidTokenError as e:
                    logger.warning(f"Invalid access token: {e}")

            # Если дошли сюда - нужно обновить токены
            if refresh_token:
                return self._refresh_tokens(request, refresh_token)
            
            return self._redirect_to_login(request)

        except Exception as e:
            logger.error(f"JWT middleware error: {e}")
            return self._redirect_to_login(request)

    def _refresh_tokens(self, request, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
            new_refresh = str(refresh) if api_settings.ROTATE_REFRESH_TOKENS else refresh_token

            # Обновляем заголовок запроса
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access}'
            
            # Получаем ответ от view
            response = self.get_response(request)
            
            # Устанавливаем новые куки
            response.set_cookie(
                'access_token',
                new_access,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds())
            )
            
            if api_settings.ROTATE_REFRESH_TOKENS:
                response.set_cookie(
                    'refresh_token',
                    new_refresh,
                    httponly=True,
                    secure=not settings.DEBUG,
                    samesite='Lax',
                    max_age=int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds())
                )
            
            return response

        except TokenError as e:
            logger.warning(f"Refresh token failed: {e}")
            return self._redirect_to_login(request)

    def _redirect_to_login(self, request):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response