#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import config

import blog

def main():
    my_blog = blog.Blog()
    my_blog.load()
    my_blog.generate()
