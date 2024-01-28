#!/usr/bin/env python
__author__ = "Joao Carlos Bastos Portela"
__copyright__ = "left"
__license__ = "GPL"
__version__ = "0.0.2"
__email__ = "jcbastosportela@gmail.com"

from settings import SettingsIds
import xbmcaddon
from utils import info


addon = xbmcaddon.Addon()


def main():
    """Main
    """
    # if no valid password is set, open the settings menu
    if addon.getSettingBool(SettingsIds.FIRST_TIME.name):
        info('First time launch')
        addon.openSettings()
        addon.setSettingBool(SettingsIds.FIRST_TIME.name, False)
        addon.setSettingBool(SettingsIds.MOVE_REMOTE.name, True)


if __name__ == '__main__':
    main()
