# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 11:38:44 2016

@author: milanz
"""

from flask import Flask
import sys

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from %s, python %s" % (sys.platform, sys.version)

if __name__ == "__main__":
    app.run()