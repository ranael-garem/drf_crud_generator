# -*- coding: utf-8 -*-
import os

from importlib import import_module
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template import Context, Template

from ..utils import get_file_name, get_instance_name


class Command(BaseCommand):
    """Author: Rana El-Garem."""

    help = ''
    model_name = ''
    app_name = ''

    def add_arguments(self, parser):
        parser.add_argument('model')
        parser.add_argument('app_name')

    def handle(self, model, app_name, *args, **options):
        self.validate_app_name(app_name)
        self.validate_model_name(model)

        self.model_name = model
        self.app_name = app_name

        app_template = os.path.join(
            settings.BASE_DIR, 'generator', 'management', 'templates')
        app_directory = os.path.join(settings.BASE_DIR, self.app_name)

        context = {
            'name': self.model_name,
            'author': options['author']
        }

        self.create_instance(app_template, app_directory, 'model', context)
        self.create_instance(app_template, app_directory,
                             'serializer', context)
        self.create_instance(app_template, app_directory, 'view', context)

        self.stdout.write(self.style.SUCCESS('Successfully called command'))

    def create_instance(self, app_template, app_directory, instance_type, context):
        """ Creates an instance (model, serializer or view) """
        model_name = self.model_name
        dir_name = '%ss' % (instance_type)
        path_old = os.path.join(app_template, '%s.py.tmpl' % (instance_type))
        path_new = os.path.join(
            app_directory, dir_name, get_file_name(instance_type, model_name) + '.py')
        self.create_file(path_new, path_old, context)
        self.initialize_instance(os.path.join(
            app_directory, dir_name), instance_type)

    def create_file(self, path_new, path_old, context):
        """ Creates a new file from path_old to path_new """
        if path_new.endswith('.tmpl'):
            path_new = path_new[:-5]
        fp_old = open(path_old, 'r')
        fp_new = open(path_new, 'w')
        fp_new.write(Template(fp_old.read()).render(Context(context)))
        fp_old.close()
        fp_new.close()
        self.stdout.write(self.style.SUCCESS(
            'Successfully created %s' % (path_new)))

    def initialize_instance(self, dir_name, instance_type):
        """ Initializes created instance in __init__.py """
        file_name = get_file_name(instance_type, self.model_name)
        instance_name = get_instance_name(instance_type, self.model_name)
        path = os.path.join(dir_name, '__init__.py')
        init = open(path, 'a+')
        init.write('from .%s import %s \n' % (file_name, instance_name))
        init.close()

    def validate_model_name(self, name):
        """
        Check that the model name does not start with '_'
        https://docs.djangoproject.com/en/1.11/ref/checks/#models
        """
        if name.startswith('_') or name.endswith('_'):
            raise CommandError("The model name %s cannot start or end with an "
                               "underscore as it collides with the query lookup syntax"
                               % (name))

    def validate_app_name(self, app_name):
        """Check that app exists."""
        try:
            import_module(app_name)
        except ImportError:
            raise CommandError(
                "App '%s' could not be found. Is it in INSTALLED_APPS?" % app_name)
