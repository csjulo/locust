import re
from locust import HttpUser, task, constant, SequentialTaskSet
from utils.readtestdata import CsvRead
from locust.exception import StopUser
from fakes.customer import Customer
from fakes.device import Device
from fakes.device import AppVersion
from fakes.constant import app_version, registration
import random

test_data = CsvRead("CSV_Data//registration.csv").read()

class UnderWritingFlow(SequentialTaskSet):
    from fakes.customer import Customer

    def __init__(self, parent):
        super().__init__(parent)
        self.token = ""
        self.application_id = ""

    def on_start(self):
        self.phone="Phone Not Exist"

        if len(test_data) > 0:
            self.phone = test_data.pop()

    @task
    def get_server_time(self):
        endpoint = "/api/v3/servertime"

        name_thread = "Registration - Get Server Time - " + endpoint

        with self.client.get(endpoint, catch_response=True, name=name_thread) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failure in get server time")

    @task
    def generate_customer(self):
        endpoint = "/api/registration-flow/v1/generate-customer/"
        name_thread = "Registration - Generate Customer - " + endpoint

        data = {
            "phone": self.phone["phone_number"]
        }

        with self.client.post(endpoint, catch_response=True, name=name_thread, data=data) as response:
            print(response.status_code)
            if response.status_code == 201:
                response.success()
            else:
                response.failure("Failure in process generate customer")

    @task
    def register(self):
        endpoint = "/api/registration-flow/v1/register/"

        name_thread = "Registration - Registration Flow - " + endpoint

        data = {
            "phone": self.phone["phone_number"],
            "android_id": registration["android_id"],
            "app_version": app_version["short_form"],
            "pin": "159357",
            "longitude": "106.841866",
            "latitude": "-6.224373",
            "gcm_reg_id": "test"
        }

        with self.client.post(endpoint, catch_response=True, name=name_thread, data=data) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure("Failure in process registration")

    @task
    def login(self):
        endpoint = "/api/pin/v4/login/"

        name_thread = "Login - Login Flow - " + endpoint

        data = {
            "username": self.phone["phone_number"],
            "android_id": registration["android_id"],
            "app_version": app_version["short_form"],
            "pin": "159357",
            "longitude": "106.841866",
            "latitude": "-6.224373",
            "gcm_reg_id": "test"
        }

        with self.client.post(endpoint, catch_response=True, name=name_thread, data=data) as response:
            print(response)
            if response.status_code == 200:
                response.success()

                try:
                    token = response.json()["data"]["token"]
                    self.token = token

                    application_id = response.json()["data"]["applications"][0]["id"]
                    self.application_id = application_id

                except AttributeError:
                    self.token = ""
                    self.application_id = ""

            else:
                response.failure("Failure in process login")

    @task
    def check_existence(self):
        endpoint = "/api/registration-flow/v2/check/"

        name_thread = "Login - Check Existence - " + endpoint

        data = {
            "phone": self.phone["phone_number"]
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

            except AttributeError:
                success_response = ""

            if response.status_code == 200 and success_response == True:
                response.success()
            else:
                response.failure("Failure in get province")

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

            except AttributeError:
                success_response = ""

            if response.status_code == 200 and success_response == True:
                response.success()
            else:
                response.failure("Failure in get detail locations")

    @task
    def check_payslip_mandatory(self):
        endpoint = "/api/v2/mobile/check-payslip-mandatory/"

        name_thread = "SubmitForm - Check payslip mandatory - " + endpoint

        with self.client.get(
            endpoint + self.application_id,
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token}
        ) as response:
            try:
                success_response = response.json()["success"]

            except AttributeError:
                success_response = ""

            if response.status_code == 200 and success_response == True:
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

    @task
    def get_terms_privacy(self):
        endpoint = "/api/v3/termsprivacy"

        name_thread = "SubmitForm - Get Terms Privacy - " + endpoint

        with self.client.get(endpoint, catch_response=True, name=name_thread) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failure in get terms privacy")

    # @task
    # def stop(self):
    #     raise StopUser()

    # def on_stop(self):
    #     print("masuk akhir")
    #     if len(test_data) > 0:
    #         print("masuk akhir2")

    #         self.user.environment.reached_end = True
    #         self.user.environment.runner.quit()
    #     raise StopUser()

class MySeqTest(HttpUser):
    wait_time = constant(1)
    host = "https://api-uat.julofinance.com"
    tasks = [UnderWritingFlow]