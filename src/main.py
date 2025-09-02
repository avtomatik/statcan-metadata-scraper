#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entry point for the STATCAN Sources Metadata Grabber.

This module runs the main export function from core.funcs.

Created on Thu Aug  5 21:59:20 2021

@author: Alexander Mikhailov
"""

from .core.pipeline import run_pipeline

if __name__ == '__main__':
    run_pipeline()
