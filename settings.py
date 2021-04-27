import json


def save_settings(chunk_size: int, lazy_factor: float, alert_server_port: int, graphql_server_port: int, graphql_server_host: str):
    settings_dict = {
        "chunk_size": chunk_size,
        "lazy_factor": lazy_factor,
        "alert_server_port": alert_server_port,
        "graphql_server_port": graphql_server_port,
        "graphql_server_host": graphql_server_host
    }
    with open("config.json", "w") as json_data_file:
        json_data_file.write(json.dumps(settings_dict))

    with open("frontend/src/config.json", "w") as json_data_file:
        json_data_file.write(json.dumps(settings_dict))


def get_settings():
    with open("config.json", "r") as json_data_file:
        return json.loads(json_data_file.read())
