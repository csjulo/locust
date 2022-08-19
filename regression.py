from locust import HttpUser, task, constant, SequentialTaskSet, LoadTestShape
from locustfiles.example_spike_test import Example
from locustfiles.underwriting_feature import UnderWritingFlow
from locustfiles.basic import BasicTest

class Regression(SequentialTaskSet):
    tasks = [Example, BasicTest]

class MySeqTest(HttpUser):
    wait_time = constant(1)
    host = "https://api-staging.julofinance.com"
    tasks = [Regression]

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
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None