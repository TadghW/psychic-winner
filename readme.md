#### Coding Challenge Submission Tadgh Wagstaff

#### Notes: 

1) I'm using Python here but have an example of a Java based REST API available [here](https://github.com/TadghW/pprRank). I was informed that the Python team use the Flask web framework, so I'll be using Flask for this solution.

2) I believe that both teams use AWS - I considered using Amazon RDS to fit into that pattern but I think that's probably overengineering for this solution. Instead I'll be using SQLite 3, a combination suggested in the [Flask documentation](https://flask.palletsprojects.com/en/2.2.x/patterns/sqlite3/).

3) As the challenge document states that this application should be considered a proof of concept, I won't be implementing performance testing or query caching, and I won't be containerising or hosting the application. You can find a containerised and hosted example of [this project](https://github.com/TadghW/pprRank) [here](https://headphones.science).

4) To keep the solution concise I won't be using libraries like postman or marshmallow, but an expanded version could implement a plethora of other tools for expandability and scalability. I will be using SQLAlchemy because I think provides concise syntax, and it writes better SQL queries than me. I'm won't be using HTML templating either, as I'm only including a very basic UI.


#### How to run: 

All of the packages and libraries required to run this application are installed in the python virtual environment found at /env. You can enter the virtual environment by running the appropriate version of env/Scripts/activate for your operating system from your command line interface. 

Once inside the virtual environment you can run this application by navigating to this project's root directory and using the command `python app.py` 

When the program is running, you can interact with it by accessing the url "localhost:5000" from your web browser of choice. 

