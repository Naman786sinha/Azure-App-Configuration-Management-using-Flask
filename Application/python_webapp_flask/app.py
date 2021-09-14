
from flask import Flask as _flask
from python_webapp_flask.configuration import config as _config
from flask_cors import CORS as _CORS
from flask_restplus import Api as _api
#from python_webapp_flask.configuration.logger import setup_logging

version='1.0' 
title='Azure App Configuration Management'

_config.initialize_config( global_config ={'version_number': str(version), 'title': str(title)})

app = _flask(title)
_CORS(app=app)
app.debug = True

_api(app, **_config.app_global_config)

# add blueprints to it
from python_webapp_flask.model.blueprint import blueprint
app.register_blueprint(blueprint)
