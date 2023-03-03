# Flask Starter Template
This is a starter template for a Flask Python backend that is ready for use in development and production environments with minimal to no configuration.
## Getting Started
You will need to set up a database for this web server template. Ideally, PostgreSQL or MySQL and not SQLite. You will need to have PostgreSQL/MySQL installed in order to install and run the matching Python libraries and instantiate a `db` connection.

1. Install a RDBMS
2. Create a database
3. Install [gunicorn](https://gunicorn.org/) (G-Unit Unicorn web server by 50 Cent)
4. Install dependencies
5. Start the server with `gunicorn app:app` (If you are using WebSockets, you must run your server using `flask run --port=PORT --debugger`)

**Install your dependencies**

Remember `npm install` from Zoom lecture? No? Well yeah, that was a thing!

`$ pip install -r requirements.txt`

## Gunicorn

**Current setup**

To start the server right after cloning this template run:

`$ gunicorn app:app`

You could also run `flask run --port=PORT` but this will not leverage the WSGI web server. At this time, you will have to use the `flask run` command in order to leverage WebSockets in your project.

**Customization**

`gunicorn [WSGI_APP] [OPTIONS]`

Where WSGI_APP is of the pattern `$(MODULE_NAME):$(VARIABLE_NAME)`. You can also do things like bind the host or set a custom port in case you're using the default (3000).

### Connecting a Database

#### 📃 SQLite
Oh you don't care about deploying your project? Right this way 👇

In `config.py` set the value of `SQLALCHEMY_DATABASE_URI` to be `sqlite:///development.sqlite3`. Then create a file in the root of the project called `development.sqlite3`. From here, you can call `flask db init` to get started. If anyone wants to use your application, you need to give them your physical address so that they can come to your house and use your computer on localhost 🏠

#### 🐘 PostgreSQL
Install PostgreSQL on Mac by running `brew install postgresql` (Linux instructions coming soon). When that finishes, you should be able to run `psql postgres` in your terminal. From here, you should create a database. I usually create a separate user within PostgreSQL and make the user the owner of that database, although it doesn't matter too _too_ much when you're running this on a machine only you have access to anyway.

```
CREATE DATABASE [database_name];
ALTER DATABASE [database_name] OWNER TO [username]
```

You can then quit the psql shell by typing `\q`. Now set the value of `SQLALCHEMY_DATABASE_URI` to be `postgresql://[user]:[password]@localhost/[database_name]`. For example, if my username was `mikegpt` and my password was `burntheboats` and the name of the database I created above was flask_python_development, the value of my database URI would be: 

`postgresql://mikegpt:burntheboats@localhost/flask_python_development`

You can now run `flask db init` and get started and you will be able to deploy your application more easily to platforms like Heroku, Render, or Fly.

#### [Flask Migrate commands](https://flask-migrate.readthedocs.io/en/latest/)
These are the commands you'll be using the most often as you develop. I recommend you verify that your database is in the exact state you expect it to be after every step with SQL until you're reasonably certain about what's happening. Then you can move to every other step. Maybe.

```
flask db --help
flask db init
flask db current
flask db upgrade
flask db downgrade
```

## Database Workflow
1. Make a change to the Model (example: add a new column/attribute)
2. Run `flask db migrate` to create a migration for this change
3. Run `flask db upgrade` to apply the change to the database
4. Made a mistake? Run `flask db downgrade` to reverse it
## App structure


## SQLAlchemy Query Interface

### Legacy vs Modern
In order to make developers write more code, SQLAlchemy switched from a style that works like OOP to a style that works more like writing raw SQL in Python. Writing more code provides you more flexibility and control over the query regardless of whether or not you need either of those things.


Here is a list of useful methods in SQLAlchemy for interacting with the database:

```python
# Return a single record
Model.query.get(primary_key)
Model.query.get_or_404(primary_key)

# Returns all records in the table for this model
Model.query.all()

# Return all records that match the filter
Model.query.filter_by(user_id=user.id)

# Return the first record for this Model
Model.query.first()
Model.query.first_or_404()

# Returns n number of records from the Model table
Model.query.limit(n)

# Count the number of records in a table. Returns an integer
Model.query.count()

# Return a list of records ordered by a column name as a string
Model.query.order_by('column')
Model.query.paginate()

# Update a single record in a table
m = Model.query.get(id)
m.email = new_email
db.session.commit()

# Update all records in this table simulatneously by using a dictionary object
Model.query.update(dict)

# Delete a record
m = Model.query.get(id)
db.session.delete()
db.session.commit()
```

### Authentication
This template is currently using a simple JWT auth implementation + a custom route decorator to manage sessions. It's not recommended for production use as is.