# Blog Portal

It is a blogging website for everyone who wants to write. Like poems to books.

It is create with "Django" a python framework.

It has the following functionalities:

 - Post:
    1. Add Post
    2. Delete Post
    3. Like Post
    4. Comment On Post
    5. And Of Course View Post
  
 - User
    1. User Signin
    2. User SignUp
    3. User Password Reset
    4. View User Profile
    5. User Profile Edit
    6. Facebook Login

# To get involved in this project 
  
 1. Clone it in your desired directory.
 ```
   git clone https://github.com/jindalpawan/Django.git
```
 2. Make it better.
 3. Commit your changes.
 4. Create a pull request.


# Installation

This project is running on Ubuntu, so this is
probably the easiest environment in which to get things running, but other
distributions of linux should be fine as well.

### Virtual environment (if your system doesn't have it already):

The development environment relies on using a Python [virtual environment][venv]
for tools and portability across platforms. Ensure that you have Python Pip
installed for your platform before proceeding with these instructions.

Windows users can use the [following guide][windows venv]. Specifically, get
Python installed and then use the get-pip.py installer once Python is working

OSX users can use the built in version of Python as long as Pip is available,
or better, install [Brew and Python][osx venv].

Linux users should have Python already installed. Ensure Pip is installed via
your package manager and you should be all set.


## Linux based Setup for development

Note: Ubuntu 16.04 LTS is recommended to use for the development environment.

1. Run the following git clone (specify a directory of your choosing if you like):

        git clone https://github.com/jindalpawan/Portal-using-rest-api

2. Run virtualenv on the git cloned directory to setup the Python virtual environment:

        virtualenv drf

3. cd into the name of the directory into which you cloned the git repository

        cd portaldrf

4. After activating the virtual environment, install the dependencies

        pip install -r requirements.txt

5. You are all set. Run the migrate command

        python manage.py migrate

        
6. You are all set. Run the final command

        python manage.py runserver


7. Its time to rock. Visit [http://localhost:8000][localhost] in your browser and you should be all set.


[venv]: http://pypi.python.org/pypi/virtualenv
[wrapper]: http://www.doughellmann.com/projects/virtualenvwrapper/
[windows venv]: http://docs.python-guide.org/en/latest/starting/install/win/
[osx venv]: http://docs.python-guide.org/en/latest/starting/install/osx/
[localhost]: http://localhost:8000/

