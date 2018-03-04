# CS361-Winter2018
Oregon State University CS361 Winter 2018 group project.

## Setup
1. Run `git clone https://github.com/brennand97/CS361-Winter2018.git` to get the repository.
2. Change directories `cd CS361-Winter2018`.
3. Setup the database (needs to be done everytime there is a model change):
    1. `python manage.py makemigrations`
    2. `python manage.py migrate`
4. Create an superuser with `python manage.py createsuperuser` -- this is used to log in to the admin interface at '\admin'.
5. Run the development server with `python manage.py runserver`.
6. Navigate your browser to http://localhost:8000.
