""" Test for crud command """
import sys
from django.test import TestCase
from django.conf import settings
from django.apps import apps
from django.core.management import call_command

class CrudCommandTest(TestCase):
    """Author: Rana El-Garem. """

    def setUp(self):
        self.app = settings.TEST_APP
        self.model = settings.TEST_MODEL
        call_command('crud', self.model, self.app)

    def test_end_to_end(self):
        """ Test that the model created can be called and initialized """
        reload(sys.modules['main.models'])
        model = apps.get_model(self.app, self.model)
        model.objects.create()
        self.assertEqual(model.objects.all().count(), 1)

    def tearDown(self):
        call_command('delete', self.model, self.app)
