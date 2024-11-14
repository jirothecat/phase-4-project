# Recipe API

## This project serves as a React front to Flask backend connection.

A website designed to share, create and comment on recipes. 


## Setup

### `server/`

In the server directory, run the following to initialize the backend:

```console
pipenv install
pipenv shell
```


```console
python server/app.py
```


### `client/`

For our React frontend, change into the client directory and run the following: 

```console
npm install --prefix client
```

```sh
npm start --prefix client
```


## Generating The Database

For generating the database, run the following: 

```console
cd server
```

Then enter the commands to create the `instance` and `migrations` folders and
the database `app.db` file:

```
flask db init
flask db upgrade head
```

python seed.py to fully seed the data. 
