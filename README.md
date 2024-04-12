# Secure Face Authentication System

> ## Setup and Installation of dependencies

- Clone this repository
```
git clone https://github.com/yadhumanikandan/secure-face-authentication-in-web.git

cd secure-face-authentication-in-web
```
- Create virtual environment `env`
```
python -m venv env

env/Scripts/activate
```
- Install `requirements.txt`
```
pip install -r requirements.txt
```
- Befor running the app make sure that all the `Essentials for running the application` is done.
- Run the app
```
python app.py
```

> ## Esentials for running the application

- virtual environment must be named `env`.
- `training_data/` directory should be created in the root directory.
- `data/` directory should be created in the root directory.
- Create `CREDS.py` file in `app/` folder.
- Make three variables in `CREDS.py` file named `APP_PASSWORD`, `SECRET_KEY` and `EMAIL` passing the values of the app password for gmail, secret key for flask app and sender email address for which the app passwrod belongs to.


> ## SMARTPHONE CAMERA ACCESS PROBLEM

### If you are using this for a development environment and want to test it on your phone you can do the following:
```
Go to: chrome://flags/#unsafely-treat-insecure-origin-as-secure
Enable `Insecure origins treated as secure`
Add the addresses for which you want to ignore this policy
Restart chrome
```