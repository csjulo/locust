from http import client
from locust import HttpUser, task, constant, SequentialTaskSet, LoadTestShape, events, TaskSet, tag
from influxdb import InfluxDBClient
from locust.exception import StopUser
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

class Example(SequentialTaskSet):
    @tag('tag1')
    @task
    def get_server_time(self):
        res = self.client.get("/api/v3/servertime")
        print("Status is 1 : ", res.status_code)

    @tag('tag2')
    @task
    def get_privacy(self):
        res = self.client.get("/api/v2/privacy")
        print("Status is 2 : ", res.status_code)

    # @task
    # def stop(self):
        # self.interrupt()
        # raise StopUser()

class MySeqTest(HttpUser):
    wait_time = constant(1)
    host = "https://api-staging.julofinance.com"
    tasks = [Example]

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
        {"duration": 25, "users": 50, "spawn_rate": 2}, # simulate ramp-up of traffic to 50 users over 25 seconds.
        {"duration": 50, "users": 50, "spawn_rate": 50}, # stay at 50 users for around 25 seconds
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