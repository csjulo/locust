from locust import HttpUser, task, constant, SequentialTaskSet, events, LoadTestShape
from utils.readtestdata import CsvRead
from locust.exception import StopUser
from json import JSONDecodeError
from fakes.constant import app_version, registration
import random
from locustfiles.example_spike_test import Example
import logging
from locust_plugins.csvreader import CSVReader

test_data = CSVReader("CSV_Data//registration.csv")

class UnderWritingFlow(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.token = ""
        self.application_id = ""
        self.phone_number = ""

    # def on_start(self):
    #     self.phone="Phone Not Exist"

    #     if len(test_data) > 0:
    #         self.phone = test_data.pop()

    @task
    def set_initial_data(self):
        data_csv = next(test_data)
        self.phone_number = data_csv[0]

    @task
    def generate_customer(self):
        endpoint = "/api/registration-flow/v1/generate-customer/"

        name_thread = "Registration - Generate Customer - " + endpoint

        data = {
            "phone": self.phone_number
        }

        with self.client.post(endpoint, catch_response=True, name=name_thread, data=data) as response:
            logging.info("Response 1 : " + response.text)
            if response.status_code == 201 and response.elapsed.total_seconds() < 1.5:
                response.success()
            else:
                response.failure("Failure in process generate customer")

    @task
    def register(self):
        endpoint = "/api/registration-flow/v1/register/"

        name_thread = "Registration - Registration Flow - " + endpoint

        data = {
            "phone": self.phone_number,
            "android_id": registration["android_id"],
            "app_version": app_version["short_form"],
            "pin": "159357",
            "longitude": "106.841866",
            "latitude": "-6.224373",
            "gcm_reg_id": "test"
        }

        with self.client.post(endpoint, catch_response=True, name=name_thread, data=data) as response:
            logging.info("Response 2 : " + response.text)
            if response.status_code == 201:
                response.success()
            else:
                response.failure("Failure in process registration")

    @task
    def login(self):
        endpoint = "/api/pin/v4/login/"

        name_thread = "Login - Login Flow - " + endpoint

        data = {
            "username": self.phone_number,
            "android_id": registration["android_id"],
            "app_version": app_version["short_form"],
            "pin": "159357",
            "longitude": "106.841866",
            "latitude": "-6.224373",
            "gcm_reg_id": "test"
        }

        with self.client.post(endpoint, catch_response=True, name=name_thread, data=data) as response:
            print(response.text)
            if response.status_code == 200:
                response.success()

                try:
                    token = response.json()["data"]["token"]
                    self.token = token

                    application_id = response.json()["data"]["applications"][0]["id"]
                    self.application_id = application_id

                except JSONDecodeError:
                    self.token = ""
                    self.application_id = ""
                    response.failure("Response could not be decoded as JSON")
                    
                except KeyError:
                    response.failure("Response did not contain expected key")

            else:
                response.failure("Failure in process login")

    @task
    def check_existence(self):
        endpoint = "/api/registration-flow/v2/check/"

        name_thread = "Login - Check Existence - " + endpoint

        data = {
            "phone": self.phone_number
        }

        with self.client.post(
            endpoint,
            catch_response=True, 
            name=name_thread, 
            data=data,
            headers={"authorization": "Token " + self.token},
        ) as response:

            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failure in process check existence")

    @task
    def scrape_data(self):
        endpoint = "/api/v2/etl/dsd/"

        name_thread = "SubmitForm - Scrape Data - " + endpoint

        data = {
            "application_id": self.application_id
        }

        files = {"upload": open("upload_file//DataScrape.zip", "rb")}

        with self.client.post(endpoint,
                catch_response=True, 
                name=name_thread, 
                data=data,
                files=files,
                headers={"authorization": "Token " + self.token},
            ) as response:

            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failure in process upload scrape data")

    @task
    def get_province(self):
        endpoint = "/api/v3/address/provinces"

        name_thread = "SubmitForm - Get Province - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token}
        ) as response:
            try:
                success_response = response.json()["success"]
                if response.status_code == 200 and success_response == True:
                    response.success()
                else:
                    response.failure("Failure in get province")

            except JSONDecodeError:
                success_response = ""
                response.failure("Response could not be decoded as JSON")
                
            except KeyError:
                response.failure("Response did not contain expected key")

    @task
    def get_detail_locations(self):
        endpoint = "/api/application-form/v1/regions/"

        name_thread = "SubmitForm - Get Detail Location - " + endpoint

        province = registration["province"]
        city = registration["city"]
        district = registration["district"]
        sub_district = registration["sub_district"]

        with self.client.get(
            endpoint + "check?province={}&city={}&district={}&sub-district={}".format(province,city,district,sub_district),
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token}
        ) as response:
            try:
                success_response = response.json()["success"]
                if response.status_code == 200 and success_response == True:
                    response.success()
                else:
                    response.failure("Failure in get detail locations")

            except JSONDecodeError:
                success_response = ""
                response.failure("Response could not be decoded as JSON")
                
            except KeyError:
                response.failure("Response did not contain expected key")
                
    @task
    def check_payslip_mandatory(self):
        endpoint = "/api/v2/mobile/check-payslip-mandatory/"

        name_thread = "SubmitForm - Check payslip mandatory - " + endpoint

        with self.client.get(
            endpoint + str(self.application_id),
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token}
        ) as response:
            logging.info("Response check : " + response.text)

            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failure in get detail locations")

    @task
    def upload_ktp(self):
        endpoint = "/api/v1/images/"

        name_thread = "SubmitForm - Upload KTP - " + endpoint

        data = {
            "image_type": "ktp_self",
            "image_source": self.application_id
        }

        files = {"upload": open("upload_file//image.png", "rb")}

        with self.client.post(endpoint,
                catch_response=True, 
                name=name_thread, 
                data=data,
                files=files,
                headers={"authorization": "Token " + self.token},
            ) as response:

            if response.status_code == 201:
                response.success()
            else:
                response.failure("Failure in process upload ktp")

    @task
    def upload_selfie(self):
        endpoint = "/api/face_recognition/v1/selfie/check-upload"

        name_thread = "SubmitForm - Upload Selfie - " + endpoint

        data = {
            "file_name": "image"
        }

        files = {"image": open("upload_file//image.png", "rb")}

        with self.client.post(endpoint,
                catch_response=True, 
                name=name_thread, 
                data=data,
                files=files,
                headers={"authorization": "Token " + self.token},
            ) as response:

            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failure in process upload selfie")

    # @task
    # def short_form_submission(self):
    #     endpoint = "/api/application-form/v1/application/"

    #     name_thread = "Submit Form - Submission - " + endpoint

    #     data = {
    #         "phone": self.phone_number
    #     }

    #     with self.client.patch(
    #         endpoint + str(self.application_id),
    #         catch_response=True, 
    #         name=name_thread, 
    #         data=data,
    #         headers={"authorization": "Token " + self.token},
    #     ) as response:
    #         print("response form submission : {}".format(response.text))
    #         if response.status_code == 200:
    #             response.success()
    #         else:
    #             response.failure("Failure in process short form submission")

    # @task
    # def stop(self):
    #     # raise exit()
    #     raise StopUser()

class MySeqTest(HttpUser):
    wait_time = constant(1)
    host = "https://api-staging.julofinance.com"
    tasks = [UnderWritingFlow]

class StagesShape(LoadTestShape):
    """
    A simply load test shape class that has different user and spawn_rate at
    different stages.
    Keyword arguments:
        stages -- A list of dicts, each representing a stage with the following keys:
            duration -- When this many seconds pass the test is advanced to the next stage
            users -- Total user count
            spawn_rate -- Number of users to start/stop per second
            stop -- A boolean that can stop that test at a specific stage
        stop_at_end -- Can be set to stop once all stages have run.
    """

    stages = [
        # {"duration": 5, "users": 10, "spawn_rate": 10},
        # {"duration": 15, "users": 50, "spawn_rate": 10},
        # {"duration": 25, "users": 100, "spawn_rate": 10},
        # {"duration": 45, "users": 10, "spawn_rate": 10},
        # {"duration": 75, "users": 1, "spawn_rate": 1}

        #### Load Test ####
        {"duration": 30, "users": 20, "spawn_rate": 2}, # simulate ramp-up of traffic to 50 users over 25 seconds.
        {"duration": 50, "users": 20, "spawn_rate": 20}, # stay at 50 users for around 25 seconds
        {"duration": 65, "users": 10, "spawn_rate": 10}, # ramp-down to 10 users around 15 seconds
        {"duration": 75, "users": 1, "spawn_rate": 1} # ramp-down to 1 users

        #### Stress Test ####
        # {"duration": 25, "users": 50, "spawn_rate": 2}, # simulate ramp-up of traffic to 50 users over 25 seconds. (normal load)
        # {"duration": 50, "users": 50, "spawn_rate": 50}, # stay at 50 users for around 25 seconds
        # {"duration": 65, "users": 60, "spawn_rate": 10}, # ramp-up to 60 users around 15 seconds (beyond the breaking point)
        # {"duration": 80, "users": 30, "spawn_rate": 10}, # ramp-down
        # {"duration": 95, "users": 10, "spawn_rate": 10}, # ramp-down
        # {"duration": 110, "users": 1, "spawn_rate": 1} # ramp-down to 1 users
        
        #### Spike Test ####
        # {"duration": 10, "users": 50, "spawn_rate": 10}, # simulate ramp-up of traffic to 50 users over 10 seconds. (normal load)
        # {"duration": 20, "users": 100, "spawn_rate": 100}, # stay at 50 users for around 25 seconds
        # {"duration": 40, "users": 50, "spawn_rate": 50}, # ramp-down to 50 users around 20 seconds (recovery)
        # {"duration": 50, "users": 30, "spawn_rate": 10}, # ramp-down
        # {"duration": 70, "users": 10, "spawn_rate": 10}, # ramp-down
        # {"duration": 85, "users": 1, "spawn_rate": 1} # ramp-down to 1 users
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None