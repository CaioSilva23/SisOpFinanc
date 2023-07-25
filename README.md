# SisOpFinanc API RESTful - Python

Financial operations system Rest API

### Dependencies

| Dependency        | For what?           | Link  |
| ------------- |:-------------:| -----:|
| tornado | web framework server    |    https://www.tornadoweb.org/ |
| sqlalchemy      | Object-Relational Mapping | https://www.sqlalchemy.org/ |
| jwt      | authenticated | https://jwt.io/ |
| logzero | create application logs   |    https://logzero.readthedocs.io/en/latest/ |

### Routes

* POST - `/api/v1/register` - Register a new user
* POST - `/api/v1/login` - User Login
* PUTCH - `/api/v1/user` - User change password
* GET - `/api/v1/actions` - List of available actions
* POST -`/api/v1/actions` - Create a new action
* GET -`/api/v1/action/{id}` - Detail an action available
* POST -`/api/v1/operations` - Performs share purchase transaction by the user
* POST -`/api/v1/actions/user` - Performs share sale transaction by the user
* GET -`/api/v1/operations` - Lists operations performed by a user
* POST -`/api/v1/actions/user` - List shares purchased from a user
* GET - `/api/v1/operation/{id}` - Details an operation performed by the user

### Architecture

* **Handlers** - It is the layer responsible for manipulating requests and performing business rules.

* **Database** - Layer responsible for data manipulation.
    
* **Util** - Gathers higher-use (repetitive) codes in the project.



### Run
After preparing your environment and your virtualenv, follow the steps:

* `cd projeto-tornado`
* `pip install -r requirements.txt`
*  set the environment variables (examples in file: .env.example) on your machine, or manually change.
* `python main.py`
