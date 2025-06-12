from rest_framework.exceptions import ValidationError  
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from api.models import Necessity
from api.serializers.NecessitySerializers import NecessityCreateUpdateSerializer, NecessitySerializer
from rest_framework.exceptions import PermissionDenied
import logging

logger = logging.getLogger('api')

class NecessityViewSet(viewsets.ModelViewSet):
    queryset = Necessity.objects.all()
    permission_classes = [AllowAny]  # Permitindo acesso sem autenticação para leitura

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return NecessityCreateUpdateSerializer
        return NecessitySerializer

    def get_queryset(self):
        try:
            user = self.request.user
            if user.is_authenticated and hasattr(user, 'ong_profile'):
                logger.info(f"ONG {user.ong_profile} acessou suas necessidades.")
                return Necessity.objects.filter(org=user.ong_profile)
            else:
                # Para usuários não autenticados ou sem perfil de ONG, retorna todas as necessidades
                logger.info("Usuário não autenticado ou sem perfil de ONG acessou todas as necessidades.")
                return Necessity.objects.all()
        except Exception as e:
            logger.error(f"Erro ao buscar necessidades: {str(e)}")
            return Necessity.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            logger.warning("Tentativa de criação de necessidade por usuário não autenticado.")
            raise ValidationError({"detail": "Usuário não autenticado."})
        if not hasattr(user, 'ong_profile'):
            logger.warning(f"Usuário {user} tentou criar necessidade sem estar associado a uma ONG.")
            raise ValidationError({"detail": "Usuário não está associado a uma ONG."})
        logger.info(f"ONG {user.ong_profile} criou uma nova necessidade.")
        serializer.save(org=user.ong_profile)
