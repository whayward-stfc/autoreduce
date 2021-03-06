# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
"""
get_icat_instrument_prefix() can be used to map Autoreduction to ICAT instrument prefixes
"""
from utils.clients.icat_client import ICATClient
from utils.settings import VALID_INSTRUMENTS as AUTOREDUCTION_INSTRUMENT_NAMES
from utils.clients.tools.isisicat_prefix_mapping_logging_setup import logger


def get_icat_instrument_prefix(autoreduction_instruments=None):
    """
    Queries ICAT for shorter names for all Autoreduction instruments or only selection if passed in
    :param autoreduction_instruments: Optionally input custom list of autoreduction instrument names
    :return: A map of Autoreduction to ICAT instrument prefixes
    """
    if not autoreduction_instruments:
        autoreduction_instruments = AUTOREDUCTION_INSTRUMENT_NAMES

    client = ICATClient()

    try:
        icat_instruments = client.execute_query("SELECT i FROM Instrument i")
    except Exception:  # pylint:disable=broad-except
        warning_message = "ICAT instrument query failed"
        print(warning_message)
        logger.warning(warning_message)
        return None

    instrument_fullname_to_short_name_map = {}

    for instrument_fullname in autoreduction_instruments:
        icat_instrument = next((x for x in icat_instruments if x.fullName == instrument_fullname),
                               None)

        if not icat_instrument:
            warning_message = f"No instrument in ICAT with fullName {instrument_fullname}"
            print(warning_message)
            logger.warning(warning_message)
            # Missing an instrument should also be picked up in the tests
            continue

        instrument_fullname_to_short_name_map[instrument_fullname] = icat_instrument.name

    return instrument_fullname_to_short_name_map
