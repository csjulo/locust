from locust import HttpUser, task, constant, SequentialTaskSet, events, LoadTestShape
from json import JSONDecodeError
from fakes.constant import app_version, registration
from locustfiles.example_spike_test import Example
import logging
from locust_plugins.csvreader import CSVReader
from influxdb import InfluxDBClient
import json
import socket
import datetime
import pytz

# Define setup to store data to influxDB
host=socket.gethostname()
client=InfluxDBClient(host="localhost",port="8086")
client.switch_database("locust")

# Define events for request success
@events.request_success.add_listener
def individual_success_handle(request_type, name, response_time, response_length, **kwargs):
    SUCCESS_TEMPLATE = '[{"measurement": "%s","tags": {"hostname":"%s","requestName": "%s","requestType": "%s","status":"%s"' \
                    '},"time":"%s","fields": {"responseTime": %s,"responseLength":%s}' \
                    '}]'
    json_string = SUCCESS_TEMPLATE % ("ResponseTable", host, name, request_type, "SUCCESS", datetime.datetime.now(tz=pytz.UTC), response_time, response_length)
    client.write_points(json.loads(json_string))

# Define events for request failed
@events.request_failure.add_listener
def individual_fail_handle(request_type, name, response_time, response_length, exception, **kwargs):
    FAIL_TEMPLATE = '[{"measurement": "%s","tags": {"hostname":"%s","requestName": "%s","requestType": "%s","exception":"%s","status":"%s"' \
                    '},"time":"%s","fields": {"responseTime": %s,"responseLength":%s}' \
                    '}]'
    json_string = FAIL_TEMPLATE % ("ResponseTable", host, name, request_type, exception, "FAIL", datetime.datetime.now(tz=pytz.UTC),response_time, response_length)
    client.write_points(json.loads(json_string))

# Get data parameterization from CSV
test_data = CSVReader("CSV_Data//registration_long_form.csv")

class UnderWritingFlow(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.token = ""
        self.phone_number = ""
        self.email = ""

    @task
    def set_initial_data(self):
        data_csv = next(test_data)
        self.phone_number = data_csv[0]
        self.email = data_csv[1]

    @task
    def register(self):
        endpoint = "/api/pin/v1/register/"

        name_thread = "Registration - Registration Flow - " + endpoint

        data = {
            "username": self.phone_number,
            "email": self.email + "@julo.co.id",
            "android_id": "apitest3423",
            "app_version": "6.7.0",
            "pin": "159357",
            "longitude": "106.841866",
            "latitude": "-6.224373",
            "gcm_reg_id": "test"
        }

        with self.client.post(endpoint, catch_response=True, name=name_thread, data=data) as response:
            print(response.text)
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
            "email": self.email + "@julo.co.id",
            "android_id": "apitest3423",
            "pin": "159357",
            "longitude": "106.841866",
            "latitude": "-6.224373",
            "gcm_reg_id": "test"
        }

        with self.client.post(endpoint, catch_response=True, name=name_thread, data=data) as response:
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

class MySeqTest(HttpUser):
    wait_time = constant(1)
    host = "https://api-staging.julofinance.com"
    tasks = [UnderWritingFlow]

    # Add listener for request success and failed events
    events.request_success.add_listener(individual_success_handle)
    events.request_failure.add_listener(individual_fail_handle)


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
        {"duration": 15, "users": 50, "spawn_rate": 1}, # simulate ramp-up of traffic to 50 users over 25 seconds.
        {"duration": 30, "users": 50, "spawn_rate": 50}, # stay at 50 users for around 15 seconds
        {"duration": 45, "users": 10, "spawn_rate": 10}, # ramp-down to 10 users around 15 seconds
        {"duration": 55, "users": 1, "spawn_rate": 1} # ramp-down to 1 users

        #### Stress Test ####
        # {"duration": 15, "users": 50, "spawn_rate": 5}, # simulate ramp-up of traffic to 50 users over 15 seconds. (normal load)
        # {"duration": 30, "users": 50, "spawn_rate": 50}, # stay at 50 users for around 20 seconds
        # {"duration": 45, "users": 75, "spawn_rate": 20}, # ramp-up to 60 users around 15 seconds (beyond the breaking point)
        # {"duration": 60, "users": 30, "spawn_rate": 10}, # ramp-down
        # {"duration": 75, "users": 10, "spawn_rate": 10}, # ramp-down
        # {"duration": 90, "users": 1, "spawn_rate": 1} # ramp-down to 1 users
        
        #### Spike Test ####
        # {"duration": 10, "users": 20, "spawn_rate": 5}, # simulate ramp-up of traffic to 20 users over 10 seconds. (normal load)
        # {"duration": 35, "users": 100, "spawn_rate": 100}, # stay at 100 users for around 10 seconds
        # {"duration": 45, "users": 20, "spawn_rate": 20}, # ramp-down to 50 users around 20 seconds (recovery)
        # {"duration": 55, "users": 10, "spawn_rate": 10}, # ramp-down
        # {"duration": 65, "users": 1, "spawn_rate": 1} # ramp-down to 1 users
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
