""" Test for crud command """
import sys
import os
import importlib

from django.test import TestCase
from django.conf import settings
from django.apps import apps
from django.core.management import call_command
from django.urls import reverse

from ..management.utils import create_file


class CrudCommandTest(TestCase):
    """Author: Rana El-Garem. """

    def setUp(self):
        self.app = settings.TEST_APP
        self.model = settings.TEST_MODEL

    def call_command(self):
        call_command('crud', self.model, self.app)
        importlib.reload(sys.modules['main.models'])
        importlib.reload(sys.modules['main.serializers'])
        importlib.reload(sys.modules['main.views'])

    def check_model_view_serializer_created_successfully(self):
        model = apps.get_model(self.app, self.model)
        model.objects.create()
        self.assertEqual(model.objects.all().count(), 1)

        serializers = importlib.import_module(self.app + '.serializers')
        self.assertTrue(
            hasattr(serializers, '{0}Serializer'.format(self.model)))

        views = importlib.import_module(self.app + '.views')
        self.assertTrue(
            hasattr(views, '{0}ViewSet'.format(self.model)))

    def test_end_to_end(self):
        """ 
        Test that the model created can be called and initialized
        Test View can be imported
        Test Serializer can be imported
        """
        self.call_command()
        self.check_model_view_serializer_created_successfully()

    def test_end_to_end_with_exisiting_urls_file_with_router_imported_and_initialized(self):
        self.create_url_file()
        self.call_command()

        self.check_model_view_serializer_created_successfully()

    def test_end_to_end_with_exisiting_urls_file_with_no_router(self):
        self.create_url_file_with_no_router()
        self.call_command()

        self.check_model_view_serializer_created_successfully()

    def create_url_file(self):
        app_directory = os.path.join(os.getcwd(), self.app)
        urls_path = os.path.join(app_directory, 'urls.py')
        context = {'app_name': self.app}
        from drf_crud_generator.management.commands.crud import Command
        command = Command()
        command.create_url_file(context, urls_path)
        importlib.reload(sys.modules['main'])
        importlib.reload(sys.modules['main.serializers'])
        importlib.reload(sys.modules['main.models'])

    def create_url_file_with_no_router(self):
        import drf_crud_generator as generator
        app_directory = os.path.join(os.getcwd(), self.app)
        urls_files_path = os.path.join(
            generator.__path__[0], 'tests', 'files', 'urls.py.tmpl')
        path_new = os.path.join(app_directory, 'urls.py')
        create_file(path_new, urls_files_path, {'app_name': self.app})
        importlib.reload(sys.modules['main'])
        importlib.reload(sys.modules['main.serializers'])
        importlib.reload(sys.modules['main.models'])

    def tearDown(self):
        call_command('delete', self.model, self.app)
        # Remove urls.py file
        path = os.path.join(settings.TEST_APP, 'urls.py')
        os.remove(path)

