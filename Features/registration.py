import re
from locust import HttpUser, task, constant, SequentialTaskSet
from utils.readtestdata import CsvRead
from locust.exception import StopUser
from variables.constant import app_version, registration
import random

test_data = CsvRead("CSV_Data//registration.csv").read()

class Registration(SequentialTaskSet):
    def on_start(self):
        self.phone="Phone Not Exist"

        if len(test_data) > 0:
            print('masuk')
            self.phone = test_data.pop()

    @task
    def generate_customer(self):
        data = {
            "phone": self.phone["phone_number"]
        }

        name_thread = "Registration - Generate Customer"

        with self.client.post("/api/registration-flow/v1/generate-customer/", catch_response=True, name=name_thread, data=data) as response:
            print(response.status_code)
            if response.status_code == 201:
                response.success()
            else:
                response.failure("Failure in process registration")

    @task
    def register(self):
        data = {
            "phone": self.phone["phone_number"],
            "android_id": registration["android_id"],
            "app_version": app_version["short_form"],
            "pin": "159357",
            "longitude": "106.841866",
            "latitude": "-6.224373",
            "gcm_reg_id": "test"
        }

        name_thread = "Registration - Registration Flow"

        with self.client.post("/api/registration-flow/v1/register/", catch_response=True, name=name_thread, data=data) as response:
            print(response.status_code)
            print("text:" + response.text)
            if response.status_code == 201:
                response.success()
            else:
                response.failure("Failure in process registration")
                
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
    wait_time = constant(2)
    host = "https://api-uat.julofinance.com"
    tasks = [Registration]