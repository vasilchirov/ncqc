"""
Module with all test fixtures.
When a test fixtures is set as argument for a test function, it automatically runs at the start of the test.

Functions:
- create_nc_boundary_check_success: Test fixture for testing boundary checking
    when all data falls within the boundaries.
- create_nc_boundary_check_fail: Test fixture for testing boundary checking
    when not all data falls within the boundaries.
- create_nc_boundary_check_property_based: Creates netCDF files for property based testing for boundary checks.
- create_nc_existence_check: Test fixture for testing existence checking.
- create_nc_emptiness_check_full: Test fixture for testing boundary checking when everything is fully populated.
- create_nc_emptiness_check_mixed: Test fixture for testing boundary checking when some things are not fully populated.
- create_nc_emptiness_check_empty: Test fixture for testing boundary checking when nothing is populated.
- create_data_points_amount_check: Test fixture for testing data_points_amount_check
"""

import os
from pathlib import Path
from typing import List
from netCDF4 import Dataset
import numpy as np
import pytest

@pytest.fixture()
def create_nc_boundary_check_success():
    """
    Test fixture for testing boundary checking when all data falls within the boundaries.
    """
    nc_path = Path(__file__).parent / 'sample_data' / 'test_boundary_success.nc'

    if os.path.exists(nc_path):
        os.remove(nc_path)

    # Create a new netCDF file
    nc_file = Dataset(nc_path, 'w', format='NETCDF4')

    # Create dimensions
    nc_file.createDimension('time', 100)
    nc_file.createDimension('diameter_classes', 32)
    nc_file.createDimension('velocity_classes', 32)

    # Create variables
    velocity_spread = nc_file.createVariable('velocity_spread', 'f4', ('velocity_classes',), fill_value=-1.0)
    kinetic_energy = nc_file.createVariable('kinetic_energy', 'f4', ('time',), fill_value=-1.0)

    # Set variables
    velocity_spread[:] = np.random.uniform(0, 3.3, size=32)
    kinetic_energy[:] = np.random.uniform(0, 1.91, size=100)

    # Close the netCDF file
    nc_file.close()

@pytest.fixture()
def create_nc_boundary_check_fail():
    """
    Test fixture for testing boundary checking when not all data falls within the boundaries.
    """
    nc_path = Path(__file__).parent / 'sample_data' / 'test_boundary_fail.nc'

    if os.path.exists(nc_path):
        os.remove(nc_path)

    # Create a new netCDF file
    nc_file = Dataset(nc_path, 'w', format='NETCDF4')

    # Create dimensions
    nc_file.createDimension('time', 100)
    nc_file.createDimension('diameter_classes', 32)
    nc_file.createDimension('velocity_classes', 32)

    # Create variables
    velocity_spread = nc_file.createVariable('velocity_spread', 'f4', ('velocity_classes',), fill_value=-1.0)
    kinetic_energy = nc_file.createVariable('kinetic_energy', 'f4', ('time',), fill_value=-1.0)

    # Set variables
    velocity_spread[:] = np.random.uniform(0, 3.3, size=32)
    kinetic_energy[:99] = np.random.uniform(0, 1.8, size=99)
    kinetic_energy[99:] = 1.909999966621399

    # Close the netCDF file
    nc_file.close()

def create_nc_boundary_check_property_based(data: List[int]):
    """
    Function to create netCDF files for property based testing for boundary checks.
    :param data: the list of data points generated by the property based test
    """
    nc_path = Path(__file__).parent / 'sample_data' / 'test_boundary_property.nc'

    if os.path.exists(nc_path):
        os.remove(nc_path)

    # Create a new netCDF file
    nc_file = Dataset(nc_path, 'w', format='NETCDF4')

    # Create dimensions and variables
    nc_file.createDimension('time', len(data))
    temperature = nc_file.createVariable('temperature', 'f4', ('time',), fill_value=-1.0)
    temperature[:] = data

    # Close the netCDF file
    nc_file.close()

@pytest.fixture()
def create_nc_existence_check():
    """
    Test fixture for testing existence checking.
    """
    nc_path = Path(__file__).parent / 'sample_data' / 'test_existence.nc'

    if os.path.exists(nc_path):
        os.remove(nc_path)

    # Create a new netCDF file
    nc_file = Dataset(nc_path, 'w', format='NETCDF4')

    # Create dimensions
    nc_file.createDimension('time', 100)
    nc_file.createDimension('diameter_classes', 32)
    nc_file.createDimension('velocity_classes', 32)

    # Create variables
    nc_file.createVariable('temperature', 'f4', ('time',), fill_value=-999.0)
    nc_file.createVariable('wind_speed', 'f4', ('time',), fill_value=-999.0)
    nc_file.createVariable('wind_direction', 'f4', ('time',), fill_value=-999.0)
    nc_file.createVariable('longitude', 'f4', fill_value=-999.0)
    nc_file.createVariable('latitude', 'f4', fill_value=-999.0)
    nc_file.createVariable('altitude', 'f4', fill_value=-999.0)

    # Create global attributes
    nc_file.title = "Test NetCDF File"
    nc_file.source = "confest.py"
    nc_file.contributors = "people"

    # Close the netCDF file
    nc_file.close()

@pytest.fixture()
def create_nc_emptiness_check_full():
    """
    Test fixture for testing boundary checking when everything is fully populated.
    """
    nc_path = Path(__file__).parent / 'sample_data' / 'test_emptiness_full.nc'

    if os.path.exists(nc_path):
        os.remove(nc_path)

    # Create a new netCDF file
    nc_file = Dataset(nc_path, 'w', format='NETCDF4')

    # Create dimensions
    nc_file.createDimension('time', 100)
    nc_file.createDimension('diameter_classes', 32)
    nc_file.createDimension('velocity_classes', 32)

    # Create variables
    temperature = nc_file.createVariable('temperature', 'f4', ('time',), fill_value=-999.0)
    wind_speed = nc_file.createVariable('wind_speed', 'f4', ('time',), fill_value=-999.0)
    wind_direction = nc_file.createVariable('wind_direction', 'f4', ('time',), fill_value=-999.0)

    # Set variables
    temperature[:] = np.random.uniform(-10, 30, size=100)
    wind_speed[:] = np.random.uniform(0, 30, size=100)
    wind_direction[:] = np.random.uniform(0, 360, size=100)

    # Create global attributes
    nc_file.title = "Test NetCDF File"
    nc_file.source = "confest.py"
    nc_file.contributors = "people"

    # Close the netCDF file
    nc_file.close()

@pytest.fixture()
def create_nc_emptiness_check_mixed():
    """
    Test fixture for testing boundary checking when some things are not fully populated.
    """
    nc_path = Path(__file__).parent / 'sample_data' / 'test_emptiness_mixed.nc'

    if os.path.exists(nc_path):
        os.remove(nc_path)

    # Create a new netCDF file
    nc_file = Dataset(nc_path, 'w', format='NETCDF4')

    # Create dimensions
    nc_file.createDimension('time', 100)
    nc_file.createDimension('diameter_classes', 32)
    nc_file.createDimension('velocity_classes', 32)

    # Create variables
    temperature = nc_file.createVariable('temperature', 'f4', ('time',), fill_value=-999.0)
    wind_speed = nc_file.createVariable('wind_speed', 'f4', ('time',), fill_value=-999.0)
    wind_direction = nc_file.createVariable('wind_direction', 'f4', ('time',), fill_value=-999.0)
    longitude = nc_file.createVariable('longitude', 'f4', fill_value=-999.0)
    latitude = nc_file.createVariable('latitude', 'f4', fill_value=-999.0)
    altitude = nc_file.createVariable('altitude', 'f4', fill_value=-999.0)

    # Set variables
    temperature[:] = np.random.uniform(-10, 30, size=100)

    wind_speed[:50] = np.random.uniform(0, 30, size=50)
    wind_speed[50:] = wind_speed.getncattr('_FillValue')

    wind_direction[:50] = np.random.uniform(0, 360, size=50)
    wind_direction[50:] = np.nan

    longitude.assignValue(longitude.getncattr('_FillValue'))
    latitude.assignValue(np.nan)
    altitude.assignValue(1.0)

    # Create global attributes
    nc_file.title = "Test NetCDF File"
    nc_file.source = "confest.py"
    nc_file.contributors = ""

    # Close the netCDF file
    nc_file.close()

@pytest.fixture()
def create_nc_emptiness_check_empty():
    """
    Test fixture for testing boundary checking when nothing is populated.
    """
    nc_path = Path(__file__).parent / 'sample_data' / 'test_emptiness_empty.nc'

    if os.path.exists(nc_path):
        os.remove(nc_path)

    # Create a new netCDF file
    nc_file = Dataset(nc_path, 'w', format='NETCDF4')

    # Create dimensions
    nc_file.createDimension('time', 100)
    nc_file.createDimension('diameter_classes', 32)
    nc_file.createDimension('velocity_classes', 32)

    # Create variables
    nc_file.createVariable('temperature', 'f4', ('time',), fill_value=-999.0)
    wind_speed = nc_file.createVariable('wind_speed', 'f4', ('time',), fill_value=-999.0)
    wind_direction = nc_file.createVariable('wind_direction', 'f4', ('time',), fill_value=-999.0)

    # Set variables
    wind_speed[:] = wind_speed.getncattr('_FillValue')
    wind_direction[:] = np.nan

    # Create global attributes
    nc_file.title = ""
    nc_file.source = ""
    nc_file.contributors = ""

    # Close the netCDF file
    nc_file.close()


@pytest.fixture()
def create_nc_data_points_amount_check():
    """
    Test fixture for testing data_points_amount_check
    """
    nc_path = Path(__file__).parent / 'sample_data' / 'test_data_points_amount.nc'

    if os.path.exists(nc_path):
        os.remove(nc_path)

    nc_file = Dataset(nc_path, 'w', format='NETCDF4')

    nc_file.createDimension('dimension_1', 10)
    nc_file.createDimension('dimension_2', 20)

    var_1d = nc_file.createVariable('var_1d', 'f4', ('dimension_1',), fill_value=-999.0)
    var_2d = nc_file.createVariable('var_2d', 'f4', ('dimension_1', 'dimension_2'), fill_value=-999.0)

    var_1d[:] = np.random.uniform(low=0, high=100, size=10)
    var_2d[:, :] = np.random.uniform(low=0, high=100, size=(10, 20))

    nc_file.close()
