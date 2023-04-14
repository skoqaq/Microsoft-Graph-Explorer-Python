import requests
import PyYAML
import os
import time
import subprocess
import sys
import webbrowser
import logging
from datetime import datetime, timedelta
from msal import PublicClientApplication
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class GraphApiCaller:
    def __init__(self, account_list_file, graph_api_list_file, main_env_file):
        self.account_list_file = account_list_file
        self.graph_api_list_file = graph_api_list_file
        self.main_env_file = main_env_file
        self.account_list = []
        self.graph_api_list = []
        self.main_env = {}
        self.access_token = {}

    def load_config(self):
        with open(self.main_env_file, "r") as f:
            self.main_env = yaml.safe_load(f)
        with open(self.account_list_file, "r") as f:
            self.account_list = yaml.safe_load(f)
        with open(self.graph_api_list_file, "r") as f:
            self.graph_api_list = yaml.safe_load(f)

    def get_bearer_token(self, account_email):
        # define the public client application
        scopes = ["<https://graph.microsoft.com/.default>"]
        client_id = ""
        redirect_uri = ""
        authority = ""
        app = PublicClientApplication(client_id, authority=authority, redirect_uri=redirect_uri)
        # define the device flow callback function
        def callback(device_code_result):
            logging.info(device_code_result["message"])
        # start the device flow
        device_flow = app.initiate_device_flow(scopes, callback=callback)
        # wait for the user to authenticate
        webbrowser.open(device_flow["verification_uri_complete"])
        print(device_flow["message"])
        sys.stdout.flush()
        time.sleep(10)
        # get the access token
        result = app.acquire_token_by_device_flow(device_flow)
        # save the access token
        self.access_token[account_email] = result["access_token"]

    def get_graph_api(self, url, account_email):
        # get the bearer token
        if account_email not in self.access_token:
            self.get_bearer_token(account_email)
        bearer_token = self.access_token[account_email]
        # send the request to the graph api
        headers = {"Authorization": "Bearer " + bearer_token}
        response = requests.get(url, headers=headers)
        return response.json()

    def run(self):
        # get the list of graph apis
        graph_api_list = self.graph_api_list["graph_api_list"]
        # iterate over the list of accounts
        for account in self.account_list:
            # get the list of graph apis for this account
            account_graph_api_list = account["graph_api_list"]
            # iterate over the list of graph apis for this account
            for graph_api in account_graph_api_list:
                # check if this graph api is in the list of graph apis
                if graph_api in graph_api_list:
                    # get the graph api
                    response = self.get_graph_api(graph_api, account["account"]["user_mail"])
                    # output the result
                    print(account["account"]["user_name"] + " - " + graph_api + " - " + str(response))
                    sys.stdout.flush()

if __name__ == "__main__":
    # set the logging level
    logging.basicConfig(level=logging.INFO)
    # create the graph api caller
    graph_api_caller = GraphApiCaller("conf/profiles/account_list.yml", "conf/graph_api_list.yml", "conf/main_env.yml")
    # load the config
    graph_api_caller.load_config()
    # run the graph api caller
    graph_api_caller.run()
