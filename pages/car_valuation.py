class CarValuation:
    """POM class to interact with the Car Valuation page"""

    def __init__(self, page, vehicle_reg_number):
        """Initialize the Car Valuation page elements.
        Params :
            page -> Page Object send fromthe test case while creating the object for this class
        """
        self.page = page
        self.reg_number_input_box = "#vrm-input"
        self.value_your_car_button = "[data-cy='valueButton']"
        self.car_make_model = ".HeroVehicle__title-FAmG"
        self.car_year = "ul.HeroVehicle__details-XpAI li"
        self.car_not_found_container = ".Toast-shared-module__toastContainer-e8ni"
        self.vehicle_reg_number = vehicle_reg_number

    def navigate_to_url(self, url):
        """Uses the page object and navigate to the given URL
        Params :
        url -> Valuation portal URL send from the test case
        """
        self.page.goto(url)

    def enter_and_search_vehicle_reg(self):
        """Uses page object, enters the registration number and click on the value your car button
        Params :
        vehicle_reg_number -> Vehicle registration number send from the test case
        """

        self.page.locator(self.reg_number_input_box).fill(self.vehicle_reg_number)
        self.page.locator(self.value_your_car_button).click()

    def get_vehicle_details(self):
        """uses page object and locate the car details in the motorway.co.uk page.
        Params :
        vehicle_reg_number -> Vehicle registration number send from the test case
        Returns :
            Make-Model-Year in the form of [List] if found
            None if car details not found
        """

        # Wait for the car details or the car not found container to be visible in the page
        self.page.wait_for_selector(
            f"{self.car_make_model}, {self.car_not_found_container}", timeout=10000
        ).is_visible()

        # Check if the car details elements are visible in the page
        if self.page.locator(self.car_make_model).is_visible():
            self.page.screenshot(
                path=f"screenshots/{self.vehicle_reg_number}_car_details_found.png"
            )  # Take screenshot if car details found
            return [
                self.page.locator(self.car_make_model).inner_text(),
                (self.page.locator(self.car_year).all_text_contents())[0],
            ]
        elif self.page.locator(
            self.car_not_found_container
        ).is_visible():  # Check if the car not found container is visible in the page
            self.page.screenshot(
                path=f"screenshots/{self.vehicle_reg_number}_car_not_found.png"
            )  # Take screenshot if car not found
            return None  # return None upon car not found container
        else:
            self.page.screenshot(
                path=f"screenshots/{self.vehicle_reg_number}_car_not_found.png"
            )  # Take screenshot if car details not found
            return None  # return None if car details not found
