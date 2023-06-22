# echo_service
This project was generated using [fastapi_template](https://github.com/s3rius/FastAPI-template)
## Access to the service
The service is available on AWS cloud by the link:
```commandline
http://13.48.42.153:8000/api/docs
```
Feel free to try Endpoints

<details>
  <summary><span style="font-size: 25px; font-weight: bold;">Task definition</span></summary>

In this challenge you will implement an API service called _Echo_. The purpose of Echo is to serve ephemeral/mock endpoints created with parameters specified by clients.

**Your task is to design and implement the Echo service in Python 3 according to the [following technical specification](#technical-specification), and implement the infrastructure for deploying the service on AWS Cloud using Terraform**.

### Technical specification

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

The Echo service works as follows:

* The server MUST implement `GET /endpoints` endpoint to return a list of mock endpoints created by clients (using `POST /endpoints` endpoint) or an empty array if no mock endpoints are defined yet.
  * The server MUST implement `POST /endpoints` endpoint to create a mock endpoint according to data from the payload. The server SHOULD validate received data.
  * The server MUST implement `PATCH /endpoints{/:id}` endpoint to updates the existing mock endpoint according to data from the payload. The server SHOULD NOT accept invalid data or update non-existing mock endpoints. If requested mock endpoint doesn't exist, the server MUST respond with `404 Not found`.
  * The server MUST implement `DELETE /endpoints{/:id}` endpoint to delete the requested mock endpoint. If requested mock endpoint doesn't exist, the server MUST respond with `404 Not found`.
  * The server MUST serve all mock endpoints as defined by clients. Mock endpoints MUST be available over HTTP. Example: if there is a mock endpoint `POST /foo/bar/baz`, it MUST be available only for `POST` requests at `/foo/bar/baz` path. It SHALL NOT be available via `GET /foo/bar/baz` or even `POST /foo/bar` because these are different endpoints. Basically Echo works like "what you define is what you get".
  * It's RECOMMENDED to validate incoming requests as might contain invalid data.
  * The server MAY implement authentication for `/endpoints`.
  * You MAY implement additional functionality if you have time or will to show your skills.

The server operates on _Endpoint_ entities:

    Endpoint {
      id    String
      verb  String
      path  String

      response {
        code    Integer
        headers Hash<String, String>
        body    String
      }
    }

  * `id` (required), a string value that uniquely identifies an Endpoint
    * `verb` (required), a string value that may take one of HTTP method names. See [RFC 7231](https://tools.ietf.org/html/rfc7231#section-4.3)
    * `path` (required), a string value of the path part of URL
    * `response` (required), an object with following attributes:
      * `code` (required), an integer status code returned by Endpoint
      * `headers` (optional), a key-value structure where keys represent HTTP header
      names and values hold actual values of these headers returned by Endpoint
      * `body` (optional), a string representation of response body returned by
      Endpoint

You MAY use [JSON:API v1.0](https://jsonapi.org/) as a format to pass the data to the `/endpoints` endpoint. If you decide to go with a format different to JSON:API v1.0, make sure to document that and the reasoning behind your choice.

Furthermore you are free to extend the list of attributes if your implementation requires that. The list above represents what the entity should have as minimum.


### Examples

<details>
  <summary>List endpoints</summary>
  <markdown>

#### Request

    GET /endpoints HTTP/1.1
    Accept: application/vnd.api+json

#### Expected response

    HTTP/1.1 200 OK
    Content-Type: application/vnd.api+json

    {
        "data": [
            {
                "type": "endpoints",
                "id": "12345",
                "attributes": [
                    "verb": "GET",
                    "path": "/greeting",
                    "response": {
                      "code": 200,
                      "headers": {},
                      "body": "\"{ \"message\": \"Hello, world\" }\""
                    }
                ]
            }
        ]
    }
  </markdown>
</details>

<details>
  <summary>Create endpoint</summary>
  <markdown>

#### Request

    POST /endpoints HTTP/1.1
    Content-Type: application/vnd.api+json
    Accept: application/vnd.api+json

    {
        "data": {
            "type": "endpoints",
            "attributes": {
                "verb": "GET",
                "path": "/greeting",
                "response": {
                  "code": 200,
                  "headers": {},
                  "body": "\"{ \"message\": \"Hello, world\" }\""
                }
            }
        }
    }

#### Expected response

    HTTP/1.1 201 Created
    Location: http://example.com/greeting
    Content-Type: application/vnd.api+json

    {
        "data": {
            "type": "endpoints",
            "id": "12345",
            "attributes": {
                "verb": "GET",
                "path": "/greeting",
                "response": {
                  "code": 200,
                  "headers": {},
                  "body": "\"{ \"message\": \"Hello, world\" }\""
                }
            }
        }
    }
  </markdown>
</details>

<details>
  <summary>Update endpoint</summary>
  <markdown>

#### Request

    PATCH /endpoints/12345 HTTP/1.1
    Content-Type: application/vnd.api+json
    Accept: application/vnd.api+json

    {
        "data": {
            "type": "endpoints",
            "id": "12345"
            "attributes": {
                "verb": "POST",
                "path": "/greeting",
                "response": {
                  "code": 201,
                  "headers": {},
                  "body": "\"{ \"message\": \"Hello, everyone\" }\""
                }
            }
        }
    }

#### Expected response

    HTTP/1.1 200 OK
    Content-Type: application/vnd.api+json

    {
        "data": {
            "type": "endpoints",
            "id": "12345",
            "attributes": {
                "verb": "POST",
                "path": "/greeting",
                "response": {
                  "code": 201,
                  "headers": {},
                  "body": "\"{ \"message\": \"Hello, everyone\" }\""
                }
            }
        }
    }
  </markdown>
</details>

<details>
  <summary>Delete endpoint</summary>
  <markdown>

#### Request

    DELETE /endpoints/12345 HTTP/1.1
    Accept: application/vnd.api+json

#### Expected response

    HTTP/1.1 204 No Content
  </markdown>
</details>

<details>
  <summary>Error response</summary>
  <markdown>

In case client makes unexpected response or server encountered an internal problem, Echo should provide proper error response.

#### Request

    DELETE /endpoints/1234567890 HTTP/1.1
    Accept: application/vnd.api+json

#### Expected response

    HTTP/1.1 404 Not found
    Content-Type: application/vnd.api+json

    {
        "errors": [
            {
                "code": "not_found",
                "detail": "Requested Endpoint with ID `1234567890` does not exist"
            }
        ]
    }
  </markdown>
</details>

<details>
  <summary>Sample scenario</summary>
  <markdown>

#### 1. Client requests non-existing path

    > GET /hello HTTP/1.1
    > Accept: application/vnd.api+json

    HTTP/1.1 404 Not found
    Content-Type: application/vnd.api+json

    {
        "errors": [
            {
                "code": "not_found",
                "detail": "Requested page `/hello` does not exist"
            }
        ]
    }

#### 2. Client creates an endpoint

    > POST /endpoints HTTP/1.1
    > Content-Type: application/vnd.api+json
    > Accept: application/vnd.api+json
    >
    > {
    >     "data": {
    >         "type": "endpoints",
    >         "attributes": {
    >             "verb": "GET",
    >             "path": "/hello",
    >             "response": {
    >                 "code": 200,
    >                 "headers": {
    >                     "Content-Type": "application/json"
    >                 },
    >                 "body": "\"{ \"message\": \"Hello, world\" }\""
    >             }
    >         }
    >     }
    > }

    HTTP/1.1 201 Created
    Location: http://example.com/hello
    Content-Type: application/vnd.api+json

    {
        "data": {
            "type": "endpoints",
            "id": "12345",
            "attributes": {
                "verb": "GET",
                "path": "/hello",
                "response": {
                    "code": 200,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": "\"{ \"message\": \"Hello, world\" }\""
                }
            }
        }
    }

#### 3. Client requests the recently created endpoint

    > GET /hello HTTP/1.1
    > Accept: application/json

    HTTP/1.1 200 OK
    Content-Type: application/json

    { "message": "Hello, world" }

#### 4. Client requests the endpoint on the same path, but with different HTTP verb

The server responds with HTTP 404 because only `GET /hello` endpoint is defined.

NOTE: if you could imagine different behavior from the server, feel free to propose it in your solution.

    > POST /hello HTTP/1.1
    > Accept: application/vnd.api+json

    HTTP/1.1 404 Not found
    Content-Type: application/vnd.api+json

    {
        "errors": [
            {
                "code": "not_found",
                "detail": "Requested page `/hello` does not exist"
            }
        ]
    }

  </markdown>
</details>

</details>

<details>
  <summary><span style="font-size: 25px; font-weight: bold;">Installation</span></summary>

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m echo_service
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: https://python-poetry.org/

## Docker

You can start the project with docker using this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

If you want to develop in docker with autoreload add `-f deploy/docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . build
```

## Project structure

```bash
$ tree "echo_service"
echo_service
├── conftest.py  # Fixtures for all tests.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

All environment variables should start with "ECHO_SERVICE_" prefix.

For example if you see in your "echo_service/settings.py" a variable named like
`random_parameter`, you should provide the "ECHO_SERVICE_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `echo_service.settings.Settings.Config`.

An example of .env file:
```bash
ECHO_SERVICE_RELOAD="True"
ECHO_SERVICE_PORT="8000"
ECHO_SERVICE_ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:
* black (formats your code);
* mypy (validates types);
* isort (sorts imports in all files);
* flake8 (spots possible bugs);


You can read more about pre-commit here: https://pre-commit.com/


## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . run --build --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . down
```

For running tests on your local machine.


2. Run the pytest.
```bash
pytest -vv .
```

</details>
