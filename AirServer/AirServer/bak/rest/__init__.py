"""
The flask application package.
"""

from flask import Flask

import models
app = Flask(__name__)

import rest.RestServer
