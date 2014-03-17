#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os 
from mako.template import Template
from mako.lookup import TemplateLookup

class Theme(object):

    def __init__(self, theme_name='default'):
        '''Mako template wrapper

        @param theme_name: theme name, defaults ot "default"
        '''

        self.theme_name = theme_name

        theme_path = self.get_template_path(theme_name)
        if not os.path.isdir(theme_path):
            raise NameError('Theme {} not found'.format(theme_name))

        self.templates = TemplateLookup(directories=[theme_path], 
                                        input_encoding='utf-8', 
                                        output_encoding='utf-8', 
                                        encoding_errors='replace')

    def get_template_path(self, theme):
        '''Get template path

        @param theme: theme name, defaults to "default"
        '''

        base_path = os.path.split(os.path.realpath(__file__))[0]
        return os.path.join(base_path, 'templates', theme)

    def template(self, layout):
        '''Get template, return None if not found.

        @param layout: layout name
        '''

        temp_file = layout+'.html'

        try:
            return self.templates.get_template(temp_file)
        except:
            return None
