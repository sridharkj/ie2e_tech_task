import pytest  # pytest framework for test execution
import logging  # logging module for logging
from utils.helpers import (
    extract_reg_numbers,
    get_vehicle_details,
)  # helper functions for extracting reg numbers and vehicle details
from pages.car_valuation import CarValuation  # page object for car valuation

logger = logging.getLogger(__name__)

# File location of input and output files
car_input_file = "data/car_input - V5.txt"
car_output_file = "data/car_output - V5.txt"

# URL for car valuation portal
valuation_portal = "https://motorway.co.uk/"

# Extracting vehicle registration numbers from input file
vehicle_reg_list = extract_reg_numbers(car_input_file)


# Test parameters with each vehicle registration number and set test id based on on the car reg number
@pytest.mark.parametrize(
    "vehicle_reg_number",
    vehicle_reg_list,
    ids=[f"Test for Vehicle Reg: {each_veh_reg}" for each_veh_reg in vehicle_reg_list],
)
def test_for_car_valuation(browser, vehicle_reg_number, caplog):
    """Test case to verify the vehicle details in Motorway.co.uk with the car output file"""

    # Set log level to INFO for capturing logs in the HTML report
    caplog.set_level(logging.INFO)

    # Get all vehicle details from car output file
    vehicle_details = get_vehicle_details(car_output_file)

    # Create a object for new page & CarValuation page
    page = browser.new_page()
    car_valuation_page = CarValuation(page, vehicle_reg_number)

    try:
        logging.info(
            f"Capturing Vehicle REG {vehicle_reg_number} details in Motorway.co.uk"
        )

        # Navigate to car valuation portal and search for the parameterized car registration number
        car_valuation_page.navigate_to_url(valuation_portal)
        car_valuation_page.enter_and_search_vehicle_reg()

        # Get vechicle details from the valuation portal
        get_car_details = (
            car_valuation_page.get_vehicle_details()
        )  # it returns Make-Model-Year if found and None if not found

        if get_car_details != None:  # if car details found

            # Get Make, Model and Year from the car details
            mw_veh_make_model = get_car_details[0]
            mw_veh_year = get_car_details[1]

            vehicle_details_matched = (
                False  # flag to check if vehicle details found in car output file
            )

            # Loop for each vehicle details captured from the car output file
            for each_vehicle in vehicle_details:
                if each_vehicle["VARIANT_REG"].replace(
                    " ", ""
                ) == vehicle_reg_number.replace(
                    " ", ""
                ):  # removing the spaces in the reg number and comparing

                    # Check if the Car Make/Model in the car output file matches with the value captured from the Motorway.co.uk
                    assert (
                        each_vehicle["MAKE_MODEL"] == mw_veh_make_model
                    ), f"Vehicle Make/Model mismatch:\n Expected (in file):  {mw_veh_make_model}, Actual (in MW): {each_vehicle['MAKE_MODEL']}"

                    # Check if the Car Year in the car output file matches with the Year captured from the Motorway.co.uk
                    assert (
                        each_vehicle["YEAR"] == mw_veh_year
                    ), f"Vehicle Year mismatch:\n Expected (in file): {mw_veh_year}, Got (in MW): {each_vehicle['YEAR']}"

                    # Logging the vehcle details for the HTML report
                    logging.info(
                        "VEHICLE DETAILS IN MOTORWAY MATCHED WITH CAR OUTPUT FILE"
                    )
                    logging.info(f"VARIANT_REG: {each_vehicle['VARIANT_REG']}")
                    logging.info(f"MAKE_MODEL: {each_vehicle['MAKE_MODEL']}")
                    logging.info(f"YEAR: {each_vehicle['YEAR']}")

                    vehicle_details_matched = (
                        True  # set the flag to True if vehcile details are matched
                    )
                    break
        else:
            # Fails the test as vehcile details not found in the motorway.co.uk portal
            logging.error(
                f"Vehicle details not found for {vehicle_reg_number} in Motorway.co.uk"
            )
            pytest.fail(
                f"Test failed: Vehicle details not found for {vehicle_reg_number} in Motorway.co.uk"
            )

        # Fails the test as vehcile details are not matched
        if not vehicle_details_matched:
            logging.error(
                f"Vehicle details not found for {vehicle_reg_number} in Car output file"
            )
            pytest.fail(
                f"Test failed: Vehicle details not found for {vehicle_reg_number} in Car output file"
            )

    finally:
        page.close()  # close the page after completing the test execution
