import os
import json
import requests
import webbrowser
from datetime import datetime, timedelta


class AccountLogin:
    def __init__(self, config_folder, tenant_id, client_id, scopes):
        self.config_folder = config_folder
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.scopes = scopes
        self.graph_api_endpoint = 'https://graph.microsoft.com/v1.0'

    def run(self):
        # Get device code
        endpoint = f'{self.graph_api_endpoint}/oauth2/devicecode'
        data = {
            'client_id': self.client_id,
            'scope': ' '.join(self.scopes)
        }
        response = requests.post(endpoint, data=data).json()
        print(response['message'])
        webbrowser.open(response['verification_url'])
        device_code = response['device_code']
        expires_in = response['expires_in']
        interval = response['interval']

        # Get access token
        access_token = None
        start_time = datetime.now()
        while (datetime.now() - start_time).seconds < expires_in:
            endpoint = f'{self.graph_api_endpoint}/oauth2/token'
            data = {
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                'client_id': self.client_id,
                'device_code': device_code
            }
            response = requests.post(endpoint, data=data).json()
            if 'access_token' in response:
                access_token = response['access_token']
                break
            elif 'error' in response and response['error'] == 'authorization_pending':
                pass  # keep waiting
            else:
                print('Authorization failed')
                return

            time.sleep(interval)

        # Get user profile
        headers = {'Authorization': f'Bearer {access_token}'}
        endpoint = f'{self.graph_api_endpoint}/me'
        response = requests.get(endpoint, headers=headers).json()
        account_email = response['mail']

        # Create profile file
        profile_file = os.path.join(self.config_folder, 'profiles', f'{account_email}.yml')
        if os.path.exists(profile_file):
            choice = input(f'The profile file "{account_email}.yml" already exists. Do you want to overwrite it? (y/n) ')
            if choice.lower() != 'y':
                print('Profile creation cancelled.')
                return

        profile_data = {
            'account_email': account_email,
            'access_token': access_token,
            'refresh_token': response['refresh_token'],
            'access_token_expires_at': (datetime.now() + timedelta(seconds=response['expires_in'])).isoformat(),
            'username': response['userPrincipalName'],
            'added_at': datetime.now().isoformat()
        }
        with open(profile_file, 'w') as f:
            yaml.dump(profile_data, f)

        print(f'Profile file "{account_email}.yml" has been created successfully.')




