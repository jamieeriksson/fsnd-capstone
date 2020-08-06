# FSND Capstone - Ultimate Frisbee Team Management Backend

## About the Project

This application was created for the Udacity Fullstack Nanodegree Capstone project. It contains a Flask application for an ultimate frisbee team and player management site. It keeps track of registered players and teams and allows you to roster players under the teams they are playing for each season.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

This project was built using pipenv for the virtual environment. All of the project dependencies are stored in the `Pipfile` file. Install dependencies by naviging to the `/backend` directory and running:

```bash
pipenv install
```

This will install all of the required packages within the `Pipfile` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

#### Dotenv File and Variables

The `config.py` file connects to a database through a `.env` file located in the `/backend` directory. Create the following two variables in order for the api to connect to your own database of choice:

```
DATABASE_URI="postgresql://<user>:<password>@localhost:<port>/<database_name>"
DATABASE_TEST_URI="postgresql://<user>:<password>@localhost:<port>/<test_database_name>"
```

## Running the server

From within the `./backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python wsgi.py
```

## Authorization

To log in or create an account for this application you can visit:
https://dev-pfwmgsv1.us.auth0.com/authorize?audience=players-and-teams&response_type=token&client_id=sZZv3qbFKlOj1QqgTfogb2O5vGdRQWm7&redirect_uri=http://0.0.0.0:8080/players

To log out of an account visit:
https://dev-pfwmgsv1.us.auth0.com/logout

### Permissions and Roles

#### Permissions:

- create:players
- update:players
- delete:players
- create:teams
- update:teams
- delete:teams

#### Roles:

- **Regular User** (no credentials): Can get player and team information.
- **Team Manager**: Can update team information.
  - update:teams
- **Admin**: Can create teams and players, can update teams and players, can delete teams and players.
  - create:players
  - update:players
  - delete:players
  - create:teams
  - update:teams
  - delete:teams

## Testing

### Setting up Authorization Credentials for Testing

You will need JWTs for an Admin user and a Team Manager user in order to run the unit tests. In the `test_credentials.txt` file there are JWTs for both an Admin and Team Manager users. Copy these variables into your `.env` file before running the test files.

### Running the Test Files

To run all of the tests execute:

```bash
python test_app.py
```
