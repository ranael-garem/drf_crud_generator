def get_file_name(instance_type, model_name):
    """ Returns file name based on type. """
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
