from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from api.models import Item
from api.serializers.ItemSerializers import ItemSerializers
import logging

logger = logging.getLogger('api')

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializers
    permission_classes = [AllowAny]  # Permitindo acesso sem autenticação

    def get_queryset(self):
        try:
            return Item.objects.all()
        except Exception as e:
            logger.error(f"Erro ao buscar itens: {str(e)}")
            return Item.objects.none()

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        if user:
            logger.info(f"Usuário {user} criou um novo item.")
        else:
            logger.info("Item criado por usuário não autenticado.")
        serializer.save()

