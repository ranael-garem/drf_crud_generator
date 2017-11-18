# DRF CRUD Generator

Generate Model, Serializer, View and add view to urls.py with a simple command given the **app** and **model name**

## Installation

Installation is available via `pip`

`$ pip install drf_crud_generator`


Add 'drf_crud_generator' to your installed_apps in your `settings.py` file. It should look like the following.

```python
INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	...
	'drf_crud_generator',
	..
)
```
---

## Usage

Run the following command, where app is the application to where the classes will be created

```python
python manage.py crud {app} {model name}
```

### Optional argument: Author name

```python
python manage.py crud {app} {model name} -a {your name}
```
---

### Make Sure your app has the following structure:

```
app  
└───models
│   │   __init__.py
└───serializers
│   │   __init__.py
└───views
│   │   __init__.py   
|___urls.py
```

