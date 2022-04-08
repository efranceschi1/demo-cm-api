from config import *


def main():
    cm = Config()

    # Lists all known clusters.
    api_response = cm.clusters().read_clusters(view='SUMMARY')
    for cluster in api_response.items:
        print(f"=> Found cluster {cluster.name} version {cluster.full_version}")
        services = cm.services().read_services(cluster.name, view='FULL')
        for service in services.items:
            print(f"   * SERVICE: {service.type}")
            if service.type in ['HIVE', 'RANGER']:
                configs = cm.services().read_service_config_with_http_info(cluster.name, service.name)
                for config in configs[0].items:
                    if 'database' in config.name:
                        print(f"      - {config.name} = {config.value}")


if __name__ == "__main__":
    main()
