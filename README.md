# Intro
This README file provides instructions on how to run the WMRC project as well as some info on the more important files.

# Development Environment
This project was created with Ubuntu 20.04.2 LTS and Python 3.8.5. However, setup on other OS platforms should be very similar to this one.

# Setup

## Dependencies
As the zipped project folder comes with a python virtual environment (with installed packages), you should be able to skip this step. However, in the case of an error, you can rebuild the virtual environment as such:

```
    - cd to rooms (top level) folder - 
    
    python -m venv venv         # create virtual environment in folder venv

    source venv/bin/activate    # activate the virtual environment

    pip --version               # should show some version and confirm that pip is working correctly

    pip install --timeout 1000 -r requirements.txt      # should install all dependencies, which are listed in requirements.txt
```

## Database
The original project uses mysql. However, as mysql is relatively complex to install and probably has different installations for different OSes, it is better to temporarily use sqlite instead. Django supports sqlite by default with no need for additional installations. 

To change the underlying database, go to [settings.py](./rooms/settings.py), go to line 87, then uncomment lines 88-91 and comment out lines 92-97, as shown below.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'OPTIONS': {
    #         'read_default_file': os.path.join(BASE_DIR, 'database.cnf')
    #     }
    # }
}
```

The sqlite database file is already included in the project (db.sqlite3) and comes with a single admin account created in the system:
```
    Admin Name: for_testing
    Admin Pass: admin161720
```

From there, you will be able to invite new users, create rooms, setup location, etc...  


# Running the project
Open a new terminal and type in the following commands:

```
    - cd to rooms top level folder - 
    source venv/bin/activate            # activates python's virtual environment
    python manage.py runserver          # runs the development server on localhost:8000
```

# The development files
If you would like to have a look at the code, the **main** files are in the following locations:  

For the accounts part:
```
    accounts/views.py           # The views/backend logic
    accounts/models.py          # Database models
    accounts/forms.py           # Input forms
    accounts/urls.py            # Url mappings
    accounts/templates/accounts/*.html      # The HTML pages
```

For the room manager (the main part):
```
    room_manager/static/...         # JS and CSS files
    room_manager/templates/room_manager/...     # HTML pages
    room_manager/*views.py          # The views
    room_manager/*forms.py          # Input forms
    room_manager/*models.py         # Database models
    room_manager/urls.py            # Url mappings
    room_manager/tests.py           # Automated tests
```


Base templates, dependencies, etc:

```
    rooms/static        # Mostly imported JS and CSS files, jQuery, Bootstrap, etc.
    rooms/templates     # Base templates
    rooms/urls          # Base urls
```

If you would like to learn more about the different files and Django:  
https://docs.djangoproject.com/en/3.1/intro/tutorial01/