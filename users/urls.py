from django.urls import path
from users.views.registerView import RegisterView  
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views.userStatusView import UserStatusView
from users.views.userProfileView import UserProfileView, ChangePasswordView
from users.views.ongView import OngDetailView, OngListView  

urlpatterns = [
    # Registro de usuário (POST /api/auth/register/)
    path('register/', RegisterView.as_view(), name='register'),
    # Login JWT (POST /api/auth/login/)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Refresh do token JWT (POST /api/auth/refresh/)
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Status do usuário autenticado (GET /api/auth/status/)
    path('status/', UserStatusView.as_view(), name='user_status'),
    # Perfil do usuário autenticado (GET /api/auth/profile/)
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    # Troca de senha (POST /api/auth/change-password/)
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    # Lista todas as ONGs (GET /api/auth/ongs/)
    path('ongs/', OngListView.as_view(), name='ong-list'),  
    # Detalhes de uma ONG (GET /api/auth/ongs/<id>/)
    path('ongs/<int:id>/', OngDetailView.as_view(), name='ong-detail')
]
