from locust import task, constant, SequentialTaskSet, HttpUser
from locust_plugins.csvreader import CSVReader
from locust.exception import StopUser
from json import JSONDecodeError

# Get data parameterization from CSV
test_data = CSVReader("CSV_Data//autodialer_users.csv")

class AudoDialerFeature(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.csrftoken = ""
        self.username = ""
        self.password = ""

    def on_start(self):
        response = self.client.get("/login/")
        self.csrftoken = response.cookies['csrftoken']

        data_csv = next(test_data)
        self.username = data_csv[0]
        self.password = data_csv[1]

        data = {
            "csrfmiddlewaretoken": self.csrftoken,
            "username": self.username,
            "password": self.password,
            "next": ""
        }

        headers = {
            "Referer": "https://api-staging.julo.co.id/login/"
        }
        with self.client.post(
            "/login/",
            catch_response=True,
            name="POST login",
            data=data,
            headers=headers
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response.text)

    @task
    def get_application_autodialer(self):
        endpoint = "/dashboard/ajax_get_application_autodialer/?csrfmiddlewaretoken={}&options=sales_ops:".format(self.csrftoken)

        name_thread = "Get application autodialer"

        with self.client.get(
            endpoint,
            catch_response=True,
            name=name_thread,
        ) as response:
            if response.status_code == 200:
                print(response.text)
                response.success()
            else:
                response.failure(response.text)

class MySeqTest(HttpUser):
    wait_time = constant(1)
    host = "https://api-staging.julo.co.id"
    tasks = [AudoDialerFeature]

# class StagesShape(LoadTestShape):
#     stages = [
#         #### Load Test ####
#         {"duration": 90, "users": 5, "spawn_rate": 5}, # simulate ramp-up of traffic to 50 users over 25 seconds.
#         {"duration": 230, "users": 10, "spawn_rate": 5}, # simulate ramp-up of traffic to 50 users over 25 seconds.
#         {"duration": 290, "users": 1, "spawn_rate": 1}, # stay at 50 users for around 15 seconds

#         #### Stress Test ####
#         # {"duration": 25, "users": 1, "spawn_rate": 1}, # simulate ramp-up of traffic to 50 users over 15 seconds. (normal load)
#         # {"duration": 40, "users": 5, "spawn_rate": 1}, # stay at 50 users for around 20 seconds
#         # {"duration": 45, "users": 75, "spawn_rate": 20}, # ramp-up to 60 users around 15 seconds (beyond the breaking point)
#         # {"duration": 60, "users": 30, "spawn_rate": 10}, # ramp-down
#         # {"duration": 75, "users": 10, "spawn_rate": 10}, # ramp-down
#         # {"duration": 90, "users": 1, "spawn_rate": 1} # ramp-down to 1 users
        
#         #### Spike Test ####
#         # {"duration": 10, "users": 20, "spawn_rate": 5}, # simulate ramp-up of traffic to 20 users over 10 seconds. (normal load)
#         # {"duration": 35, "users": 100, "spawn_rate": 100}, # stay at 100 users for around 10 seconds
#         # {"duration": 45, "users": 20, "spawn_rate": 20}, # ramp-down to 50 users around 20 seconds (recovery)
#         # {"duration": 55, "users": 10, "spawn_rate": 10}, # ramp-down
#         # {"duration": 65, "users": 1, "spawn_rate": 1} # ramp-down to 1 users
#     ]

#     def tick(self):
#         run_time = self.get_run_time()

#         for stage in self.stages:
#             if run_time < stage["duration"]:
#                 tick_data = (stage["users"], stage["spawn_rate"])
#                 return tick_data

#         return None
