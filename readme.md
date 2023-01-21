### Challenge Submission Tadgh Wagstaff

##### Notes: 

1) I'm using Python here but have an example of a Java based REST API available on my GitHub page. I was informed that the Python team use the Flask web framework, so I'll be doing the same here.

2) I believe that both teams use AWS. I don't know what database technologies either team prefer, but I have an example of an API using a document-based database available on my GitHub so for this submission I'm going to use Amazon RDS.

3) As the challenge document states that this application should be considered a proof of concept, I won't be implementing performance testing or query caching, and I won't be containerising or hosting the application.


##### How to run: 

All of the packages and libraries required to run this application are installed in the python virtual environment found at /env. You can enter the virtual environment by running env/Scripts/activate from your command line interface. 

Once inside the virtual environment you can run this application by navigating to this project's root directory and using the command `python3 main.py` 

When the program is running, you can interact with it by entering the domain "localhost:5050" into the url bar of your browser of choice. 

