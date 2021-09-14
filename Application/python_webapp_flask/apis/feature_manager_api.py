from flask import Flask
from flask import request, abort
from flask_restful import Resource,Api
from azure.storage.blob import PublicAccess
from azure.storage.blob import BlobClient
from azure.cli.core import get_default_cli as azcli
import json
from flask_restplus import reqparse,inputs
from python_webapp_flask.configuration import config
from flask import url_for, Blueprint
from flask_restplus import Api
from flask_cors import CORS as _CORS
from werkzeug.utils import cached_property
from flask_restplus import Namespace, fields

restart_app =  reqparse.RequestParser()
restart_app.add_argument('appName', required=True, type=str)
restart_app.add_argument('resourceGroup', required=True, type=str)

list_all_features =  reqparse.RequestParser()
list_all_features.add_argument('label', required=True, type=str)

show_feature =  reqparse.RequestParser()
show_feature.add_argument('name', required=True, type=str)
show_feature.add_argument('label', required=True, type=str)


app = Namespace('feature_manager', description='CRUD Operations')

create_feature_params = app.model("CreateFeature", {
    'name': fields.String(required=True, description = 'Name of the Feature to be created', example = 'HideJourney'),
    'label': fields.String(required = True, description = 'Label of the Feature', example = 'webapp'),
    'description': fields.String(required = True, description = 'Description of the Feature', example = 'This feature is to hide journey in the Web App.'),
})

modify_feature_params = app.model("ModifyFeature", {
    'name': fields.String(required=True, description = 'Name of the Feature to be modified', example = 'HideJourney'),
    'label': fields.String(required = True, description = 'Label of the Feature', example = 'webapp'),
    'status': fields.String(required = True, description = 'True or False', example = 'true/false'),
}) 

@app.route("/ListAllFeatures")
class ListAllFeatures(Resource):

    def __init__(self, input):
        self.input = input

    @app.expect(list_all_features, validate=True)
    def get(self,):
        args = list_all_features.parse_args()
        label = args['label']
        connectionString = config.app_global_config['YOUR_APP_CONFIGURATION_RESOURCE_WRITE_KEY(CONNECTION_STRING)']
        cli = azcli()
        cli.invoke(["appconfig", "feature", "list", "--connection-string", connectionString, "--label", label, "-o", "json"])       
        if cli.result.result:
            d = json.dumps(cli.result.result)
            return d
        else:                    
            return ""

@app.route("/CreateFeature")
class CreateFeature(Resource):

    def __init__(self, input):
        self.input = input

    @app.expect(create_feature_params)
    def put(self,):
        args = app.payload
        name = args['name']
        description = args['description']
        label = args['label']
        connectionString = config.app_global_config['YOUR_APP_CONFIGURATION_RESOURCE_WRITE_KEY(CONNECTION_STRING)']
        #name = "Feature-.appconfig.featureflag/"
        #name += temp
        cli = azcli()
        cli.invoke(["appconfig", "feature", "set", "--connection-string", connectionString, "--feature", name, "--description", description, "--label", label, "--yes", "-o", "json"])       
        if cli.result.result:
            d = json.dumps(cli.result.result)
            return d
        else:                    
            return ""

@app.route("/ModifyFeature")
class ModifyFeature(Resource):

    def __init__(self, input):
        self.input = input
    
    @app.expect(modify_feature_params)
    def post(self,):
        args = app.payload
        name = args['name']
        label = args['label']
        status = args['status']
        connectionString = config.app_global_config['YOUR_APP_CONFIGURATION_RESOURCE_WRITE_KEY(CONNECTION_STRING)']
        #name = "Feature-.appconfig.featureflag/"
        #name += temp
        cli = azcli()
        print(status , "---------")
        print(type(status))
        if status.lower() == 'false':
            cli.invoke(["appconfig", "feature", "disable", "--connection-string", connectionString, "--feature", name, "--label", label, "--yes", "-o", "json"])
        if status.lower() == 'true':            
            cli.invoke(["appconfig", "feature", "enable", "--connection-string", connectionString, "--feature", name, "--label", label, "--yes", "-o", "json"])        
        if cli.result.result:
            d = json.dumps(cli.result.result)
            return d
        else:                    
            return ""
        #return ""       

@app.route("/DeleteFeature")
class DeleteFeature(Resource):

    def __init__(self, input):
        self.input = input
    
    @app.expect(show_feature, validate=True)
    def delete(self,):
        args = show_feature.parse_args()
        name = args['name']
        label = args['label']
        connectionString = config.app_global_config['YOUR_APP_CONFIGURATION_RESOURCE_WRITE_KEY(CONNECTION_STRING)']
        #name = "Feature-.appconfig.featureflag/"
        #name += temp
        cli = azcli()
        cli.invoke(["appconfig", "feature", "delete", "--connection-string", connectionString, "--feature", name, "--label", label, "--yes", "-o", "json"])       
        if cli.result.result:
            d = json.dumps(cli.result.result)
            return d
        else:                    
            return ""

@app.route("/ShowFeature")
class ShowFeature(Resource):

    def __init__(self, input):
        self.input = input

    @app.expect(show_feature, validate=True)
    def get(self,):
        args = show_feature.parse_args()
        name = args['name']
        label = args['label']
        connectionString = config.app_global_config['YOUR_APP_CONFIGURATION_RESOURCE_WRITE_KEY(CONNECTION_STRING)']
        #name = "Feature-.appconfig.featureflag/"
        #name += temp
        cli = azcli()
        cli.invoke(["appconfig", "feature", "show", "--connection-string", connectionString, "--feature", name, "--label", label, "-o", "json"])       
        if cli.result.result:
            d = json.dumps(cli.result.result)
            return d
        else:                    
            return ""
