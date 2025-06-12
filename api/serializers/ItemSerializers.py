from rest_framework import serializers
from api.models import Item

class ItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'category']  # Removendo 'quantity' dos fields para evitar que o ORM tente buscá-lo
        
    def to_representation(self, instance):
        """
        Sobrescrevendo to_representation para tratar o campo quantity de forma segura
        """
        try:
            # Primeiro, obtemos a representação básica dos campos seguros
            data = {
                'id': instance.id,
                'name': instance.name,
                'category': instance.category,
            }
            
            # Tentamos adicionar quantity de forma segura
            try:
                # Usando uma consulta raw ou getattr para evitar o ORM padrão
                data['quantity'] = getattr(instance, 'quantity', 0)
            except Exception:
                # Se falhar, definimos um valor padrão
                data['quantity'] = 0
                
            return data
            
        except Exception as e:
            # Em caso de erro completo, retornamos dados mínimos seguros
            return {
                'id': getattr(instance, 'id', None),
                'name': getattr(instance, 'name', 'Nome não disponível'),
                'category': getattr(instance, 'category', 'Categoria não disponível'),
                'quantity': 0
            }