from .cli import UniCliApp


def run_cli() -> int:
    app = UniCliApp()
    return app.run()
