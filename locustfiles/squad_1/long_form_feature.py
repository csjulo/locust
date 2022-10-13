from locust import task, constant, SequentialTaskSet, FastHttpUser, LoadTestShape, TaskSet, tag, constant_throughput, constant_pacing
from locust_plugins.csvreader import CSVReader
from locust.exception import StopUser
from json import JSONDecodeError
import random
from fakes.constant import app_version, registration
from fakes.customer import Customer as customers

# Get data parameterization from CSV
test_data = CSVReader("CSV_Data//registration_long_form.csv")

class LongFormFeature(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.token = ""
        self.application_id = ""
        self.nik = ""
        self.email = ""
        self.image_id = ""
        self.province = ""
        self.city = ""
        self.district = ""
        self.sub_district = ""
        self.device_id = ""

    @tag('x0', 'x100', '105')
    @task
    def set_initial_data(self):
        data_csv = next(test_data)
        self.nik = data_csv[0]
        self.email = data_csv[1]

    @tag('x0')
    @task
    def get_server_time(self):
        endpoint = "/api/v3/servertime"

        name_thread = "Get server time - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failure in get server time")

    @tag('x0')
    @task
    def get_privacy(self):
        endpoint = "/api/v2/privacy"

        name_thread = "Get privacy - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failure in get privacy")

    @tag('x0')
    @task
    def check_strong_pin(self):
        endpoint = "/api/pin/v1/check-strong-pin/"

        name_thread = "Check Strong pin - " + endpoint

        data = {
            "pin": "159357",
        }

        with self.client.post(
            endpoint,
            catch_response=True,
            name=name_thread,
            data=data,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failure in check strong pin")

    @tag('x0')
    @task
    def register(self):
        endpoint = "/api/pin/v1/register/"

        name_thread = "Registration Flow - " + endpoint

        data = {
            "username": self.nik,
            "email": self.email + "@julo.co.id",
            "android_id": "apitest3423",
            "app_version": "7.5.0",
            "pin": "159357",
            "longitude": "106.841866",
            "latitude": "-6.224373",
            "gcm_reg_id": "test"
        }

        with self.client.post(endpoint, catch_response=True, name=name_thread, data=data) as response:
            if response.status_code == 201:
                response.success()
                try:
                    token = response.json()["data"]["token"]
                    self.token = token

                    application_id = response.json()["data"]["applications"][0]["id"]
                    self.application_id = application_id

                    device_id = response.json()["data"]["device_id"]
                    self.device_id = device_id

                except JSONDecodeError:
                    response.failure("Response could not be decoded as JSON")
                    
                except KeyError:
                    response.failure("Response did not contain expected key")

            else:
                response.failure(response.text)

    @tag('x0')
    @task
    def get_version_check(self):
        endpoint = "/api/v2/version/check?version_name=7.5.0"

        name_thread = "Get version check - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failure in get version check")

    @tag('x0')
    @task
    def get_additional_info(self):
        endpoint = "/api/v2/additional/info"

        name_thread = "Get additional info - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failure in get additional info")


    @tag('x100')
    @task
    def get_customer_module(self):
        endpoint = "/api/customer-module/v1/user-config?app_version=7.5.0"

        name_thread = "Get customer module - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token},
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @tag('x100')
    @task
    def get_longform_settings(self):
        endpoint = "/api/application_flow/v1/longform/setting"

        name_thread = "Get customer module - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token},
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @tag('x100')
    @task
    def get_application(self):
        endpoint = "/api/v1/applications/"

        name_thread = "Get application - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token},
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)
    
    @tag('x100')
    @task
    def get_mobile_feature_setting(self):
        endpoint = "/api/v2/mobile/feature-settings?feature_name=form_selfie"

        name_thread = "Get mobile feature setting form selfie - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token},
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @tag('x100')
    @task
    def check_payslip_mandatory(self):
        endpoint = "/api/v2/mobile/check-payslip-mandatory/"

        name_thread = "Get payslip mandatory - " + endpoint

        with self.client.get(
            endpoint + str(self.application_id),
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token},
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @tag('x100')
    @task
    def liveness_detection_pre_check(self):
        endpoint = "/api/liveness-detection/v1/pre-check"

        name_thread = "Liveness detection pre check - " + endpoint

        with self.client.post(
            endpoint,
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token},
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    # @tag('x100')
    # @task
    # def liveness_detection_pre_active_check(self):
    #     endpoint = "/api/liveness-detection/v1/pre-active-check"

    #     name_thread = "Liveness detection pre active check - " + endpoint

    #     with self.client.post(
    #         endpoint,
    #         catch_response=True,
    #         name=name_thread,
    #         headers={"authorization": "Token " + self.token},
    #     ) as response:
    #         if response.status_code == 200:
    #             response.success()
    #         else:
    #             response.failure(response.text)

    @tag('x100')
    @task
    def scrape_data(self):
        endpoint = "/api/v2/etl/dsd/"

        name_thread = "Scrape Data - " + endpoint

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

    # @tag('x100')
    # @task
    # def get_setting_ocr_timeout(self):
    #     endpoint = "/api/ocr/v2/setting/ocr_timeout"

    #     name_thread = "Get setting ocr timeout - " + endpoint

    #     with self.client.post(
    #         endpoint,
    #         catch_response=True,
    #         name=name_thread,
    #         headers={"authorization": "Token " + self.token},
    #     ) as response:
    #         if response.status_code == 200:
    #             response.success()
    #         else:
    #             response.failure(response.text)

    @tag('x100')
    @task
    def j1_submit_ktp_ocr(self):
        endpoint = "/api/ocr/v3/ktp/"

        name_thread = "Upload ktp - " + endpoint

        data = {"file_name": "ktp_test.jpg", "retries": 5}

        files = {"image": open("upload_file//image.png", "rb"), "raw_image": open("upload_file//image.png", "rb")}

        with self.client.post(endpoint,
                catch_response=True, 
                name=name_thread, 
                data=data,
                files=files,
                headers={"authorization": "Token " + self.token},
            ) as response:

            if response.status_code == 200:
                response.success()

                try:
                    image_id = response.json()["data"]["image"]["image_id"]
                    self.image_id = image_id

                except JSONDecodeError:
                    response.failure("Response could not be decoded as JSON")
                    
                except KeyError:
                    response.failure("Response did not contain expected key")
            else:
                response.failure(response.text)

    @tag('x100')
    @task
    def j1_submit_ktp(self):
        endpoint = "/api/ocr/v2/ktp/submit/"

        name_thread = "Submit ktp - " + endpoint

        data = {"image_id": self.image_id}

        with self.client.post(endpoint,
                catch_response=True, 
                name=name_thread, 
                data=data,
                headers={"authorization": "Token " + self.token},
            ) as response:

            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @tag('x100')
    @task
    def get_mobile_feature_setting_mother_maiden_name(self):
        endpoint = "/api/v2/mobile/feature-settings?feature_name=mother_maiden_name"

        name_thread = "Get mobile feature setting mother maiden name - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token},
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @tag('x100')
    @task
    def get_mobile_feature_setting_birth_place(self):
        endpoint = "/api/v2/mobile/feature-settings?feature_name=set_birth_place_required"

        name_thread = "Get mobile feature setting birth place - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token},
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @tag('x100')
    @task
    def upload_selfie(self):
        endpoint = "/api/face_recognition/v1/selfie/check-upload"

        name_thread = "Upload Selfie - " + endpoint

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
                response.failure(response.text)

    @tag('x100')
    @task
    def get_url_image(self):
        endpoint = "/api/application_flow/v1/get_application_image_url/?image_id="

        name_thread = "Get url image - " + endpoint

        with self.client.get(
            endpoint + str(self.image_id),
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token},
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @tag('x100')
    @task
    def get_province(self):
        endpoint = "/api/v3/address/provinces"

        name_thread = "Get Province - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token}
        ) as response:
            try:
                success_response = response.json()["success"]
                province = response.json()["data"]
                if response.status_code == 200 and success_response == True:
                    response.success()

                    pick_random_province = random.randint(0, len(province) - 1)
                    self.province = pick_random_province

                else:
                    response.failure(response.text)

            except JSONDecodeError:
                response.failure("Response could not be decoded as JSON")

            except KeyError:
                response.failure("Response did not contain expected key")

    @tag('x100')
    @task
    def get_cities(self):
        endpoint = "/api/v3/address/cities"

        name_thread = "Get Cities - " + endpoint

        data = {"province": self.province}

        with self.client.post(
            endpoint,
            catch_response=True,
            name=name_thread,
            data=data,
            headers={"authorization": "Token " + self.token}
        ) as response:
            print(f"response cities : {response.text}")
            try:
                if response.status_code == 200:
                    response.success()

                    city = response.json()["data"]
                    pick_random_city = random.randint(0, len(city) - 1)
                    self.city = pick_random_city

                else:
                    response.failure(response.text)

            except JSONDecodeError:
                response.failure("Response could not be decoded as JSON")

            except KeyError:
                response.failure("Response did not contain expected key")

    @tag('x100')
    @task
    def get_address_districts(self):
        endpoint = "/api/v3/address/districts"

        name_thread = "Get districts - " + endpoint

        data = {"province": self.province, "city": self.city}

        with self.client.post(
            endpoint,
            catch_response=True,
            name=name_thread,
            data=data,
            headers={"authorization": "Token " + self.token}
        ) as response:
            print(f"response districts : {response.text}")
            try:
                if response.status_code == 200:
                    response.success()

                    district = response.json()["data"]
                    pick_random_district = random.randint(0, len(district) - 1)
                    self.district = pick_random_district

                else:
                    response.failure(response.text)

            except JSONDecodeError:
                response.failure("Response could not be decoded as JSON")

            except KeyError:
                response.failure("Response did not contain expected key")

    # @tag('x100')
    # @task
    # def get_address_subdistricts(self):
    #     endpoint = "/api/v3/address/subdistricts"

    #     name_thread = "Get sub districts - " + endpoint

    #     data = {"province": self.province, "city": self.city, "district": self.district}

    #     with self.client.post(
    #         endpoint,
    #         catch_response=True,
    #         name=name_thread,
    #         data=data,
    #         headers={"authorization": "Token " + self.token}
    #     ) as response:
    #         try:
    #             if response.status_code == 200:
    #                 response.success()

    #                 sub_district = response.json()["data"]
    #                 pick_random_sub_district = random.randint(0, len(sub_district) - 1)
    #                 self.sub_district = pick_random_sub_district

    #             else:
    #                 response.failure(response.text)

    #         except JSONDecodeError:
    #             response.failure("Response could not be decoded as JSON")

    #         except KeyError:
    #             response.failure("Response did not contain expected key")

    @tag('x100')
    @task
    def request_otp(self):
        endpoint = "/api/otp/v1/request"

        name_thread = "OTP request - " + endpoint

        data = {
            "action_type": "verify_phone_number",
            "android_id": registration["android_id"],
            "otp_service_type": "sms",
            "phone_number": registration["phone"],
        }

        with self.client.post(endpoint,
                catch_response=True, 
                name=name_thread, 
                data=data,
                headers={"authorization": "Token " + self.token},
            ) as response:

            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @tag('x100')
    @task
    def get_list_bank(self):
        endpoint = "/api/v3/product-line/10/dropdown_bank_data?is_show_log=true"

        name_thread = "Get list bank - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token},
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @tag('x100')
    @task
    def get_mobile_feature_setting_boost(self):
        endpoint = "/api/v2/mobile/feature-settings?feature_name=boost"

        name_thread = "Get mobile feature setting boost - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token},
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @tag('x100')
    @task
    def get_booster_status(self):
        endpoint = "/api/v3/booster/status/"

        name_thread = "Get booster status - " + endpoint

        with self.client.get(
            endpoint + str(self.application_id),
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token},
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @tag('x100')
    @task
    def get_termsprivacy(self):
        endpoint = "/api/v3/termsprivacy"

        name_thread = "Get terms privacy - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token},
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @tag('x105')
    @task
    def j1_form_submission(self):
        endpoint = "/api/v3/application/"

        name_thread = "Form Submission - " + endpoint

        form_submission_data = customers().generate_form_submission_params(device_id=self.device_id)

        with self.client.patch(
            endpoint + str(self.application_id),
            catch_response=True, 
            name=name_thread, 
            data=form_submission_data,
            headers={"authorization": "Token " + self.token},
        ) as response:

            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @tag('x105')
    @task
    def clcs_scrape_check(self):
        endpoint = "/api/v2/etl/clcs-scraped-checking/"

        name_thread = "Clcs scraped checking - " + endpoint

        with self.client.get(
            endpoint + str(self.application_id),
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token},
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @tag('x105')
    @task
    def get_credit_info(self):
        endpoint = "/api/customer-module/v3/credit-info"

        name_thread = "Get credit info - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token},
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @tag('x105')
    @task
    def get_info_card(self):
        endpoint = "/api/streamlined_communication/v1/android_info_card"

        name_thread = "Get info card - " + endpoint

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
            headers={"authorization": "Token " + self.token},
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    # @task
    # def stop(self):
    #     raise StopUser()

class MySeqTest(FastHttpUser):
    # wait_time = constant_throughput(5)
    # wait_time = constant_pacing(5)
    wait_time = constant(1)
    host = "https://api-staging.julofinance.com"
    tasks = [LongFormFeature]

class StagesShape(LoadTestShape):
    stages = [
        #### Load Test ####
        {"duration": 60, "users": 5, "spawn_rate": 5}, # simulate ramp-up of traffic to 50 users over 25 seconds.
        {"duration": 220, "users": 10, "spawn_rate": 10}, # simulate ramp-up of traffic to 50 users over 25 seconds.
        {"duration": 300, "users": 1, "spawn_rate": 1}, # stay at 50 users for around 15 seconds

        #### Stress Test ####
        # {"duration": 25, "users": 1, "spawn_rate": 1}, # simulate ramp-up of traffic to 50 users over 15 seconds. (normal load)
        # {"duration": 40, "users": 5, "spawn_rate": 1}, # stay at 50 users for around 20 seconds
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
