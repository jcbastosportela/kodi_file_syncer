import xbmc
import xbmcaddon

_addon = xbmcaddon.Addon()
_addonname = _addon.getAddonInfo('name')


def info(msg):
    xbmc.log(f'{_addonname} - {msg}', level=xbmc.LOGINFO)


def debug(msg):
    xbmc.log(f'{_addonname} - {msg}', level=xbmc.LOGDEBUG)


def error(msg):
    xbmc.log(f'{_addonname} - {msg}', level=xbmc.LOGERROR)


def warn(msg):
    xbmc.log(f'{_addonname} - {msg}', level=xbmc.LOGWARNING)
