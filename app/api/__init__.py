from flask_restful import Api
from .routes import NerTagApi
from .search import SearchApi

api = Api(prefix='/api/')

api.add_resource(NerTagApi, '/')
api.add_resource(SearchApi, '/search/<int:file_id>')
