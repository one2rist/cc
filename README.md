# Reservation task SHORT

Company needs an internal service for its employees which helps them to reserve company
meeting rooms for internal or external meetings. Each employee should be able to check each
room’s availability, book or cancel a reservation through an API.

## Requirements for implementation:
* There should be an API for:
    * Get meeting room reservations
    * Create reservation(Reservation has title, from and to dates, employees)
    * Cancel reservation
* It’s assumed that these APIs will be with public access
* Reasonable amount of automated tests
* Solution should be uploaded to version control
* Solution should be built using: Django and Python3, Django Rest Framework, SQL
* tabase of your choice (PostgreSQL, SQLite, MySQL, etc)
* PEP8 rules must be followed. Additional linters are welcomed (PyLint, Flake8)
* Project README.md must be created with launch instructions

## Installation


```bash
git clone ...
cd path/to/project
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cd apps
python manage.py migrate
deactivate
```

## Tests

```bash
source env/bin/activate
cd apps
python -Wa manage.py test
```

## Usage
Run test server on a local machine:

```bash
source env/bin/activate
cd apps
#create superuser, use '1' as a password:
python manage.py createsuperuser --username super --email super@gmail.com
#run server:
python manage.py runserver 8000
```

Check API request examples:

```bash
#post room:
http -a super:1 POST http://127.0.0.1:8000/api/rooms/ title="Room 1"

#list rooms:
http GET http://127.0.0.1:8000/api/rooms/

#post reservation for Room id=1:
http -a super:1 POST http://127.0.0.1:8000/api/reservations/ \
title="Booking 1" \
room=1 \
start="2022-01-01T01:00:00Z" \
end="2022-01-01T02:00:00Z" \
organizer=1 \
employees:="[1]"

#post reservation for the same Room and overlapping time will be rejected

#get reservations for Room id=1:
http GET http://127.0.0.1:8000/api/rooms/1/

#delete Reservation id=1:
http -a super:1 DELETE http://127.0.0.1:8000/api/reservations/1/

```

Or test in [WEB-API](http://localhost:8000/api)

## Docker
built with nginx/gunicorn, so it is better to run on port 80 in order to make hyperlinks work properly:
```bash
docker run -it -p 80:8020 \
-e DJANGO_SUPERUSER_USERNAME=admin \
-e DJANGO_SUPERUSER_PASSWORD=sekret1 \
-e DJANGO_SUPERUSER_EMAIL=admin@example.com \
one2rist/cc:cc
