# py-auth
Authentication service made by Python

## Installation enviroment
## Set up the virtual environemt (Interpreter)
I've simply installed virtual environment in my local project folder using below command

```shell
$ python3 -m venv .venv
```

> Then, you can see `.venv` folder on your project folder, but `.gitignore` won't store that folder in your repository. 

## APIs

* This service can make the sing up for the new user. 
* This service can return the access token (bearer) when the user logs in.
* This service can get the user data after logged in.


| Router |    type    |       API         |     Description       |
|--------|------------|-------------------|-----------------------|
| auth   |    POST    |  '/v1/auth/login` | Login and Create User |
|        |    GET     |  '/v1/auth/user'  | Get User data         |
|        |    POST    |  '/v1/auth/token' | Create token          |

## Built With
* [Fast API](https://fastapi.tiangolo.com/)
* [SqlAlchemy](https://www.sqlalchemy.org/)

## Authors
Allen Kim - Initial work - [coolexplorer](https://github.com/coolexplorer)

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
