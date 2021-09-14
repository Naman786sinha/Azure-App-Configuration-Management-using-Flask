from flask_restplus import Api
from flask import url_for, Blueprint
from python_webapp_flask.configuration import config


blueprint = Blueprint('App Configuration Manager', __name__, url_prefix="/azure_app_configuration")

#monkey patch to serve over https
@property
def specs_url(self):
    """Monkey patch for HTTPS"""
    scheme = 'http' if '5000' in self.base_url else 'https'
    return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)
Api.specs_url = specs_url

api = Api(blueprint, title=config.app_global_config['title'],
                     version=config.app_global_config['version_number'])

from python_webapp_flask.apis.feature_manager_api import app as ns1
from python_webapp_flask.apis.app_configuration_api import app as ns2
from python_webapp_flask.apis.export_app_config_api import app as ns3

api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)
