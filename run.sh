#!/bin/sh

Xephyr -br -ac -noreset -screen 1680x1050 :1 & 

/usr/bin/python3 twm/main.py