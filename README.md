# SisOpFinanc FullStack Application

Financial operations system - FullStack Application

### Dependencies

### backend

| Dependency        | For what?           | Link  |
| ------------- |:-------------:| -----:|
| python |  programming language   |    https://www.python.org/ |
| tornado | web framework server    |    https://www.tornadoweb.org/ |
| postgres |  database  |    https://www.postgresql.org/ |
| sqlalchemy      | Object-Relational Mapping | https://www.sqlalchemy.org/ |
| redis      | caching requests | https://redis.io/ |
| jwt      | authenticated | https://jwt.io/ |
| logzero | create application logs   |    https://logzero.readthedocs.io/en/latest/ |

### frontend

| Dependency        | For what?           | Link  |
| ------------- |:-------------:| -----:|
| javascript |  programming language   |    https://js.org/index.html |
| react js | lib frontend    |    https://react.dev/ |

### DevOps

| Dependency        | For what?           | Link  |
| ------------- |:-------------:| -----:|
| docker |  operating system level virtualization   |   https://www.docker.com/|


### Routes

* POST - `/api/v1/register` - Register a new user
* POST - `/api/v1/login` - User Login
* PUTCH - `/api/v1/change-password` - User change password
* PUTCH - `/api/v1/reset-password` - User reset password
* GET - `/api/v1/user` - User change password
* GET - `/api/v1/actions` - List of available actions
* POST -`/api/v1/actions` - Create a new action
* GET -`/api/v1/action/{id}` - Detail an action available
* POST -`/api/v1/operations` - Performs share purchase transaction by the user
* POST -`/api/v1/actions/user` - Performs share sale transaction by the user
* GET -`/api/v1/operations` - Lists operations performed by a user
* POST -`/api/v1/actions/user` - List shares purchased from a user
* GET - `/api/v1/operation/{id}` - Details an operation performed by the user
* DELETE - `/api/v1/operation/{id}` - Delete an operation performed by the user


### Architecture backend

* **Handlers** - It is the layer responsible for manipulating requests and performing business rules.

* **Database** - Layer responsible for data manipulation.

* **Auth** - Responsible for user authentication.
    
* **Util** - Gathers higher-use (repetitive) codes in the project.



### Run
After preparing your environment and your virtualenv, follow the steps:

Obs: need to have docker and docker compose installed on the machine

* `cd projeto-tornado`
* `docker compose up`
