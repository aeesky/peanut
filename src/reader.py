#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import markdown

from datetime import datetime

ALL_METAS = ['title', 'date', 'tags', 'publish', 'top']

class Reader(object):
    '''Abstract class for all readers

    Attribute:
        file_extensions: List, all supporting file types.
    '''

    file_extensions = ''

    def read(self, file_path):
        '''Read draft from path

        Args:
            file_path: String, file path.
        '''

        raise NotImplementedError

class MarkdownReader(object):
    '''Markdown reader'''

    file_extensions = ['md', 'markdown']

    file_name_regex = re.compile(r'([^/]+)\.(md|markdown)')

    def __init__(self):
        '''Init markdown paraser with some extensions.'''

        extensions = ['fenced_code',  # Fenced Code Blocks
                      'codehilite',   # CodeHilite
                      'meta',         # Meta-Data
                      'footnotes',    # Footnotes
                      'tables',       # Tables
                      'smart_strong', # Smart Strong
                      'nl2br',        # New Line to Break
                      ]

        # Do not guess language
        extension_configs = {'codehilite': [('guess_lang', False)]}

        self.md = markdown.Markdown(extensions=extensions,
                                    extension_configs=extension_configs)
 
    _meta_handlers = [lambda x: x[0] if x else '', #title
                      lambda x: datetime.strptime(x[0], '%Y-%m-%d') if x else datetime.now(), #date
                      lambda x: x[0].split(',') if x else [], #tag 
                      lambda x: False if x and x[0]=='no' else True, #publish defaults to True
                      lambda x: True if x and x[0]=='yes' else False, #top defaults to False
                      ]

    def _parse_metadata(self, meta):
        '''Parse meta data from markdown meta.

        title: Hello world
        date: 2014-3-10
        tags: hello, world
        publish: yes
        top: no
        '''

        res = {}
        handlers = dict(zip(ALL_METAS, self._meta_handlers))
        for name, handler in handlers.items():
            value = handler(meta.get(name, None))
            res[name] = value

        return res

    def _parse_slug(self, file_name):
        '''parse slug from file name'''

        m = self.file_name_regex.search(file_name)
        if not m:
            return None
        return m.group(1)

    def read(self, file_name):
        '''Read markdown file.'''

        slug = self._parse_slug(file_name)
        draft = {}

        with open(file_name, 'r') as f:
            content = f.read().decode('utf-8')
            html = self.md.reset().convert(content.strip(' \n'))
            if self.md.Meta:
                draft = self._parse_metadata(self.md.Meta)
            
            draft['content'] = html
            draft['slug'] = slug
            return draft
