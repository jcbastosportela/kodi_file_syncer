#!/usr/bin/env python
__author__ = "Joao Carlos Bastos Portela"
__copyright__ = "left"
__license__ = "GPL"
__version__ = "0.0.2"
__email__ = "jcbastosportela@gmail.com"

import time
import xbmc
import xbmcgui
import settings
from settings import SettingsIds, Settings
from utils import *
import subprocess
import os


CHECK_PERDIOD = 60 #s

RSYNC_INGORE_LINES = [
    "sending incremental file list",
    "deleting ",
    "sent ",
    "total size is "
]

def _sync_and_clean(remote:str, local:str,delete_remote:bool)->None:
    """Sync remote files

    Args:
        remote (str): Sync from
        local (str): Sync to
        delete_remote (bool): if \c True will remove files from remote path
    """
    try:
        command = ["rsync", "-avz", "--omit-dir-times", "--no-perms", "--no-owner", "--no-group", "--ignore-existing", remote+'/', local+'/']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        # Capture the command's output
        stdout, stderr = process.communicate()

        # Check the return code to see if rsync was successful
        if process.returncode == 0:
            info("Rsync completed successfully.")
            # Parse the output to find synchronized files
            synchronized_files = []
            for line in stdout.splitlines():
                if len([l for l in RSYNC_INGORE_LINES if line.startswith(l)]) > 0:
                    continue
                elif line.strip():
                    info(line.strip())
                    synchronized_files.append(line.strip())

            if synchronized_files:
                dialog = xbmcgui.Dialog()
                dialog.notification('New files synced', ', '.join(synchronized_files), icon='info', time=5000)  # 5000 milliseconds (5 seconds)
            else:
                info("No files synchronized.")
                # delete the files only when nothing was synced, avoid deleting files completed while copying
                if delete_remote:
                    ret = subprocess.run(f'rm -rf {remote}/*', shell=True)
                    info(ret)
        else:
            dialog = xbmcgui.Dialog()
            dialog.notification(f'Failed rsync {process.returncode}', stderr, icon='warning', time=5000)  # 5000 milliseconds (5 seconds)
    except Exception as ex:
        dialog = xbmcgui.Dialog()
        dialog.notification(f'Failed rsync', ex, icon='warning', time=5000)  # 5000 milliseconds (5 seconds)


if __name__ == '__main__':
    monitor = xbmc.Monitor()

    s = settings.load()
    info(f"The server address is {s.MOUNT_POINT}")
    remote_movies_path = os.path.abspath(os.path.join(s.MOUNT_POINT, 'movies/'))
    local_movies_path = os.path.abspath('/media/Portela/movies/')
    remote_series_path = os.path.abspath(os.path.join(s.MOUNT_POINT, 'series/'))
    local_series_path = os.path.abspath('/media/Portela/series/')

    while not monitor.abortRequested():
        info("Going to rsync %s" % time.time())
        _sync_and_clean(remote_movies_path, local_movies_path, s.DELETE_REMOTE)
        _sync_and_clean(remote_series_path, local_series_path, s.DELETE_REMOTE)
        info('Done rsyncing')
        
        # Sleep/wait for abort for CHECK_PERDIOD seconds
        if monitor.waitForAbort(CHECK_PERDIOD):
            # Abort was requested while waiting. We should exit
            break
    info("Leaving")