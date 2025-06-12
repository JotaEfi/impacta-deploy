from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from api.models import Faq
from api.serializers.faqSerializer import faqSerializer
from users.models import userType
import logging

logger = logging.getLogger('api')


class FaqViewsSet(viewsets.ModelViewSet):
    queryset = Faq.objects.all()
    serializer_class = faqSerializer
    permission_classes = [AllowAny]  # Permitindo acesso sem autenticação para leitura

    def get_queryset(self):
        try:
            return Faq.objects.all()
        except Exception as e:
            logger.error(f"Erro ao buscar FAQs: {str(e)}")
            return Faq.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            logger.warning("Tentativa de criação de FAQ por usuário não autenticado.")
            raise ValidationError("Usuário não autenticado.")
        if user.user_type != userType.ONG:
            logger.warning(f"Usuário {user} tentou criar FAQ sem permissão.")
            raise ValidationError("Apenas ONGs podem criar perguntas e respostas no FAQ.")
        logger.info(f"FAQ criado pela ONG {user}.")
        serializer.save(org_user=user)
