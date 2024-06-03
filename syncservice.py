#!/usr/bin/env python
__author__ = "Joao Carlos Bastos Portela"
__copyright__ = "left"
__license__ = "GPL"
__version__ = "0.0.4"
__email__ = "jcbastosportela@gmail.com"

import time
import xbmc
import xbmcgui
import settings
from utils import info
import subprocess
import os


CHECK_PERDIOD = 60  # s

RSYNC_INGORE_LINES = [
    "sending incremental file list",
    "deleting ",
    "sent ",
    "total size is "
]


def _sync_and_clean(remote: str, local: str, delete_remote: bool, remote_copied: str|None) -> None:
    """Sync remote files

    Args:
        remote (str): Sync from
        local (str): Sync to
        delete_remote (bool): if \c True will remove files from remote path
        remote_copied (str|None): remote path where to move all copied files 
    """
    try:
        command = ["rsync", "-avz", "--omit-dir-times", "--no-perms",
                   "--no-owner", "--no-group", "--ignore-existing", remote+'/', local+'/']
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

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
                dialog.notification('New files synced', ', '.join(
                    synchronized_files), icon='info', time=5000)
            else:
                info("No files synchronized.")
                # delete the files only when nothing was synced, avoid deleting files completed while copying
                if delete_remote:
                    ret = subprocess.run(f'rm -rf {remote}/*', shell=True)
                    info(ret)
                elif remote_copied:
                    ret = subprocess.run(f'mv {remote}/* {remote_copied}/', shell=True)
                    info(ret)
        else:
            dialog = xbmcgui.Dialog()
            # 5000 milliseconds (5 seconds)
            dialog.notification(
                f'Failed rsync {process.returncode}', stderr, icon='warning', time=5000)
    except Exception as ex:
        dialog = xbmcgui.Dialog()
        # 5000 milliseconds (5 seconds)
        dialog.notification('Failed rsync', ex, icon='warning', time=5000)


if __name__ == '__main__':
    monitor = xbmc.Monitor()

    s = settings.load()
    info(f"The movies source is {s.MOVIES_MOUNT_POINT}")
    remote_movies_path = os.path.abspath(s.MOVIES_MOUNT_POINT)
    remote_copied_movies_path = os.path.abspath(
        os.path.join(s.MOVIES_MOUNT_POINT, '../copied_movies/')) if s.MOVE_REMOTE else None
    local_movies_path = os.path.abspath(s.MOVIES_DEST)

    info(f"The series source is {s.MOVIES_MOUNT_POINT}")
    remote_series_path = os.path.abspath(s.SERIES_MOUNT_POINT)
    remote_copied_series_path = os.path.abspath(
        os.path.join(s.SERIES_MOUNT_POINT, '../copied_series/')) if s.MOVE_REMOTE else None
    local_series_path = os.path.abspath(s.SERIES_DEST)

    while not monitor.abortRequested():
        info("Going to rsync %s" % time.time())
        _sync_and_clean(remote_movies_path, local_movies_path, s.DELETE_REMOTE, remote_copied_movies_path)
        _sync_and_clean(remote_series_path, local_series_path, s.DELETE_REMOTE, remote_copied_series_path)
        info('Done rsyncing')

        # Sleep/wait for abort for CHECK_PERDIOD seconds
        if monitor.waitForAbort(CHECK_PERDIOD):
            # Abort was requested while waiting. We should exit
            break
    info("Leaving")
