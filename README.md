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
* Put this following code to run the test on web interface :
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
-u specifies the number of Users to spawn
-r specifies the spawn rate (number of users to start per second)


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
