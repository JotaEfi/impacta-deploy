from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Views já existentes
from api.views.posts.PostsViews import PostViewSet
from api.views.faq.faqViews import FaqViewsSet

# Novas views de doações
from api.views.necessityDonations.necessityDonationsView import NecessityViewSet
from api.views.donations.donationView import DonationViewSet
from api.views.PaymentInfo.PaymentInfoView import PaymentInfoViewSet
from api.views.DonationReport.donation_report_view import DonationReportViewSet
from api.views.Accountability.accountability_view import AccountabilityViewSet
from api.views.items.ItemsViews import ItemViewSet 

router = DefaultRouter()
# CRUD de posts (ONGs) (/api/posts/)
router.register(r'posts', PostViewSet, basename='post')
# CRUD de FAQs (perguntas e respostas) (/api/faqs/)
router.register(r'faqs', FaqViewsSet, basename='faq')
# CRUD de necessidades das ONGs (/api/necessities/)
router.register(r'necessities', NecessityViewSet, basename='necessity')
# CRUD de doações (/api/donations/)
router.register(r'donations', DonationViewSet, basename='donation')
# CRUD de informações de pagamento das ONGs (/api/payment-info/)
router.register(r'payment-info', PaymentInfoViewSet, basename='payment-info')
# CRUD de relatórios de doação (/api/donation-reports/)
router.register(r'donation-reports', DonationReportViewSet, basename='donation-report')
# CRUD de prestação de contas (/api/accountability/)
router.register(r'accountability', AccountabilityViewSet, basename='accountability')
# CRUD de itens (/api/items/)
router.register(r'items', ItemViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls)),
]
