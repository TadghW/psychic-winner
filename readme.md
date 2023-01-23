## Coding Challenge Submission Tadgh Wagstaff

*Please see about this solution and instructions on how to run the software below*

### Notes: 

1) I decided to use Python for this solution to compliment my Java-based REST API available [here](https://github.com/TadghW/pprRank). 

2) I was informed that the Python team use Flask, so I decided to work with Flask for this solution

2) Although both teams use AWS I decided that using a remote db exceeded the scope of this assignment. Instead, I used a local database instance with SQLite 3, a combination suggested in the [Flask documentation](https://flask.palletsprojects.com/en/2.2.x/patterns/sqlite3/)

3) Because the documentation states that the solution should be considered a proof of concept I haven't done performance testing or implemented query caching. I also haven't containerised or hosted the application. You can find a containerised and hosted example of [this project](https://github.com/TadghW/pprRank) [here](https://headphones.science)

4) You can interface with the program directly by sending requests to the endpoints, or through a dashboard I made by visiting localhost:5000 in your browser

### How to run: 

**Step 1 - Create virtual environment:** Create a new python virtual environment at the root of this directory using [venv](https://docs.python.org/3/library/venv.html#module-venv)

**Step 2 - Enter virtual environment:** Using a terminal / CLI navigate to ``env/Scripts`` (Windows) or ``env/bin`` (MacOS, Linux, Unix-based OS) and run `activate` to enter the virtual environment 

**Step 3 - Install requirements:** Navigate back to the root folder in the terminal and enter the command `pip install -r requirements.txt`

**Step 4 - Launch API + Integration Testing:** Now you can launch the API from the terminal with `python3 app.py`. Once the application is running, you can run the accompanying integration tests from the terminal with `python3 test_integration_tests.py`

