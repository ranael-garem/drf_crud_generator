# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import Context, Template

from ..utils import get_file_name, get_instance_name


class Command(BaseCommand):
    """Author: Rana El-Garem."""

    help = ''

    def add_arguments(self, parser):
        parser.add_argument('model')
        parser.add_argument('app_name')

    def handle(self, *args, **options):
        model_name = options['model']
        app_name = options['app_name']
        app_directory = os.path.join(settings.BASE_DIR, app_name)

        self.delete_file(app_directory, "model", model_name)
        self.delete_file(app_directory, "serializer", model_name)
        self.delete_file(app_directory, "view", model_name)
        self.remove_view_from_urls(model_name, app_name)
        # path = os.path.join(
        #     settings.TEST_APP, 'urls.py')
        # os.remove(path)

        self.stdout.write(self.style.SUCCESS('Successfully called command'))

    def delete_file(self, app_directory, instance_type, model_name):
        """ Delete file """
        file_name = get_file_name(instance_type, model_name)
        instance_name = get_instance_name(instance_type, model_name)
        dir_name = '%ss' % (instance_type)
        path = os.path.join(
            app_directory, dir_name, file_name + '.py')
        os.remove(path)

        path = os.path.join(
            app_directory, dir_name, '__init__.py')
        target = 'from .%s import %s \n' % (file_name, instance_name)
        self.remove_line_from_file(path, target)
        self.stdout.write(self.style.SUCCESS(
            'Successfully deleted %s' % (type)))

    def remove_view_from_urls(self, model_name, app_name):
        app_directory = os.path.join(os.getcwd(), app_name)
        urls_path = os.path.join(app_directory, 'urls.py')

        base_name = model_name.lower() + 's'
        register_line = "router.register('{0}', views.{1}, base_name='{0}')\n".format(
            base_name, get_instance_name('view', model_name))
        self.remove_line_from_file(urls_path, register_line)

    def remove_line_from_file(self, path, target):
        """ Remove line from a file given its path """
        try:
            init_file = open(path, "r+")
        except:
            return
        lines = init_file.readlines()
        init_file.seek(0)
        for i in lines:
            if i != target:
                init_file.write(i)
        init_file.truncate()
        init_file.close()
