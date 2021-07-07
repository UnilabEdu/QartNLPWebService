from flask import Blueprint

tagging_blueprint = Blueprint('tagging',
                              __name__,
                              template_folder='templates',
                              static_folder='static'
                              )
