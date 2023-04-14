import json
import requests
import time
import yaml

class GraphAPI:

    def __init__(self, account_config_file, api_list):
        self.account_config_file = account_config_file
        self.api_list = api_list
        self.access_token = None
        self.email = None

    def read_account_config(self):
        with open(self.account_config_file, 'r') as f:
            account_config = yaml.safe_load(f)
            self.email = account_config['email']
            self.access_token = account_config['access_token']

    def call_api(self, url):
        session = requests.Session()
        session.headers.update({'Authorization': 'Bearer ' + self.access_token})

        response = session.get(url)

        if response.status_code == 200:
            return response.content.decode('utf-8')
        else:
            print(f'Error calling {url}: {response.status_code}')
            return None

    def call_all_apis(self):
        self.read_account_config()
        print(f'Calling APIs for {self.email}')
        for api_url in self.api_list:
            print(f'Calling {api_url}')
            result = self.call_api(api_url)
            if result:
                print(result)
            time.sleep(1)

if __name__ == '__main__':
    # Read configuration from main environment file
    with open('conf/config.yml', 'r') as f:
        main_env = yaml.safe_load(f)['main_env']
        config_folder = main_env['config_folder']
        account_list = main_env['account_list']
        graph_api_list = main_env['graph_api_list']

    # Call APIs for each account in account_list
    for account_config_file in account_list:
        graph_api = GraphAPI(f'{config_folder}/profiles/{account_config_file}', graph_api_list)
        graph_api.call_all_apis()
