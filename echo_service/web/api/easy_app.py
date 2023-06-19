from fastapi import FastAPI

easy_app: FastAPI


def create_easy_app(app: FastAPI) -> None:
    global easy_app
    easy_app = app


def get_easy_app() -> FastAPI:
    global easy_app
    return easy_app
