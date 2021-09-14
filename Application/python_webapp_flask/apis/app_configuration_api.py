from flask import Flask
from flask import request, abort
from flask_restful import Resource,Api
from azure.storage.blob import PublicAccess
from azure.storage.blob import BlobClient
from azure.cli.core import get_default_cli as azcli
import json
from flask_restplus import reqparse
from python_webapp_flask.configuration import config
from flask import url_for, Blueprint
from flask_restplus import Api
from flask_cors import CORS as _CORS
from werkzeug.utils import cached_property
from flask_restplus import Namespace, fields

#add_key =  reqparse.RequestParser()
#add_key.add_argument('key', required=True, type=str)
#add_key.add_argument('value', required=True, type=str)
#add_key.add_argument('label', type=str)
#add_key.add_argument('storeName', required=True, type=str)
#add_key.add_argument('subscription', required=True, type=str)

get_status =  reqparse.RequestParser()
get_status.add_argument('key', required=True, type=str)
get_status.add_argument('label', type=str)
get_status.add_argument('storeName', required=True, type=str)
get_status.add_argument('subscription', required=True, type=str)

get_all_keys = reqparse.RequestParser()
get_all_keys.add_argument('storeName', required=True, type=str)
get_all_keys.add_argument('subscription', required=True, type=str)

app = Namespace('app_configuration', description='CRUD Operations')

add_key_params = app.model("AddNewKey", {
    'key': fields.String(required=True, description = 'Name of the Key to be created/modified', example = 'key1'),
    'value': fields.String(required = True, description = 'Value of the Key to be created/modified', example = 'value1'),
    'label': fields.String(description = 'Label if any', example = 'Bot'),
    'storeName': fields.String(required = True, description = 'Name of the App Config Resource', example = 'Dev-App Config'),
    'subscription': fields.String(required = True, description = 'Subscription in which the AppConfig Resource lies', example = 'Subscription1'),
})

@app.route("/AddNewKey")
class AppConfigAddNewKey(Resource):

    def __init__(self, input):
        self.input = input

    @app.expect(add_key_params)
    def post(self,):

        username = config.app_global_config['SERVICE_PRINCIPAL_USERNAME_VALUE_FROM_APP_CONFIG']
        password = config.app_global_config['SERVICE_PRINCIPAL_PASSWORD_VALUE_FROM_APP_CONFIG']
        tenant = config.app_global_config['TENANT_NAME_VALUE_FROM_APP_CONFIG']

        args = app.payload
        label = args['label']    
        key = args['key']
        value = args['value']    
        storeName = args['storeName']
        subscription = args['subscription']
        azcli().invoke(["login","--service-principal", "-u", username ,"-p", password , "--tenant" ,tenant])
        azcli().invoke(["account", "set", "--subscription", subscription]) 
        print("Logged in!")
        Dict = {'status': ''}
        # Create a new key-value 
        cli = azcli()
        if label is None:
            cli.invoke(["appconfig", "kv", "set", "--name", storeName, "--key", key, "--value", value, "--yes"])
        else:
            cli.invoke(["appconfig", "kv", "set", "--name", storeName, "--key", key, "--value", value, "--label", label, "--yes"])
        if cli.result.result:
            Dict['status'] = "Success"
        else:            
            Dict['status'] = "Failed"
        return Dict

@app.route("/GetStatus")
class AppConfigGetStatus(Resource):

    def __init__(self, input):
        self.input = input

    @app.expect(get_status, validate=True)
    def get(self,):

        username = config.app_global_config['SERVICE_PRINCIPAL_USERNAME_VALUE_FROM_APP_CONFIG']
        password = config.app_global_config['SERVICE_PRINCIPAL_PASSWORD_VALUE_FROM_APP_CONFIG']
        tenant = config.app_global_config['TENANT_NAME_VALUE_FROM_APP_CONFIG']
        
        args = get_status.parse_args()
        key = args['key']
        label = args['label']
        storeName = args['storeName']
        subscription = args['subscription']
        azcli().invoke(["login","--service-principal", "-u", username ,"-p", password , "--tenant" ,tenant])
        azcli().invoke(["account", "set", "--subscription", subscription]) 
        print("Logged in!")

        Dict = {'key': key, 'value': 'Not Found'} 

        #Get a key-value 
        try:
            cli = azcli()
            if label is None:
                cli.invoke(["appconfig", "kv", "show", "-n", storeName, "--key", key])
            else:
                cli.invoke(["appconfig", "kv", "show", "-n", storeName, "--key", key, "--label", label])            
            print(type(cli.result.result))
            if cli.result.result:
                return cli.result.result
            else:            
                return Dict
        except Exception as inst:
            print("Inside exception",inst)    
            return Dict

@app.route("/GetAllKeys")
class AppConfigGetAllKeys(Resource):

    def __init__(self, input):
        self.input = input

    @app.expect(get_all_keys, validate=True)
    def get(self,):

        username = config.app_global_config['SERVICE_PRINCIPAL_USERNAME_VALUE_FROM_APP_CONFIG']
        password = config.app_global_config['SERVICE_PRINCIPAL_PASSWORD_VALUE_FROM_APP_CONFIG']
        tenant = config.app_global_config['TENANT_NAME_VALUE_FROM_APP_CONFIG']
        
        args = get_all_keys.parse_args()
        storeName = args['storeName']
        subscription = args['subscription']
        azcli().invoke(["login","--service-principal", "-u", username ,"-p", password , "--tenant" ,tenant])
        azcli().invoke(["account", "set", "--subscription", subscription]) 
        print("Logged in!")

        Dict = {'key': storeName,'value': 'Not Found'} 

        responseList = []

        responseList.append(Dict)

        # Get all key-values 
        try:
            cli = azcli()
            cli.invoke(["appconfig", "kv", "list", "-n", storeName, "--all"])
            print(type(cli.result.result))
            if cli.result.result:
                d = json.dumps(cli.result.result)
                return d
            else:     
                d = json.dumps(responseList)       
                return d
        except Exception as inst:
            print("Inside exception",inst) 
            d = json.dumps(responseList)    
            return d