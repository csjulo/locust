from http import client
from locust import HttpUser, task, constant, SequentialTaskSet, LoadTestShape, events
from influxdb import InfluxDBClient
import json
import socket
import datetime
import pytz

host=socket.gethostname()
client=InfluxDBClient(host="localhost",port="8086")
client.switch_database("locust")

@events.request_success.add_listener
def individual_success_handle(request_type, name, response_time, response_length, **kwargs):
    SUCCESS_TEMPLATE = '[{"measurement": "%s","tags": {"hostname":"%s","requestName": "%s","requestType": "%s","status":"%s"' \
                    '},"time":"%s","fields": {"responseTime": "%s","responseLength":"%s"}' \
                    '}]'
    json_string = SUCCESS_TEMPLATE % ("ResponseTable", host, name, request_type, "SUCCESS", datetime.datetime.now(tz=pytz.UTC), response_time, response_length)
    client.write_points(json.loads(json_string))

@events.request_failure.add_listener
def individual_fail_handle(request_type, name, response_time, response_length, exception, **kwargs):
    FAIL_TEMPLATE = '[{"measurement": "%s","tags": {"hostname":"%s","requestName": "%s","requestType": "%s","exception":"%s","status":"%s"' \
                    '},"time":"%s","fields": {"responseTime": "%s","responseLength":"%s"}' \
                    '}]'
    json_string = FAIL_TEMPLATE % ("ResponseTable", host, name, request_type, exception, "FAIL", datetime.datetime.now(tz=pytz.UTC),response_time, response_length)
    client.write_points(json.loads(json_string))

class Example(SequentialTaskSet):
    @task
    def get_server_time(self):
        res = self.client.get("/api/v3/servertime")
        print("Status is 1 : ", res.status_code)

    @task
    def get_privacy(self):
        res = self.client.get("/api/v2/privacy")
        print("Status is 2 : ", res.status_code)

class MySeqTest(HttpUser):
    wait_time = constant(1)
    host = "https://api-staging.julofinance.com"
    tasks = [Example]

    events.request_success.add_listener(individual_success_handle)
    events.request_failure.add_listener(individual_fail_handle)


# class StagesShape(LoadTestShape):
#     """
#     A simply load test shape class that has different user and spawn_rate at
#     different stages.
#     Keyword arguments:
#         stages -- A list of dicts, each representing a stage with the following keys:
#             duration -- When this many seconds pass the test is advanced to the next stage
#             users -- Total user count
#             spawn_rate -- Number of users to start/stop per second
#             stop -- A boolean that can stop that test at a specific stage
#         stop_at_end -- Can be set to stop once all stages have run.
#     """

#     stages = [
#         {"duration": 5, "users": 10, "spawn_rate": 10},
#         {"duration": 15, "users": 50, "spawn_rate": 10},
#         {"duration": 25, "users": 100, "spawn_rate": 10}
#     ]

#     def tick(self):
#         run_time = self.get_run_time()

#         for stage in self.stages:
#             if run_time < stage["duration"]:
#                 tick_data = (stage["users"], stage["spawn_rate"])
#                 return tick_data

#         return None