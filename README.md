remote-sytem-users
==============

Python web app for finding all users on a remote Ubuntu system. It also marks users with root and interactive shell privileges in a nice tabular format. Uses the python `paramiko` module for SSH into remote system.

How to run
------------------

It is always a good idea using a virtual environment to run your
application. That will avoid interference from your hosting
environment. That can be done using [virtualenv](https://virtualenv.pypa.io/en/stable/):

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ python server.py

Application can now be accessed at localhost:3000

Testing the app
---------------------------

Input your Remote sytem's IP, username and password in the form and click on submit.
If SSH is successful, it will list all users in a neat tabular format.

> :)
