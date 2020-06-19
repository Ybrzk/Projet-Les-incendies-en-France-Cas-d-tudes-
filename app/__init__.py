#!/usr/bin/env python
# coding: utf-8

# import library
from flask import Flask
from app import config

# Init flask app 
app = Flask(__name__ )


app.config.from_object(config)



# import library
from app import views
from app import models

# le fichier init sert a initialiser l'app de flask 
