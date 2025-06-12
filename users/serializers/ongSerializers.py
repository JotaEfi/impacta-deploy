git add .git add .# serializers.py
from rest_framework import serializers
from users.models import Ong, CustomUser
from api.models import Necessity, Post, Faq, Donation, Avaliation
from api.serializers.NecessitySerializers import NecessitySerializer
from api.serializers.PostsSerializers import PostSerializers
from api.serializers.faqSerializer import faqSerializer

class OngUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'city', 'state', 'address', 'postal_code']

class OngSerializer(serializers.ModelSerializer):
    user = OngUserSerializer(read_only=True)
    necessities = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()
    faqs = serializers.SerializerMethodField()
    donations = serializers.SerializerMethodField()
    avaliations = serializers.SerializerMethodField()
    total_donations = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Ong
        fields = [
            'id', 'user', 'name', 'description', 'created_at',
            'necessities', 'posts', 'faqs', 'donations', 'avaliations',
            'total_donations', 'average_rating'
        ]

    def get_necessities(self, obj):
        try:
            necessities = Necessity.objects.filter(org=obj)
            return NecessitySerializer(necessities, many=True).data
        except Exception:
            return []

    def get_posts(self, obj):
        try:
            posts = Post.objects.filter(org_user=obj.user)
            return PostSerializers(posts, many=True).data
        except Exception:
            return []

    def get_faqs(self, obj):
        try:
            faqs = Faq.objects.filter(org_user=obj.user)
            return faqSerializer(faqs, many=True).data
        except Exception:
            return []

    def get_donations(self, obj):
        try:
            donations = Donation.objects.filter(org=obj).values('id', 'date')
            return [{
                'id': donation['id'],
                'item': self._get_item_name(donation['id']),
                'donor': self._get_donor_username(donation['id']),
                'date': donation['date']
            } for donation in donations]
        except Exception:
            return []
    
    def _get_item_name(self, donation_id):
        try:
            donation = Donation.objects.get(id=donation_id)
            return donation.item.name if donation.item else None
        except Exception:
            return None
    
    def _get_donor_username(self, donation_id):
        try:
            donation = Donation.objects.get(id=donation_id)
            return donation.donor.username if donation.donor else None
        except Exception:
            return None

    def get_avaliations(self, obj):
        try:
            avaliations = Avaliation.objects.filter(org=obj)
            return [{
                'id': avaliation.id,
                'donor': avaliation.donor.username if avaliation.donor else None,
                'comment': avaliation.comment,
                'date': avaliation.date
            } for avaliation in avaliations]
        except Exception:
            return []

    def get_total_donations(self, obj):
        try:
            return Donation.objects.filter(org=obj).count()
        except Exception:
            return 0

    def get_average_rating(self, obj):
        try:
            avaliations = Avaliation.objects.filter(org=obj)
            if not avaliations.exists():
                return None
            return None
        except Exception:
            return None