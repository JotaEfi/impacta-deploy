from rest_framework import serializers
from api.models import Item

class ItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'category']  # Removendo 'quantity' temporariamente para evitar erros de coluna ausente
        
    def to_representation(self, instance):
        try:
            data = super().to_representation(instance)
            # Tentando adicionar quantity apenas se a coluna existir
            try:
                data['quantity'] = instance.quantity
            except AttributeError:
                data['quantity'] = 0  # Valor padrão se o campo não existir
            return data
        except Exception as e:
            # Em caso de erro, retorna apenas os campos básicos
            return {
                'id': getattr(instance, 'id', None),
                'name': getattr(instance, 'name', ''),
                'category': getattr(instance, 'category', ''),
                'quantity': 0
            }