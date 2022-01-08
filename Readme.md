# Keeper Solution Test

Rest API that allows you to create bookmarks. Original task:

Create a REST api for web bookmarks. These bookmarks can be private or public.
After authentication, users can create and delete / update their bookmarks.
They can also view their bookmarks and other users public bookmarks. Anonymous users can
only view public bookmarks.
Every bookmark should have "title","url" and "created_at" fields. Other fields are up to you.


## Installation
```
    virtualenv env
    pip install -r requirements.txt
    source env/bin/activate
```

## Migrations
```
    python manage.py makemigrations
    python manage.py migrate 
```

## Run
``` 
    python manage.py runserver
```

## Tests
``` 
    python manage.py test
```

## Endpoints:
Please refer to endpoints.txt to see full list