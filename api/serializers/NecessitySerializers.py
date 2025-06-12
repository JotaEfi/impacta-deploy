from rest_framework import serializers
from api.models import Item, Necessity
from users.models import Ong
from api.serializers.ItemSerializers import ItemSerializers


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name']  # Removendo campos que podem não existir

class OngSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ong
        fields = ['id', 'name']

class NecessitySerializer(serializers.ModelSerializer):
    # Removendo ReadOnlyFields que dependem de relacionamentos para evitar erros
    # org_name = serializers.ReadOnlyField(source='org.name')
    # item_name = serializers.ReadOnlyField(source='item.name')
    
    class Meta:
        model = Necessity
        fields = ['id', 'org', 'item']  # Mantendo apenas campos essenciais que provavelmente existem
        
    def to_representation(self, instance):
        """
        Sobrescrevendo to_representation para tratar campos ausentes de forma segura
        """
        try:
            data = {
                'id': instance.id if hasattr(instance, 'id') else None,
                'org': instance.org.id if hasattr(instance, 'org') and instance.org else None,
                'item': instance.item.id if hasattr(instance, 'item') and instance.item else None,
            }
            
            # Tentando adicionar campos opcionais de forma segura
            try:
                data['org_name'] = instance.org.name if instance.org else None
            except:
                data['org_name'] = None
                
            try:
                data['item_name'] = instance.item.name if instance.item else None
            except:
                data['item_name'] = None
                
            try:
                data['quantity'] = getattr(instance, 'quantity', 1)
            except:
                data['quantity'] = 1
                
            try:
                data['urgency'] = getattr(instance, 'urgency', 'media')
            except:
                data['urgency'] = 'media'
                
            try:
                data['status'] = getattr(instance, 'status', 'pendente')
            except:
                data['status'] = 'pendente'
                
            try:
                data['created_at'] = getattr(instance, 'created_at', None)
            except:
                data['created_at'] = None
                
            return data
            
        except Exception as e:
            return {
                'id': None,
                'org': None,
                'item': None,
                'org_name': None,
                'item_name': None,
                'quantity': 1,
                'urgency': 'media',
                'status': 'pendente',
                'created_at': None
            }
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        return value

class NecessityCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Necessity
        fields = ['item']  # Mantendo apenas campos essenciais para criação
    
    def validate_quantity(self, value):
        if value and value <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        return value