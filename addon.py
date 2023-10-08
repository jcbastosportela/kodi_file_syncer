#!/usr/bin/env python
__author__ = "Joao Carlos Bastos Portela"
__copyright__ = "left"
__license__ = "GPL"
__version__ = "0.0.2"
__email__ = "jcbastosportela@gmail.com"

import settings
from settings import Settings, SettingsIds
import xbmcaddon
import json
from utils import *
from functools import partial


addon = xbmcaddon.Addon()


def main():
    """Main
    """
    # if no valid password is set, open the settings menu
    if addon.getSettingBool(SettingsIds.FIRST_TIME.name):
        info('First time launch')
        addon.openSettings()
        addon.setSettingBool(SettingsIds.FIRST_TIME.name, False)

    settings.save(Settings(addon.getSettingString(SettingsIds.MOUNT_POINT.name)))


if __name__ == '__main__':
    main()