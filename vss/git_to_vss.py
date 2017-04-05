# -*- coding: utf-8 -*-
import os
import stat
import shutil
import argparse
import git
import vss


class GitToVss:

    def __init__(self, SS_PATH, SS_DIR, GIT_ROOT, VSS_ROOT, VSS_WORKSPACE_ROOT, USER, PWD):
        self.SS_PATH = SS_PATH
        self.SS_DIR = SS_DIR
        self.GIT_ROOT = GIT_ROOT
        self.VSS_ROOT = VSS_ROOT
        self.VSS_WORKSPACE_ROOT = VSS_WORKSPACE_ROOT
        self.USER = USER
        self.PWD = PWD

    def setup_env(self):
        os.putenv("SSUSER", self.USER)
        os.putenv("SSPWD", self.PWD)
        os.environ['SSUSER'] = self.USER
        os.environ['SSPWD'] = self.PWD

    def full(self):
        repo = git.Repo(GIT_ROOT)
        headtree = repo.head.commit.tree

        # 先建立文件夹，然后再提交文件
        for entry in headtree.traverse():
            if entry.type == 'tree':
                print(entry.path)
                if vss.exists(SS_DIR, os.path.join(VSS_ROOT, entry.path), SS_PATH):
                    pass
                else:
                    vss.mkdir(SS_DIR, os.path.join(VSS_ROOT, entry.path), SS_PATH)

        for entry in headtree.traverse():
            if entry.type == 'blob':
                print(entry.path)
                if vss.exists(SS_DIR, os.path.join(VSS_ROOT, entry.path), SS_PATH):
                    vss_item_path = os.path.join(VSS_ROOT, entry.path)
                    local_dir = os.path.join(VSS_WORKSPACE_ROOT, os.path.dirname(entry.path))
                    vss.checkout(SS_DIR, vss_item_path, local_dir, SS_PATH)
                    self.copy_one_file(entry.path)
                    vss.checkin(SS_DIR, vss_item_path, local_dir, SS_PATH)
                else:
                    vss_dir = os.path.join(VSS_ROOT, os.path.dirname(entry.path))
                    vss.add(SS_DIR, vss_dir, os.path.join(VSS_WORKSPACE_ROOT, entry.path), SS_PATH)

    def incr(self):
        repo = git.Repo(GIT_ROOT)
        headcommit = repo.head.commit

        file_diff = headcommit.diff('HEAD~1')

        for adiff in file_diff.iter_change_type('A'):  # add
            print("add " + adiff.a_path)
            vss_dir = os.path.join(VSS_ROOT, os.path.dirname(adiff.a_path))
            self.copy_one_file(adiff.a_path)
            vss.add(SS_DIR, vss_dir, os.path.join(VSS_WORKSPACE_ROOT, adiff.path), SS_PATH)

        for adiff in file_diff.iter_change_type('D'):  # delete
            print("delete " + adiff.a_path)
            vss_item_path = os.path.join(VSS_ROOT, adiff.a_path)
            self.delete_on_file(adiff.a_path)
            vss.delete(SS_DIR, vss_item_path, SS_PATH)

        for adiff in file_diff.iter_change_type('R'):  # rename
            print("rename " + adiff.a_path)
            vss_rename_from = os.path.join(VSS_ROOT, adiff.rename_from)
            vss_rename_to = os.path.join(VSS_ROOT, adiff.rename_to)
            vss.rename(SS_DIR, vss_rename_from, vss_rename_to, SS_PATH)

        for adiff in file_diff.iter_change_type('M'):  # modify
            print("modify " + adiff.a_path)
            vss_item_path = os.path.join(VSS_ROOT, adiff.a_path)
            local_dir = os.path.join(VSS_WORKSPACE_ROOT, os.path.dirname(adiff.a_path))
            vss.checkout(SS_DIR, vss_item_path, local_dir, SS_PATH)
            self.copy_one_file(adiff.a_path)
            vss.checkin(SS_DIR, vss_item_path, local_dir, SS_PATH)

    def copy_one_file(self, path):
        source_path = os.path.join(GIT_ROOT, path)
        target_path = os.path.join(VSS_WORKSPACE_ROOT, path)

        if os.path.exists(target_path):
            if not os.access(target_path, os.W_OK):  # 如果不可写, 清除只读属性
                os.chmod(target_path, stat.S_IWRITE)
            shutil.copy2(source_path, target_path)
        else:
            shutil.copy2(source_path, target_path)

    def delete_on_file(self, path):
        target_path = os.path.join(VSS_WORKSPACE_ROOT, path)
        if os.path.isdir(target_path):
            os.rmdir(target_path)
        else:
            os.remove(target_path)

if __name__ == '__main__':
    """
    example:
    python git_to_vss.py -s "C:\Program Files (x86)\Microsoft Visual SourceSafe\ss.exe" -d "E:\tmp\test_vss" -g "E:\worksapce\Project1" -v "$/test0" -w "E:\tmp\vss_workspace\Project1" -u "user" -p "pass"
    
   """
    parser = argparse.ArgumentParser(description='git sync to vss tool')
    parser.add_argument('-s', '--ss_path', required=True, help='path of ss.exe')
    parser.add_argument('-d', '--ss_dir', required=True, help='vss database path')
    parser.add_argument('-g', '--git_root', required=True, help='git repository root')
    parser.add_argument('-v', '--vss_root', required=True, help='vss parent project path')
    parser.add_argument('-w', '--vss_workspace_root', required=True, help='local work copy of vss')
    parser.add_argument('-u', '--user', required=True, help='username to login vss')
    parser.add_argument('-p', '--password', required=True, help='password to login vss')
    parser.add_argument('-m', '--mode', choices=['full', 'incr'], default='full', help='full or incr')

    args = parser.parse_args()

    SS_PATH = args.ss_path
    SS_DIR = args.ss_dir
    GIT_ROOT = args.git_root
    VSS_ROOT = args.vss_root
    VSS_WORKSPACE_ROOT = args.vss_workspace_root
    USER = args.user
    PWD = args.password
    MODE = args.mode

    print("SS_PATH: "+SS_PATH)
    print("SS_DIR: " + SS_DIR)
    print("GIT_ROOT: " + GIT_ROOT)
    print("VSS_ROOT: " + VSS_ROOT)
    print("VSS_WORKSPACE_ROOT: " + VSS_WORKSPACE_ROOT)
    print("USER: " + USER)
    print("PWD: " + PWD)
    print("MODE: " + MODE)

    gts = GitToVss(SS_PATH, SS_DIR, GIT_ROOT, VSS_ROOT, VSS_WORKSPACE_ROOT, USER, PWD)
    gts.setup_env()

    if MODE == 'full':
        gts.full()
    else:
        gts.incr()

