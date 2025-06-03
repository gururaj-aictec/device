# database.py
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, request, jsonify
from  flask import render_template
db = SQLAlchemy()
os.environ["FLASK_ENV"] = "development"
os.environ["FLASK_DEBUG"] = "1"
app = Flask(__name__)
app.debug = True