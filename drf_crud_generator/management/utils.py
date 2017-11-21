import os
import re
from django.template import Context, Template


def create_file(path_new, path_old, context):
    """ Creates a new file from path_old to path_new """
    fp_old = open(path_old, 'r')
    fp_new = open(path_new, 'w')
    fp_new.write(Template(fp_old.read()).render(Context(context)))
    fp_old.close()
    fp_new.close()
    return "Successfully created %s" % (path_new)


def convert_camelcase_to_snakecase(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def get_file_name(instance_type, model_name):
    """ Returns file name based on type. """
    model_name = convert_camelcase_to_snakecase(model_name)
    if instance_type == "model":
        file_name = '%s' % (model_name.lower())
    elif instance_type == "serializer":
        file_name = '%s_serializer' % (model_name.lower())
    elif instance_type == "view":
        file_name = '%s_viewset' % (model_name.lower())
    return file_name


def get_instance_name(instance_type, model_name):
    """ Returns instance name. """
    if instance_type == "model":
        instance_name = model_name
    elif instance_type == "serializer":
        instance_name = '%sSerializer' % (model_name)
    elif instance_type == "view":
        instance_name = '%sViewSet' % (model_name)
    return instance_name


def write_to_file(path, lines):
    file = open(path, 'w')
    for line in lines:
        file.write(line)
    file.close()


def check_file_exists(path):
    return os.path.isfile(path)
