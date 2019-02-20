from django.test import TestCase
from django.utils import timezone
from hello_django.models import User


class UserTestCase(TestCase):

    def setUp(self) -> None:
        print('test up')
        now = timezone.now()
        user = User(username='admin', password='123456', real_name='admin', email='aaa@test.com', update_time=now,
                    create_time=now)
        user.save()

    def test_get_all(self):
        print(User.objects.get(username='admin'))

    def tearDown(self):
        print('test down')
