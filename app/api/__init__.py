from flask_restful import Api
from .routes import NerTagApi

api = Api(prefix='/api/')

api.add_resource(NerTagApi, '/')
