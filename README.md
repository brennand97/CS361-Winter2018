# CS361-Winter2018
Oregon State University CS361 Winter 2018 group project.

## Setup
1. Run `git clone https://github.com/brennand97/CS361-Winter2018.git` to get the repository.
2. Change directories `cd CS361-Winter2018`.
3. Run `pip install -r requirments.txt` to install the dependencies (run this inside of a virtual environment if you like).
4. Setup the database (needs to be done everytime there is a model change):
    1. `python manage.py makemigrations`
    2. `python manage.py migrate`
5. Run `python manage.py loaddata test_data` to load the test data into the database.
6. Create an superuser with `python manage.py createsuperuser` &mdash; this is used to log in to the admin interface at '\admin'.
    1. Note: A super user with username 'admin' and password 'adminadmin' is already provided in the test data fixture.
7. Run the development server with `python manage.py runserver`.
8. Navigate your browser to http://localhost:8000.
