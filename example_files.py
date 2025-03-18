import json
import os

import main


def read_json_gen(file_name: str):
    dir_path: str = os.path.join(os.path.dirname(__file__), file_name)
    with open(dir_path, 'r', encoding=main.ENCODING) as f:
        return json.load(f)


def read_active_example():
    return read_json_gen('examples/activ.json')


def get_programs_active_info_test_file():
    return read_active_example()["data"]


def read_homeappliances_example():
    return read_json_gen('examples/homeappliances.json')


def read_status_example():
    return read_json_gen('examples/status.json')
