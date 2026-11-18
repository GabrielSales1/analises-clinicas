from flask import Flask,render_template, request , redirect, url_for, flash, session
import flask_login
from db import db
from main import app

from models.coletas_model import Coleta 

@app.route('/coletas')
@flask_login.login_required
def coletas() : 
    return ('<p> say gex </p>')