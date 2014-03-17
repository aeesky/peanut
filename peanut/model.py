#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import config

from datetime import datetime

class BaseModel(object):
    required_metas = ('title', 'slug')
    optional_metas = {'layout'}

    def __init__(self, **metas):
        #check required metas
        for m in self.required_metas:
            if m not in metas:
                raise NameError('Meta: {} not found'.format(m))

        for m in self.required_metas:
            setattr(self, m, metas.get(m))

        for m in self.optional_metas:
            value = metas.get(m) or self.optional_metas[m]
            setattr(self, m, value)

    @property
    def url(self):
        '''url'''
        base = config.url.get(self.layout)
        if not base:
            raise KeyError('Layout: {} not found'.format(self.layout))

        return base.format(slug=self.slug)

    @property
    def dst_path(self):
        '''destination file path'''

        html_path = config.path['html']
        base = os.path.join(html_path, config.path.get(self.layout))
        if not base:
            raise KeyError('Layout: {} not found'.format(self.layout))

        return os.path.join(base, self.slug+'.html')

class Post(BaseModel):
    '''Post'''

    optional_metas = {
        'content': '',
        'date': datetime.now(),
        'publish': True,
        'top': False,
        'tags': [],
        'category': None,
        'layout': 'post',
    }

class Tag(BaseModel):
    '''Tag'''

    optional_metas = {
        'layout': 'tag',
    }

    def __init__(self, title):
        super(Tag, self).__init__(title=title, slug=title)

    def __eq__(self, other):
        return self.title == other.title

    def __hash__(self):
        return self.title.__hash__()

class Category(Tag):
    '''Category'''

    optional_metas = {
        'layout': 'category',
    }

    layout = 'category'

class Static(BaseModel):
    '''Static'''

    def __init__(self, layout, **metas):
        super(Static, self).__init__(layout=layout, **metas)
