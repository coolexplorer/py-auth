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
| Router |    type    |       API         |     Description       |
|--------|------------|-------------------|-----------------------|
| auth   |    POST    |  '/v1/auth/login` | Login and Create User |
|        |    GET     |  '/v1/auth/user'  | Get User data         |
|        |    POST    |  '/v1/auth/token' | Create token          |

