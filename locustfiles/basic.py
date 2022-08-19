from locust import User, task, constant

class BasicTest(User):
    wait_time = constant(1)

    @task
    def say_hello(self):
        print("Hello")

    @task
    def wear_mask(self):
        print("Stay safe")

    @task
    def say_goodbye(self):
        print("Good bye")