# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
"""
Test utility functions for constructing run variables
"""
import unittest
import datetime

from mock import patch

from queue_processors.queue_processor.queueproc_utils.variable_utils import VariableUtils as vu

from model.database import access


# pylint:disable=missing-class-docstring
class TestVariableUtils(unittest.TestCase):

    def setUp(self):
        self.var_model = access.start_database().variable_model
        self.data_model = access.start_database().data_model
        self.valid_variable = self.var_model.Variable(name='test',
                                                      value='value',
                                                      type='text',
                                                      is_advanced=False,
                                                      help_text='help text')
        self.valid_inst_var = self.var_model.InstrumentVariable(name='test',
                                                                value='value',
                                                                is_advanced=False,
                                                                type='text',
                                                                help_text='help test',
                                                                instrument_id=4,
                                                                experiment_reference=54321,
                                                                start_run=12345,
                                                                tracks_script=1)
        self.reduction_run = self.data_model.ReductionRun(run_number=1111,
                                                          run_version=0,
                                                          run_name='run name',
                                                          cancel=0,
                                                          hidden_in_failviewer=0,
                                                          admin_log='admin log',
                                                          reduction_log='reduction log',
                                                          created=datetime.datetime.utcnow(),
                                                          last_updated=datetime.datetime.utcnow(),
                                                          experiment_id=222,
                                                          instrument_id=3,
                                                          status_id=4,
                                                          script='script',
                                                          started_by=1)

    def test_derive_run_variable(self):
        """
        Test: A RunVariable record is created
        When: calling the derive_run_variable function with valid input
        """
        expected = self.var_model.RunVariable(name=self.valid_variable.name,
                                              value=self.valid_variable.value,
                                              is_advanced=self.valid_variable.is_advanced,
                                              type=self.valid_variable.type,
                                              help_text=self.valid_variable.help_text,
                                              reduction_run=self.reduction_run)
        actual = vu.derive_run_variable(self.valid_variable, self.reduction_run)
        self.assertIsInstance(actual, self.var_model.RunVariable)
        self.assertEqual(actual.name, expected.name)

    @patch('queue_processors.queue_processor.queueproc_utils.variable_utils.'
           'VariableUtils.derive_run_variable')
    @patch('model.database.access.save_record')
    def test_save_run_variable(self, mock_derive_run_var, mock_save):
        """
        Test: A record is correctly generated and saved in the database
        When: Calling the save_run_variable function
        """
        var_utils = vu()
        var_utils.save_run_variables([self.valid_variable], self.reduction_run)
        mock_derive_run_var.assert_called_once()
        mock_save.assert_called_once()

    def test_copy_variable(self):
        """
        Test: A Variable object can is copied
        When: copy_variable function is called
        """
        expected = self.valid_variable
        expected.pk = None

        actual = vu.copy_variable(vu.copy_variable(self.valid_inst_var))
        self.assertIsInstance(actual, self.var_model.InstrumentVariable)
        self.assertEqual(actual.name, expected.name)

    def test_get_type_string(self):
        """
        Test: Python types are successfully recognised and converted to database input
        When: Calling get_type_string
        """
        self.assertEqual(vu.get_type_string('a string'), 'text')
        self.assertEqual(vu.get_type_string(1), 'number')
        self.assertEqual(vu.get_type_string(1.0), 'number')
        self.assertEqual(vu.get_type_string(True), 'boolean')
        self.assertEqual(vu.get_type_string([1, 2, 3]), 'list_number')
        self.assertEqual(vu.get_type_string(['s', 't', 'r']), 'list_text')

    def test_get_type_string_unknown_type(self):
        """
        Test: A value of unknown type is output as database type text
        When: Calling get_type_string
        """
        self.assertEqual(vu.get_type_string({'key': 'value'}), 'text')

    def test_convert_variable_to_type(self):
        """
        Test: database variables types are successfully recognised and converted into python
        single variable types
        When: calling convert_variable_to_type with valid arguments
        """
        self.assertIsInstance(vu.convert_variable_to_type('text', 'text'), str)
        self.assertIsInstance(vu.convert_variable_to_type('1', 'number'), int)
        self.assertIsInstance(vu.convert_variable_to_type('1.0', 'number'), float)
        self.assertIsInstance(vu.convert_variable_to_type('True', 'boolean'), bool)
        self.assertIsInstance(vu.convert_variable_to_type('False', 'boolean'), bool)

    def test_convert_variable_to_type_list_types(self):
        """
        Test database variables types are successfully recognised and converted into python
        for list types
        """
        str_list = vu.convert_variable_to_type('[\'s\',\'t\'', 'list_text')
        self.assertIsInstance(str_list, list)
        self.assertIsInstance(str_list[0], str)
        int_list = vu.convert_variable_to_type('1,2', 'list_number')
        self.assertIsInstance(int_list, list)
        self.assertIsInstance(int_list[0], int)
        float_list = vu.convert_variable_to_type('1.0,2.0', 'list_number')
        self.assertIsInstance(float_list, list)
        self.assertIsInstance(float_list[0], float)

    def test_convert_variable_unknown_type(self):
        """
        Test output variable type are unchanged if the target type is unrecognised
        """
        self.assertIsInstance(vu.convert_variable_to_type('value', 'unknown'), str)
        self.assertIsInstance(vu.convert_variable_to_type(1, 'unknown'), int)

    def test_convert_variable_mismatch_type(self):
        """
        Test: number type conversion with non number
        """
        self.assertIsNone(vu.convert_variable_to_type('string', 'number'))
