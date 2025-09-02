#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entry point for the STATCAN Sources Metadata Grabber.

This module runs the main export function from core.funcs.

Created on Thu Aug  5 21:59:20 2021

@author: Alexander Mikhailov
"""

from .core.funcs import export_statcan_data
from .utils.filenames import get_default_filename

if __name__ == '__main__':
    export_statcan_data(get_default_filename())
