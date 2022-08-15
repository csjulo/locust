from locust import HttpUser, task, constant, SequentialTaskSet

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