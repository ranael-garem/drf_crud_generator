""" Test for validating arguments given in command."""
from django.test import TestCase
from django.conf import settings
from django.core.management.base import CommandError
from drf_crud_generator.management.commands import crud


class ValidateArgumentsTestCase(TestCase):
    """
    Test Validation of arguments of command 'crud'
    1. model_name
    Author: Rana El-Garem.
    """

    def setUp(self):
        self.command = crud.Command()

    def test_valid_model_name(self):
        """ Test valid model name as argument for command """
        model = settings.TEST_MODEL
        self.command.validate_model_name(model)

    def test_invalid_model_name(self):
        """
        Test model name cannot start with _ or __
        corresponding to error models.E023 and models.E024
        https://docs.djangoproject.com/en/1.11/ref/checks/#models
        """
        model = '_Book'
        self.assertRaises(
            CommandError, self.command.validate_model_name, model)

        model = '__Book'
        self.assertRaises(
            CommandError, self.command.validate_model_name, model)

        model = 'Book_'
        self.assertRaises(
            CommandError, self.command.validate_model_name, model)

    def test_valid_app_name(self):
        """ Check that app name exists """
        app = settings.TEST_APP
        self.command.validate_app_name(app)

    def test_invalid_app_name(self):
        """ Test that error is raised if app does not exist """
        app = settings.TEST_INVALID_APP
        self.assertRaises(
            CommandError, self.command.validate_app_name, app)
