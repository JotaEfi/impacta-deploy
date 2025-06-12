from rest_framework import serializers
from api.models import Faq
from users.models import userType

class faqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = ['id', 'org_user', 'question']  # Mantendo apenas campos essenciais
        read_only_fields = ['org_user']

    def to_representation(self, instance):
        """
        Sobrescrevendo to_representation para tratar campos ausentes de forma segura
        """
        try:
            data = {
                'id': instance.id if hasattr(instance, 'id') else None,
                'org_user': instance.org_user.id if hasattr(instance, 'org_user') and instance.org_user else None,
                'question': instance.question if hasattr(instance, 'question') else '',
            }
            
            # Tentando adicionar campos opcionais de forma segura
            try:
                data['answer'] = getattr(instance, 'answer', '')
            except:
                data['answer'] = ''
                
            try:
                data['date'] = getattr(instance, 'date', None)
            except:
                data['date'] = None
                
            return data
            
        except Exception as e:
            return {
                'id': None,
                'org_user': None,
                'question': '',
                'answer': '',
                'date': None
            }

    def validate_question(self, value):
        if not value.strip():
            raise serializers.ValidationError("A pergunta não pode estar em branco.")
        return value

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            if request.user.user_type != userType.ONG:
                raise serializers.ValidationError("Apenas ONGs podem criar ou responder FAQs.")
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['org_user'] = request.user
        return super().create(validated_data)