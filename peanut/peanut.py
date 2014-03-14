#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import config

from reader import Reader
from model import Post, Tag, Category

class Peanut(object):

    def __init__(self):
        self.draft_path = config.path['drafts']

        self.categories = {}
        self.tags = {}
        self.posts = []

        self._reader = Reader()

    def load(self):
       '''Load all drafts''' 

       self
