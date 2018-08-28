# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 15:39:01 2018

@author: suvod
"""

from pygit2 import clone_repository
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE,GIT_MERGE_ANALYSIS_UP_TO_DATE,GIT_MERGE_ANALYSIS_FASTFORWARD,GIT_MERGE_ANALYSIS_NORMAL,GIT_RESET_HARD
from pygit2 import Repository
import shutil,os
from os import listdir
from os.path import isfile, join
from datetime import datetime


class git2repo(object):
    
    def __init__(self,repo_url,repo_name):
        self.repo_url = repo_url
        self.repo_name = repo_name
        self.repo_path = os.getcwd() + '\\temp_repo\\' + repo_name
        
        
    def clone_repo(self):
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
        self.repo = clone_repository(self.repo_url, self.repo_path)
        return self.repo
    
    
    def repo_remove(self):
        self.repo.free()
        deldir = self.repo_path + '\\.git\\objects\\pack'
        delFiles = [f for f in listdir(deldir) if isfile(join(deldir, f))]
        for i in delFiles:
            file_name = deldir + '\\' + i
            os.chmod(file_name, 0o777)
        if os.path.exists(self.repo_path):
            shutil.rmtree(self.repo_path,ignore_errors=True)
            
        
    def get_commits(self):
        commits = []
        for commit in self.repo.walk(self.repo.head.target, GIT_SORT_TOPOLOGICAL | GIT_SORT_REVERSE):
            commits.append(commit)
        return commits
    
    def get_committed_files(self):
        committed_files = []
        commits = self.get_commits()
        for i in range(len(commits)-1):
            t0 = commits[i]
            t1 = commits[i+1]
            _diff = self.repo.diff(t0,t1)
            for j in _diff.deltas:
                committed_files.append([commits[i].id,j.new_file.id, j.new_file.mode,j.new_file.path])
        return committed_files
    
    def get_diffs(self,commits):
        diffs = []
        for i in range(len(commits)-1):
            t0 = commits[i]
            if i != 0:
                t1 = commits[i].parents[0]
            else:
                continue
            _diff = self.repo.diff(t0,t1)
            for diff_i in _diff.__iter__():
                file_path = diff_i.delta.new_file.path
                old_lineno = []
                new_lineno = []
                for x in diff_i.hunks:
                    for y in x.lines:
                        old_lineno.append(y.old_lineno)
                        new_lineno.append(y.new_lineno)
                diffs.append([commits[i].id,file_path,old_lineno,new_lineno])
        return diffs
    
    def get_blame(self,file_path):
        return self.repo.blame(file_path,flags = 'GIT-BLAME_TRACK_COPIES_ANY_COMMIT_COPIES')
        