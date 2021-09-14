import os, json
from azure.appconfiguration import AzureAppConfigurationClient

def  fetch_config(connection_str):

    client = AzureAppConfigurationClient.from_connection_string(connection_str)

    filtered_listed = client.list_configuration_settings()
    l={}
    for item in  filtered_listed:
        l[item.key] = item.value
    return  l

def initialize_config(global_config=None):

    global CONF_ENV, app_global_config

    app_global_config = global_config

    #if unpecified, default to dev enviroment
    configuration_service_connection_string =  "APP_CONFIGURATION_RESOURCE_CONNECTION_STRING"
    CONF_ENV = os.environ.get("AppConfigConnection", configuration_service_connection_string)
   

    for k,v in fetch_config(CONF_ENV).items():
        app_global_config[k] = v    


    