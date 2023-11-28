from typing import Mapping

from asshatsuite.settings import AHS_SETTINGS


def get_ahs_setting(key: str):
    settings: Mapping = AHS_SETTINGS.deepcopy()
