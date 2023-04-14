import os
import time
import schedule
import yaml
import logging

def load_config():
    with open('conf/config.yml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

def run_task(account_config, api_list):
    # 执行任务
    logging.info('start to run task for account {}'.format(account_config['email']))
    # 调用 API
    # ...

def main():
    config = load_config()
    account_list = config['main_env']['account_list']
    api_list = config['main_env']['graph_api_list']
    for account_config in account_list:
        schedule.every(account_config['cron']['interval']).minutes.do(run_task, account_config, api_list)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    main()
