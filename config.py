import os
import yaml
import cm_client
from os.path import expanduser


class Config:
    def __init__(self):
        cm_config_dir = expanduser("~/.cm")

        if not os.path.isdir(cm_config_dir):
            os.mkdir(cm_config_dir)

        cm_config_file = f"{cm_config_dir}/config.yaml"
        if not os.path.isfile(cm_config_file):
            print(f"Config file not found: {cm_config_file}")
            cm_template_file = "config_template.yaml"
            with open(cm_template_file, "r") as src:
                with open(cm_config_file, "w") as dst:
                    print(f"Creating config file from template: {cm_template_file}")
                    dst.write(src.read())
                    print(f"Created the new config file: {cm_config_file}")
                    print("Please, edit this file and try again")
                    exit(1)

        with open(cm_config_file, "r") as config_stream:
            try:
                self.config = yaml.safe_load(config_stream)
            except yaml.YAMLError as err:
                print(err)

        cfg = self.config['cm_client']['configuration']
        cm_client.configuration.username = cfg['username']
        cm_client.configuration.password = cfg['password']
        self.api_client = cm_client.ApiClient(cfg['api_url'])

    def clusters(self) -> cm_client.ClustersResourceApi:
        return cm_client.ClustersResourceApi(self.api_client)

    def services(self) -> cm_client.ServicesResourceApi:
        return cm_client.ServicesResourceApi(self.api_client)

