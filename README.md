# Reservation task SHORT

Company needs an internal service for its employees which helps them to reserve company
meeting rooms for internal or external meetings. Each employee should be able to check each
room’s availability, book or cancel a reservation through an API.

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
