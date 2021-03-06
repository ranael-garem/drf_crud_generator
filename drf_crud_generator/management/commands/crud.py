# -*- coding: utf-8 -*-
import os
import sys

from importlib import import_module, reload
from django.core.management.base import BaseCommand, CommandError
from django.template import Context, Template

from rest_framework.routers import DefaultRouter, SimpleRouter

from ..utils import (
    get_file_name,
    get_instance_name,
    write_to_file,
    check_file_exists,
    create_file
)


class Command(BaseCommand):
    """Author: Rana El-Garem."""

    help = ''
    model_name = ''
    app_name = ''

    def add_arguments(self, parser):
        parser.add_argument('model')
        parser.add_argument('app_name')

        parser.add_argument(
            '-a', '--author', action='store', dest='author',
            default='Autogenerated by CRUD command',
            help="What is your name?",
        )

    def handle(self, model, app_name, *args, **options):
        self.validate_app_name(app_name)
        self.validate_model_name(model)

        self.model_name = model
        self.app_name = app_name

        context = {
            'name': self.model_name,
            'author': options['author'],
            'app_name': app_name
        }

        self.create_instance('model', context)
        self.create_instance('serializer', context)
        self.create_instance('view', context)
        self.add_view_to_urls(context)

        self.stdout.write(self.style.SUCCESS('Successfully called command'))

    def create_instance(self, instance_type, context):
        """ Creates an instance (model, serializer or view) """
        import drf_crud_generator as generator
        crud_template_dir = os.path.join(
            generator.__path__[0], 'management', 'templates')
        app_directory = os.path.join(os.getcwd(), self.app_name)

        model_name = self.model_name
        dir_name = '%ss' % (instance_type)
        path_old = os.path.join(
            crud_template_dir, '%s.py.tmpl' % (instance_type))
        path_new = os.path.join(
            app_directory, dir_name, get_file_name(instance_type, model_name) + '.py')

        file_created = create_file(path_new, path_old, context)
        self.initialize_instance(os.path.join(
            app_directory, dir_name), instance_type)

        self.stdout.write(self.style.SUCCESS(file_created))

    def initialize_instance(self, dir_name, instance_type):
        """ Initializes created instance in __init__.py """
        file_name = get_file_name(instance_type, self.model_name)
        instance_name = get_instance_name(instance_type, self.model_name)
        path = os.path.join(dir_name, '__init__.py')
        init = open(path, 'a+')
        init.write('from .%s import %s \n' % (file_name, instance_name))
        init.close()

    def add_view_to_urls(self, context):
        app_directory = os.path.join(os.getcwd(), self.app_name)
        urls_path = os.path.join(app_directory, 'urls.py')
        if not check_file_exists(urls_path):
            self.create_url_file(context, urls_path)
        else:
            self.initialize_router(urls_path)
        self.register_viewset_with_router(urls_path, context)

    def create_url_file(self, context, urls_path):
        import drf_crud_generator as generator
        crud_template_dir = os.path.join(
            generator.__path__[0], 'management', 'templates')

        path_old = os.path.join(
            crud_template_dir, 'urls.py.tmpl')
        path_new = urls_path
        create_file(path_new, path_old, context)

    def initialize_router(self, urls_path):
        reload(sys.modules['{0}.models'.format(self.app_name)])
        reload(sys.modules['{0}'.format(self.app_name)])
        self.urls_module = import_module(self.app_name + '.urls')

        def is_router_imported():
            return (
                hasattr(self.urls_module, 'DefaultRouter') or
                hasattr(self.urls_module, 'SimpleRouter'))

        def is_router_initialized():
            if hasattr(self.urls_module, 'router'):
                router = getattr(self.urls_module, 'router')
                return type(router) is DefaultRouter or type(router) is SimpleRouter
            return False

        if is_router_imported() and is_router_initialized():
            return

        url_file = open(urls_path, 'r')
        lines = url_file.readlines()

        if not is_router_imported():
            lines.insert(
                0, "from rest_framework.routers import DefaultRouter\n")

        if not is_router_initialized():
            for index, line in enumerate(lines):
                if "urlpatterns" in line:
                    router = 'SimpleRouter' if hasattr(
                        self.urls_module, 'SimpleRouter') else 'DefaultRouter'
                    lines.insert(
                        index - 1, "router = {0}(trailing_slash=False)".format(router))
                    break
        url_file.close()

        write_to_file(urls_path, lines)

    def register_viewset_with_router(self, urls_path, context):
        base_name = self.model_name.lower() + 's'
        register_line = "router.register('{0}', views.{1}, base_name='{0}')\n".format(
            base_name, get_instance_name('view', self.model_name))
        url_file = open(urls_path, 'r')
        lines = url_file.readlines()
        for index, line in enumerate(lines):
            if "router = " in line:
                lines.insert(index + 1, register_line)
                break
        url_file.close()

        write_to_file(urls_path, lines)

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
