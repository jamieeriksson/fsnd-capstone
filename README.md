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

#### Envrionment Variables

##### Dotenv Database Variables

The `config.py` file connects to a database through a `.env` file located in the `/backend` directory. Create the following two variables in order for the api to connect to your own database of choice:

```
DATABASE_URI="postgresql://<user>:<password>@localhost:<port>/<database_name>"
DATABASE_TEST_URI="postgresql://<user>:<password>@localhost:<port>/<test_database_name>"
```

##### Authorization setup.sh Variables

For Udacity reviewers the Auth0 environment variables as well as authorization tokens for testing are located in the `setup.sh` file. To set these variables, move into the `/backend` directory and execute the following:

```bash
. setup.sh
```

## Running the server

From within the `./backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python wsgi.py
```

## Live URL

This API is deployed on Heroku and can be visited at:
https://fsnd-capstone-ultimate-teams.herokuapp.com/

## API Behavior

### Endpoints

GET '/players',  
POST '/players',  
GET '/players/int:player_id',  
PATCH '/players/int:player_id',  
DELETE '/players/int:player_id',  
GET '/teams',  
POST '/teams',  
GET '/teams/int:team_id',  
PATCH '/teams/int:team_id',  
DELETE '/teams/int:team_id',

GET '/players'

- Permissions: none
- Fetches a paginated list of ultimate frisbee players.
- Request Arguments: page number for pagination
- Returns: An object stating a successful request, the total number of players in the database, and the list of objects of individual player details.

  ```
  {
  "players": [
    {
      "gender": "F",
      "id": 1,
      "jersey_number": 15,
      "name": "Doe Johnson",
      "position": "Hybrid",
      "team": "Whiplash"
    },
    {
      "gender": "M",
      "id": 2,
      "jersey_number": 42,
      "name": "John Smith",
      "position": "Handler",
      "team": "WOOF"
    }
  ],
  "success": true,
  "total_players": 2
  }
  ```

POST '/players'

- Permissions: create:players
- Allows user to create a new ultimate frisbee player in the database.
- Request Arguments: player name, gender, jersey number, position player plays, the team they are rostered on (optional)
- Returns: An object stating a successful request and returning the information of the newly created player.
  ```
  {
  "player": {
      "gender": "F",
      "id": 1,
      "jersey_number": 15,
      "name": "Doe Johnson",
      "position": "Hybrid",
      "team": "Whiplash"
    },
  "success": true
  }
  ```

GET '/players/int:player_id'

- Permissions: none
- Retrieves information on an individual player by player id.
- Request Arguments: player id
- Returns: An object stating a successful request and returning the information of the desired player.
  ```
  {
  "player": {
      "gender": "F",
      "id": 1,
      "jersey_number": 15,
      "name": "Doe Johnson",
      "position": "Hybrid",
      "team": "Whiplash"
    },
  "success": true
  }
  ```

PATCH '/players/int:player_id'

- Permissions: update:player
- Allows user to update and change information about a specific player.
- Request Arguments: player id, name, gender, jersey number, position player plays, and the team they are rostered on.
- Returns: An object stating a successful request, the newly updated information of the desired player, and the previous information of the player.
  ```
  {
  "new_player_info_": {
      "gender": "F",
      "id": 1,
      "jersey_number": 15,
      "name": "Doe Johnson",
      "position": "Hybrid",
      "team": "Whiplash"
    },
  "previous_player_info_": {
      "gender": "F",
      "id": 1,
      "jersey_number": 4,
      "name": "Doe Johnson",
      "position": "Cutter",
      "team": "Public Enemy"
    },
  "success": true
  }
  ```

DELETE '/players/int:player_id'

- Permissions: delete:player
- Removes and deletes an individual player from the database by player id.
- Request Arguments: player id
- Returns: An object stating a successful request and the id of the player deleted.
  ```
  {
  "deleted": 1
  "success": true
  }
  ```

GET '/teams'

- Permissions: none
- Fetches a paginated list of ultimate frisbee teams.
- Request Arguments: page number for pagination
- Returns: An object stating a successful request, the total number of teams in the database, and the list of objects of individual team details.

  ```
  {
  "success": true,
  "teams": [
    {
      "division": "Womens",
      "id": 1,
      "level": "College",
      "location": "Richardson, Texas",
      "name": "Whiplash",
      "roster": [
        "Doe Johnson"
      ]
    },
    {
      "division": "Open",
      "id": 2,
      "level": "College",
      "location": "Richardson, Texas",
      "name": "WOOF",
      "roster": [
        "John Smith"
      ]
    }
  ],
  "total_teams": 2
  }
  ```

POST '/teams'

- Permissions: create:teams
- Allows user to create a new ultimate frisbee team in the database.
- Request Arguments: team name, location, division, and level.
- Returns: An object stating a successful request and returning the information of the newly created team.
  ```
  {
  "team": {
      "division": "Open",
      "id": 2,
      "level": "College",
      "location": "Richardson, Texas",
      "name": "WOOF",
      "roster": []
    }
  "success": true
  }
  ```

GET '/teams/int:team_id'

- Permissions: none
- Retrieves information on an individual team by team id.
- Request Arguments: team id
- Returns: An object stating a successful request and returning the information of the desired team.
  ```
  {
  "team": {
      "division": "Open",
      "id": 2,
      "level": "College",
      "location": "Richardson, Texas",
      "name": "WOOF",
      "roster": []
    }
  "success": true
  }
  ```

PATCH '/teams/int:team_id'

- Permissions: update:team
- Allows user to update and change information about a specific team.
- Request Arguments: team id, team name, location, division, and level.
- Returns: An object stating a successful request, the newly updated information of the desired team, and the previous information of the team.
  ```
  {
  "new_team_info_": {
      "division": "Open",
      "id": 2,
      "level": "College",
      "location": "Richardson, Texas",
      "name": "WOOF",
      "roster": []
    },
  "previous_team_info_": {
      "division": "Mixed",
      "id": 2,
      "level": "College",
      "location": "Dallas, Texas",
      "name": "WOOF",
      "roster": [
        "Doe Johnson",
        "John Smith"
      ]
    },
  "success": true
  }
  ```

DELETE '/teams/int:team_id'

- Permissions: delete:team
- Removes and deletes an individual team from the database by team id.
- Request Arguments: team id
- Returns: An object stating a successful request and the id of the team deleted.
  ```
  {
  "deleted": 1
  "success": true
  }
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

You will need JWTs for an Admin user and a Team Manager user in order to run the unit tests. These JWTs should have been exported as environment variables when you ran the `setup.sh` file. You can check if these variables set correctly by executing:

```bash
echo "$ADMIN_TOKEN"
echo "$TEAM_MANAGER_TOKEN"
```

### Running the Test Files

To run all of the tests execute:

```bash
python test_app.py
```
