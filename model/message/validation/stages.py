# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
"""
Combination of validation checks to be performed on the Message at each stage of the pipeline
"""
import model.message.validation.validators as validators
from model.message.validation.process import check_validity_dict


def validate_data_ready(message):
    """
    Assert a message is ready to be passed to the /DataReady queue
    :param message: A message object to be validated
    :return: True if valid
    """
    validity_dict = {
        'run_number': validators.validate_run_number(message.run_number),
        'instrument': validators.validate_instrument(message.instrument),
        'rb_number': validators.validate_rb_number(message.rb_number),
        'started_by': isinstance(message.started_by, int),
        'file_path': isinstance(message.data, str),
        'facility': isinstance(message.facility, str)
    }
    return check_validity_dict(validity_dict)
