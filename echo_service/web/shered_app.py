from fastapi import FastAPI


class SharedApp:
    _app: FastAPI

    def save(self, app: FastAPI) -> None:
        self._app = app

    def extract(self) -> FastAPI:
        return self._app


shared_app = SharedApp()
