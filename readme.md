#### Coding Challenge Submission Tadgh Wagstaff

Hi! Thanks for reading, please see a few notes about this solution below

#### Notes: 

1) I decided to use Python for this solution to compliment my Java-based REST API available [here](https://github.com/TadghW/pprRank). 

2) I was informed that the Python team use Flask, so I decided to work with Flask for this solution

2) Although both teams use AWS I decided that using a remote db exceeded the scope of this assignment. Instead, I used a local database instance with SQLite 3, a combination suggested in the [Flask documentation](https://flask.palletsprojects.com/en/2.2.x/patterns/sqlite3/)

3) Because the documentation states that the solution should be considered a proof of concept I haven't done performance testing or implemented query caching. I also haven't containerised or hosted the application. You can find a containerised and hosted example of [this project](https://github.com/TadghW/pprRank) [here](https://headphones.science)

4) You can interface with the program directly by sending requests to the endpoints, or through a dashboard I made by visiting localhost:5000 in your browser

#### How to run: 

All of the packages and libraries required to run this application are installed in the python virtual environment found at /env. You can enter the virtual environment by running env/Scripts/activate for your operating system from your command line interface. 

Once inside the virtual environment you can run this application by navigating to this project's root directory and using the command `python app.py`

Once the application is running, you can run the integrations tests I wrote for the app with `test_integration_tests.py`

