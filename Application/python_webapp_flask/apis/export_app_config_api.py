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
from flask_restplus import Namespace

create_feature =  reqparse.RequestParser()
create_feature.add_argument('name', required=True, type=str)
create_feature.add_argument('label', required=True, type=str)
create_feature.add_argument('description', required=True, type=str)

app = Namespace('export_app_config', description='Export App Config Properties files')
 
@app.route("/dev")
class AppConfigExportDev(Resource):

    def __init__(self, input):
        self.input = input

    def post(self,):

        username = config.app_global_config['SERVICE_PRINCIPAL_USERNAME_VALUE_FROM_APP_CONFIG']
        password = config.app_global_config['SERVICE_PRINCIPAL_PASSWORD_VALUE_FROM_APP_CONFIG']
        tenant = config.app_global_config['TENANT_NAME_VALUE_FROM_APP_CONFIG']

        connection_string = "YOUR_STORAGE_ACCOUNT_CONNECTION_STRING"
        cont_name = config.app_global_config['CONTAINER_NAME_VALUE_FROM_APP_CONFIG']

        azcli().invoke(["login","--service-principal", "-u", username ,"-p", password , "--tenant" ,tenant])
        azcli().invoke(["account", "set", "--subscription", "SUBSCRIPTION_NAME"]) 
        print("Login!")

        #Download for Dev
        azcli().invoke(["appconfig", "kv", "export", "--name", "APP_CONFIG_RESOURCE_NAME", "-d", "file", "--path", "./Dev.properties", "--format", "properties", "--yes"])
        print("File downloaded for Dev!")

        #Upload for Dev-------------------------------------
        blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=cont_name, blob_name="AppConfigFile/Dev.properties")

        with open("./Dev.properties", "rb") as data:
            blob.upload_blob(data,overwrite=True)
        print("File uploaded for Dev!")

        return "Success for dev!"

