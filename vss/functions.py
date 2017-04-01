"""
A set of high-level functions to ease the use of Microsoft Visual SourceSafe.
"""
import os
from .vss_wrapper import VSS

def checkout(repository_path, vss_project_path, local_path, ss_path=None):
    """
    Check out a VSS project to the specified local directory.

    Return the standard output.
    """

    vss = VSS(repository_path, ss_path)

    return vss.checkout(vss_project_path, recursive=True, get_folder=local_path, output='error')

def undo_checkout(repository_path, vss_project_path, local_path, ss_path=None):
    """
    Undo a checkout of a VSS project to the specified local directory.

    Return the standard output.
    """

    vss = VSS(repository_path, ss_path)

    return vss.undo_checkout(vss_project_path, recursive=True, get_folder=local_path, output='error')

def checkin(repository_path, vss_project_path, local_path, ss_path=None):
    """
    Check in a VSS project from the specified local directory.

    Return the standard output.
    """

    vss = VSS(repository_path, ss_path)

    return vss.checkin(vss_project_path, recursive=True, get_folder=local_path, output='error', comment_no_text=True)

def get(repository_path, vss_project_path, local_path, ss_path=None):
    """
    Get a read-only copy of a VSS project into the specified local directory.

    Return the standard output.
    """

    vss = VSS(repository_path, ss_path)

    return vss.get(vss_project_path, recursive=True, get_folder=local_path, output='error', ignore='all')

def delete(repository_path, vss_project_path, ss_path=None):
    """
    delete file

    Return the standard output.
    """

    vss = VSS(repository_path, ss_path)

    return vss.delete(vss_project_path, output='error', ignore='all')

def add(repository_path, vss_project_path, local_path, ss_path=None):
    """
    add file
    vss_project_path(to the deepest folder)
    Return the standard output.
    """

    vss = VSS(repository_path, ss_path)

    vss.set_current_project(vss_project_path)

    return vss.add(local_path, recursive=True, output='error', ignore='all')

def exists(repository_path, vss_project_path, ss_path=None):
    """
    exists for True

    Return the standard output.
    """
    vss = VSS(repository_path, ss_path)

    return 0 == vss.properties(vss_project_path)

def mkdir(repository_path, vss_project_path, ss_path=None):
    """
    make dir
    """
    vss = VSS(repository_path, ss_path)
    return vss.create(vss_project_path, output='error', ignore='all')

def rename(repository_path, vss_project_path, vss_project_new_path, ss_path=None):
    """ rename a item """
    vss = VSS(repository_path, ss_path)
    return vss.rename(vss_project_path, vss_project_new_path, output='error', ignore='all')

