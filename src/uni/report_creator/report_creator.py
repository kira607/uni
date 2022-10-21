import argparse
import json

from .config import Config
from .creator import Creator


class ReportCreator:
    def __init__(self):
        pass

    def create_report(self, config: Config):
        Creator(config).run()
