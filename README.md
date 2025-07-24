## Honit Core

Management core of Honit network system.

### How to Run?

1- Provide the necessary ENVs in the local.conf file.

2- Run this commands:

```shell
    python -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
```
