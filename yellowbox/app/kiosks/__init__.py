from flask import Blueprint

kiosks = Blueprint('kiosks', __name__)

from . import views
