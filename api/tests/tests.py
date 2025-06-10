from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import Item, Donation, Avaliation, Post, Faq, Necessity, PaymentInfo, DonationReport, Accountability, Badge, DonorBadge
from users.models import CustomUser, Ong, userType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

class BasicApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_api_root(self):
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 404])  # Ajuste conforme seu endpoint root

class DonationModelTest(TestCase):
    def setUp(self):
        self.ong_user = CustomUser.objects.create_user(
            username='onguser', email='ong@example.com', password='Test123456!', user_type=userType.ONG)
        self.ong = Ong.objects.create(user=self.ong_user, name='ONG Teste')
        self.donor = CustomUser.objects.create_user(
            username='donoruser', email='donor@example.com', password='Test123456!', user_type=userType.DONOR)
        self.item = Item.objects.create(name='Arroz', category='Alimento', quantity=100)

    def test_create_donation(self):
        donation = Donation.objects.create(org=self.ong, item=self.item, donor=self.donor, quantity=10)
        self.assertEqual(donation.status, 'pendente')
        self.assertEqual(donation.quantity, 10)
        self.assertEqual(donation.org, self.ong)
        self.assertEqual(donation.donor, self.donor)

class AvaliationModelTest(TestCase):
    def setUp(self):
        self.ong_user = CustomUser.objects.create_user(username='ong2', email='ong2@example.com', password='Test123456!', user_type=userType.ONG)
        self.ong = Ong.objects.create(user=self.ong_user, name='ONG 2')
        self.donor = CustomUser.objects.create_user(username='donor2', email='donor2@example.com', password='Test123456!', user_type=userType.DONOR)

    def test_create_avaliation(self):
        aval = Avaliation.objects.create(org=self.ong, donor=self.donor, comment='Ótima ONG!')
        self.assertEqual(aval.org, self.ong)
        self.assertEqual(aval.donor, self.donor)
        self.assertEqual(aval.comment, 'Ótima ONG!')

class PostModelTest(TestCase):
    def setUp(self):
        self.ong_user = CustomUser.objects.create_user(username='ongpost', email='ongpost@example.com', password='Test123456!', user_type=userType.ONG)
        self.ong = Ong.objects.create(user=self.ong_user, name='ONG Post')
        self.donor = CustomUser.objects.create_user(username='donorpost', email='donorpost@example.com', password='Test123456!', user_type=userType.DONOR)

    def test_ong_can_create_post(self):
        post = Post(org_user=self.ong_user, description='Nova campanha')
        post.save()
        self.assertEqual(post.org_user, self.ong_user)

    def test_donor_cannot_create_post(self):
        with self.assertRaises(ValueError):
            post = Post(org_user=self.donor, description='Tentativa inválida')
            post.save()

class FaqModelTest(TestCase):
    def setUp(self):
        self.ong_user = CustomUser.objects.create_user(username='ongfaq', email='ongfaq@example.com', password='Test123456!', user_type=userType.ONG)
        self.ong = Ong.objects.create(user=self.ong_user, name='ONG FAQ')
        self.donor = CustomUser.objects.create_user(username='donorfaq', email='donorfaq@example.com', password='Test123456!', user_type=userType.DONOR)

    def test_ong_can_create_faq(self):
        faq = Faq(org_user=self.ong_user, question='Como doar?', answer='Via site')
        faq.save()
        self.assertEqual(faq.org_user, self.ong_user)

    def test_donor_cannot_create_faq(self):
        with self.assertRaises(ValueError):
            faq = Faq(org_user=self.donor, question='Tentativa?', answer='Não pode')
            faq.save()

class NecessityModelTest(TestCase):
    def setUp(self):
        self.ong_user = CustomUser.objects.create_user(username='ongnec', email='ongnec@example.com', password='Test123456!', user_type=userType.ONG)
        self.ong = Ong.objects.create(user=self.ong_user, name='ONG Nec')
        self.item = Item.objects.create(name='Feijão', category='Alimento', quantity=50)

    def test_create_necessity(self):
        nec = Necessity.objects.create(org=self.ong, item=self.item, quantity=20, urgency='alta')
        self.assertEqual(nec.status, 'pendente')
        self.assertEqual(nec.urgency, 'alta')
        self.assertEqual(nec.org, self.ong)

class BadgeModelTest(TestCase):
    def setUp(self):
        self.donor = CustomUser.objects.create_user(username='donorbadge', email='donorbadge@example.com', password='Test123456!', user_type=userType.DONOR)
        self.badge = Badge.objects.create(name='Primeira Doação', description='Primeira doação realizada', icon=SimpleUploadedFile('badge.png', b'filecontent'))

    def test_award_badge(self):
        donor_badge = DonorBadge.objects.create(donor=self.donor, badge=self.badge)
        self.assertEqual(donor_badge.donor, self.donor)
        self.assertEqual(donor_badge.badge, self.badge)

class PaymentInfoModelTest(TestCase):
    def setUp(self):
        self.ong_user = CustomUser.objects.create_user(username='ongpay', email='ongpay@example.com', password='Test123456!', user_type=userType.ONG)
        self.ong = Ong.objects.create(user=self.ong_user, name='ONG Pay')

    def test_create_payment_info(self):
        pay = PaymentInfo.objects.create(org=self.ong, pix_key='123456', bank='Banco X', agency='0001', account='12345-6')
        self.assertEqual(pay.org, self.ong)
        self.assertEqual(pay.pix_key, '123456')
        self.assertEqual(pay.bank, 'Banco X')

class DonationReportModelTest(TestCase):
    def setUp(self):
        self.ong_user = CustomUser.objects.create_user(username='ongrep', email='ongrep@example.com', password='Test123456!', user_type=userType.ONG)
        self.ong = Ong.objects.create(user=self.ong_user, name='ONG Rep')
        self.donor = CustomUser.objects.create_user(username='donorrep', email='donorrep@example.com', password='Test123456!', user_type=userType.DONOR)
        self.item = Item.objects.create(name='Macarrão', category='Alimento', quantity=30)
        self.donation = Donation.objects.create(org=self.ong, item=self.item, donor=self.donor, quantity=5)

    def test_create_report(self):
        report = DonationReport.objects.create(donation=self.donation, confirmed=True, message='Recebido!')
        self.assertEqual(report.donation, self.donation)
        self.assertTrue(report.confirmed)
        self.assertEqual(report.message, 'Recebido!')

class AccountabilityModelTest(TestCase):
    def setUp(self):
        self.ong_user = CustomUser.objects.create_user(username='ongacc', email='ongacc@example.com', password='Test123456!', user_type=userType.ONG)
        self.ong = Ong.objects.create(user=self.ong_user, name='ONG Acc')
        self.img = SimpleUploadedFile('prestacao.png', b'filecontent')

    def test_create_accountability(self):
        acc = Accountability.objects.create(org=self.ong, title='Prestação 1', description='Transparência', image=self.img)
        self.assertEqual(acc.org, self.ong)
        self.assertEqual(acc.title, 'Prestação 1')
        self.assertEqual(acc.description, 'Transparência')

class ApiEndpointsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/users/register/'
        self.login_url = '/api/users/login/'
        self.ong_list_url = '/api/users/ongs/'
        self.user_data = {
            'email': 'apiuser@example.com',
            'username': 'apiuser',
            'password': 'Test123456!',
            'password2': 'Test123456!',
            'user_type': 'DONOR',
            'city': 'São Paulo',
            'state': 'SP',
            'address': 'Rua Teste, 123',
            'postal_code': '01000-000',
            'first_name': 'Api',
            'last_name': 'User'
        }

    def test_register_api(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('email', response.data)

    def test_login_api(self):
        self.client.post(self.register_url, self.user_data, format='json')
        login_data = {'email': 'apiuser@example.com', 'password': 'Test123456!'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user_type', response.data)
        self.access_token = response.data['access']

    def test_ong_list_api(self):
        response = self.client.get(self.ong_list_url)
        self.assertIn(response.status_code, [200, 403])  # 403 se protegido, 200 se público

    def test_protected_status_api(self):
        # Registro e login
        self.client.post(self.register_url, self.user_data, format='json')
        login_data = {'email': 'apiuser@example.com', 'password': 'Test123456!'}
        login_response = self.client.post(self.login_url, login_data, format='json')
        access_token = login_response.data['access']
        # Acesso autenticado
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/users/status/')
        self.assertEqual(response.status_code, 200)
        # Acesso sem autenticação
        self.client.credentials()
        response = self.client.get('/api/users/status/')
        self.assertEqual(response.status_code, 401)
