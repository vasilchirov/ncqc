"""
Module for testing the functionality of the value_change_rate_check method

Functions:
- test_value_change_rate_check_no_nc: Test for value change rate check when no netCDF file is loaded
- test_change_rate: Test checking for the change rate of variables
- test_change_rate_var_not_in_file: Test checking for the change rate of variables when
  variable is not in file.
- test_change_rate_omitted_var: Tests checking for the change rate of variables when variable
  should be omitted from check
"""

import os
from pathlib import Path
import pytest

from netcdfqc.QCnetCDF import QualityControl

data_dir = Path(__file__).parent.parent / 'sample_data'

change_rate_check_test_dict = {
    'dimensions': {
    },
    'variables': {
        'test_pass': {
            'do_values_change_at_acceptable_rate_check': {'perform_check': True, 'acceptable_difference': 1}
        },
        'test_fail': {
            'do_values_change_at_acceptable_rate_check': {'perform_check': True, 'acceptable_difference': 1}
        },
    },
    'global attributes': {
    },
    'file size': {
    }
}

change_rate_check_var_not_in_nc_dict = {
    'dimensions': {
    },
    'variables': {
        'test_not_in_nc': {
            'do_values_change_at_acceptable_rate_check': {'perform_check': True, 'acceptable_difference': 1}
        },
    },
    'global attributes': {
    },
    'file size': {
    }
}

change_rate_check_omit_var_test_dict = {
    'dimensions': {
    },
    'variables': {
        'test_pass': {
            'do_values_change_at_acceptable_rate_check': {'perform_check': True, 'acceptable_difference': 1}
        },
        'test_fail': {
            'do_values_change_at_acceptable_rate_check': {'perform_check': False, 'acceptable_difference': 1}
        },
    },
    'global attributes': {
    },
    'file size': {
    }
}

def test_value_change_rate_check_no_nc():
    """
    Test for value change rate check when no netCDF file is loaded.
    """
    qc_obj = QualityControl()
    qc_obj.add_qc_checks_dict(change_rate_check_test_dict)
    qc_obj.values_change_rate_check()
    assert not qc_obj.logger.info
    assert qc_obj.logger.errors == ['values change rate check error: no nc file loaded']
    assert not qc_obj.logger.warnings


@pytest.mark.usefixtures("create_nc_change_rate_check")
def test_change_rate():
    """
    Test checking for the change rate of variables.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_change_rate.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(change_rate_check_test_dict)

    qc_obj.values_change_rate_check()

    assert qc_obj.logger.info == ["value change rate check for variable 'test_pass': success",
                                  "value change rate check for variable 'test_fail': fail"]
    assert not qc_obj.logger.errors
    assert not qc_obj.logger.warnings

    if os.path.exists(nc_path):
        os.remove(nc_path)


@pytest.mark.usefixtures("create_nc_change_rate_check")
def test_change_rate_var_not_in_file():
    """
    Test checking for the change rate of variables when variable is not in file.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_change_rate.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(change_rate_check_var_not_in_nc_dict)

    qc_obj.values_change_rate_check()

    assert not qc_obj.logger.errors
    assert qc_obj.logger.warnings == ['variable \'test_not_in_nc\' not in nc file']

    if os.path.exists(nc_path):
        os.remove(nc_path)

@pytest.mark.usefixtures("create_nc_change_rate_check")
def test_change_rate_omitted_var():
    """
    Test checking for the change rate of variables when variable should be omitted from check.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_change_rate.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(change_rate_check_omit_var_test_dict)

    qc_obj.values_change_rate_check()

    #only variable test_pass is checked,variable test_fail isn't checked
    assert qc_obj.logger.info == ["value change rate check for variable 'test_pass': success"]

    assert not qc_obj.logger.errors
    assert not qc_obj.logger.warnings

    if os.path.exists(nc_path):
        os.remove(nc_path)



