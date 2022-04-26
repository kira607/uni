import sys

from .apps import UniApp


def main() -> int:
    app = UniApp()
    return app.run()


if __name__ == '__main__':
    sys.exit(main())