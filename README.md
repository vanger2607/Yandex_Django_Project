# Состояние проекта
[![Django CI](https://github.com/vanger2607/Yandex_Django_Project/actions/workflows/django.yml/badge.svg?branch=dev)](https://github.com/vanger2607/Yandex_Django_Project/actions/workflows/django.yml)
[![flake-8](https://github.com/vanger2607/Yandex_Django_Project/actions/workflows/python-package.yml/badge.svg?branch=dev)](https://github.com/vanger2607/Yandex_Django_Project/actions/workflows/python-package.yml)

# YAMOSGI
Это проект - аналог игры "Борьба умов", нас не все устраивало в Борьбе умов, поэтому мы решили создать свою игру и добавить в нее новые, крутые фичи

## Installation
- ### Create venv
#### Windows
```
python -m venv venv
```
#### Linux
```
python3 -m venv venv
```
- ### Activate venv
#### Windows
(For Windows you need to allow PowerShell scripts to run)
```
Set-ExecutionPolicy Unrestricted -Scope Process
```
```
venv\Scripts\activate.ps1
```
#### Linux
```
source venv/bin/activate
```
- ### Install requirements.txt
```
pip install -r requirements.txt
```
- ### Migrate the migrations
#### Windows
```
cd LyceumProject
python manage.py migrate
```
#### Linux
```
cd LyceumProject
python3 manage.py migrate
```
- ### Load test data from fixtures
#### Windows
```
python manage.py loaddata catalog/fixtures/subjects.json
```
#### Linux
```
python3 manage.py loaddata catalog/fixtures/subjects.json
```
- ### Run the project
#### Windows
```
python manage.py runserver
```
#### Linux
```
python3 manage.py runserver
```
Then go to http://127.0.0.1:8000

To store DEBUG and SECRET_KEY parameters are used environment variables.
You can create and set values, or change the value in settings.py