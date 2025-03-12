import re  # Libray for Regular expression
import csv  # Library for reading file data in CSV format


def extract_reg_numbers(car_input_file):
    """Function to extract the vehicle registration numbers from input file"""
    with open(car_input_file, "r") as file:
        file_content = file.read()
        return re.findall(r"\b[A-Z]{2}[0-9]{2}\s?[A-Z]{3}\b", file_content)


def get_vehicle_details(car_details_file):
    """Function to get all vehicle details from the car output file"""
    with open(car_details_file, "r") as file:
        file_content = csv.DictReader(file)
        vehicle_list = []
        for row in file_content:
            vehicle_list.append(row)
        return vehicle_list
