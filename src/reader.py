#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import markdown

from datetime import datetime

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
        #Init markdown paraser with some extensions.
        self.md = markdown.Markdown(extensions=['fenced_code',  #Fenced Code Blocks
                                                'codehilite',   #CodeHilite
                                                'meta',         #Meta-Data
                                                'footnotes',    #Footnotes
                                                'tables',       #Tables
                                                'smart_strong', #Smart Strong
                                                'nl2br'],       #New Line to Break
                                    extension_configs={'codehilite': [('guess_lang', False)]})
 
    # Meta data handlers
    # title: Hello world
    # date: 2014-3-10
    # tag: test
    # top: no
    # publish: yes

    _meta_handlers = {
        'tag':      lambda x: x if x else [],
        'title':    lambda x: x[0] if x else '',
        'date':     lambda x: datetime.strptime(x[0], '%Y-%m-%d') if x else datetime.now(),
        'top':      lambda x: True if x and x[0]=='yes' else False,
        'publish':  lambda x: False if x and x[0]=='no' else True,
    }

    def _parse_metadata(self, meta):
        res = {}
        for name, handler in self._meta_handlers.items():
            value = handler(meta.get(name, None))
            res[name] = value

        return res

    def _get_slug(self, file_name):
        m = self.file_name_regex.search(file_name)
        if not m:
            return None
        return m.group(1)

    def read(self, file_name):
        '''Read markdown file.'''

        slug = self._get_slug(file_name)

        if not slug:
            print('No slug')
            return None

        with open(file_name, 'r') as f:
            content = f.read().decode('utf-8')
            html = self.md.reset().convert(content.strip(' \n'))
            if not self.md.Meta:
                #Meta must not be empty
                print('No meta')
                return None

            result = self._parse_metadata(self.md.Meta)
            
            result['content'] = html
            result['slug'] = slug
            return result
