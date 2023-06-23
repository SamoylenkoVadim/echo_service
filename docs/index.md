#  Documentation
The purpose of Echo is to serve ephemeral/mock endpoints created with parameters specified by clients.

This project was generated using [fastapi_template](https://github.com/s3rius/FastAPI-template)
## Access to the service
The service is available on AWS cloud by the link: [http://13.48.42.153:8000/api/docs](http://13.48.42.153:8000/api/docs)

Feel free to try endpoints.

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
