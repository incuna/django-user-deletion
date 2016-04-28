import factory

from .models import User


class UserFactory(factory.DjangoModelFactory):
    name = factory.Sequence('User {}'.format)
    username = factory.Sequence('username{}'.format)
    email = factory.Sequence('email{}@incuna.com'.format)

    class Meta:
        model = User
