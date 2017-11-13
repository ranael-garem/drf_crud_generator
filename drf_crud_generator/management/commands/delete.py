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
        # parser.add_argument(
        #     '--app', '-a', action='store', dest='app_name',
        #     help='The app to create files in')

    def handle(self, *args, **options):
        model_name = options['model']
        app_name = options['app_name']
        app_directory = os.path.join(settings.BASE_DIR, app_name)

        self.delete_file(app_directory, "model", model_name)
        self.delete_file(app_directory, "serializer", model_name)
        self.delete_file(app_directory, "view", model_name)

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
        self.remove_from_init(path, target)
        self.stdout.write(self.style.SUCCESS(
            'Successfully deleted %s' % (type)))

    def remove_from_init(self, path, target):
        """ Remove import from __init__.py """
        init_file = open(path, "r+")
        lines = init_file.readlines()
        init_file.seek(0)
        for i in lines:
            if i != target:
                init_file.write(i)
        init_file.truncate()
        init_file.close()
