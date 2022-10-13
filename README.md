# Prerequisites
* pyenv - [Download & Install pyenv](https://github.com/pyenv/pyenv).
* python - Install python with pyenv. Install python version > v3.7.10 :
```bash
pyenv install 3.7.10
pyenv global 3.7.10
```
* Go to the terminal, and install locust and locust-plugins on your local :
```bash
pip install locust
pip install locust-plugins
```
* Make sure locust is installed with following this code :
```bash
locust --version
```

# How to run the test with web interface
* To run the test please following this code :
  - ```bash
    locust -f /path/to/your/test/case/file
    ```
  - Open your browser, as default you can point it to http://localhost:8089/


# How to run the test using the command line (headless)
* To run the test :
```bash
locust -f /path/to/your/test/case/file --headless -u xxx -r xxx
```

<b><ins>Notes</ins></b>:

`-u` specifies the number of Users to spawn

`-r` specifies the spawn rate (number of users to start per second)

# How to run the test with custom load shapes
If you might want to generate a load spike or ramp up and down at custom times, you can using a <b>LoadTestShape class</b>.

By using a LoadTestShape class you have full control over the user count and spawn rate at all times.

Define a class inheriting the LoadTestShape class in your locust file. If this type of class is found then it will be automatically used by Locust.

In the class you also have access to the <b><i>get_run_time()</b></i> method, for checking how long the test has run for.

<b><ins>Example</ins></b>:

```bash
class StagesShape(LoadTestShape):
    stages = [
        #### Load Test ####
        {"duration": 60, "users": 5, "spawn_rate": 5}, 
        {"duration": 220, "users": 10, "spawn_rate": 10}, 
        {"duration": 300, "users": 1, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
```

<b><ins>Notes</ins></b>:

`duration` specifies the time to stop the running of each stage

`users` specifies the number of Users to spawn in each stage

`spawn_rate` specifies the spawn rate (number of users to start per second) in each stage

# Common options that can be used while run the test using command line (headless)
* `--tags` : List of tags to include in the test, so only tasks with any matching tags will be executed

<b><ins>Example</ins></b>:

```bash
locust -f /path/to/your/test/case/file --headless -u xxx -r xxx --tags specific_tag
```

* `--csv xxx.csv --csv-full-history` : Store current request stats to files in CSV format.

<b><ins>Example</ins></b>:

```bash
locust -f /path/to/your/test/case/file --headless -u xxx -r xxx --csv Test.csv --csv-full-history
```

* `--html xxx.html` : Store HTML report to file path specified.

<b><ins>Example</ins></b>:

```bash
locust -f /path/to/your/test/case/file --headless -u xxx -r xxx --html Test.html
```
