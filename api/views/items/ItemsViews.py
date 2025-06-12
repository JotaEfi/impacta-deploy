from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.models import Item
from api.serializers.ItemSerializers import ItemSerializers
from django.db import connection
import logging

logger = logging.getLogger('api')

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializers
    permission_classes = [AllowAny]  # Permitindo acesso sem autenticação

    def get_queryset(self):
        try:
            # Usando values() para selecionar apenas os campos que sabemos que existem
            # Isso evita que o ORM tente buscar a coluna 'quantity' que não existe
            return Item.objects.values('id', 'name', 'category')
        except Exception as e:
            logger.error(f"Erro ao buscar itens: {str(e)}")
            return Item.objects.none()
    
    def list(self, request, *args, **kwargs):
        try:
            # Implementação customizada do list para controlar melhor a serialização
            queryset = self.get_queryset()
            
            # Convertendo os dados para uma lista de objetos Item "mock" 
            # para compatibilidade com o serializer
            items_data = []
            for item_dict in queryset:
                # Criando um objeto mock do Item com apenas os campos seguros
                class MockItem:
                    def __init__(self, id, name, category):
                        self.id = id
                        self.name = name
                        self.category = category
                
                mock_item = MockItem(
                    id=item_dict['id'],
                    name=item_dict['name'], 
                    category=item_dict['category']
                )
                items_data.append(mock_item)
            
            serializer = self.get_serializer(items_data, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Erro ao listar itens: {str(e)}")
            return Response([], status=200)

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        if user:
            logger.info(f"Usuário {user} criou um novo item.")
        else:
            logger.info("Item criado por usuário não autenticado.")
        serializer.save()

