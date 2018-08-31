# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 12:49:38 2018

@author: suvod
"""

import git2repo
import pygit2
import re
import pandas as pd
from datetime import datetime
import re, unicodedata
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE
import os
from utils import utils

class buggy_commit_maker(object):
    
    
    def __init__(self,project_name):
        self.project_name = project_name
        self.data_path = os.getcwd() + '\\data\\'
        self.commit = self.read_files('commit')
        self.committed_files = self.read_files('committed_files')
        
        
    def read_files(self,file_data):
        file_path = self.data_path + self.project_name + '_' + file_data + '.pkl'
        return pd.read_pickle(file_path)
    
    
    def isBuggyCommit(commit):
        res=re.search(r'\b{bug|defect|fix|patch|#}\b',utils().stemming(commit.message),re.IGNORECASE)
        if res is not None:
            return True

    