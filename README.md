# Miro_Backend_Dev_Task

1. Install python 3.9+ and pip2. 
2. `python3 -m venv venv ` to create a virtual environment
3. `source venv/bin/activate` to activate the virtual environment
4. `pip install -r requirements.txt` to install all the dependencies
5. Install Docker.
6. `docker compose up` in a new terminal to start the database and redis servers in local

### Setting up Backend Application
1. Change the directory by `cd notesapp/` 
2. `python manage.py makemigrations` to create the migrations
3. `python manage.py migrate` to create the database schema.
4. `python manage.py runserver` to start the server
5. `python manage.py createsuperuser` to create a super admin (optional)
