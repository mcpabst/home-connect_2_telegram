#! /usr/bin/python3
# -*- encoding: utf-8 -*-
import argparse
import base64
import json
import os

import requests
import yaml

import example_files

__author__ = 'Markus Pabst'
__since__ = '2025-03-17'
__credits__ = [""]
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = ""
__status__ = ""
__copyright__ = "Copyright 2025"

ENCODING: str = 'utf-8'
base_url: str
access_token: str
refresh_token: str
encoded_data_base_auth: str
test_intern: bool = True

NAME_KEY = 'key'
NAME_VALUE = 'value'
NAME_BASE_URL = 'base_url'
NAME_REFRESH_TOKEN = 'refresh_token'
NAME_CLIENT_ID = 'client_id'

test_intern: bool = False


def get_access_token(m_encoded_data_base_auth) -> str:
    url = "{}/security/oauth/token".format(base_url)
    payload = "grant_type=refresh_token&refresh_token={}&scope=".format(refresh_token)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': "Basic {}".format(m_encoded_data_base_auth)
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code.__eq__(200):
        data = json.loads(response.text)
        return data["access_token"]
    else:
        raise RuntimeError("failure in request {} ,{}".format(response.status_code, response.text))
    pass


def get_header_with_token():
    global access_token
    return {
        'Authorization': "Bearer {}".format(access_token),
        'Accept': 'application/vnd.bsh.sdk.v1+json'
    }


def get_home_appliances():
    data: dict
    if not test_intern:
        url = "{}/api/homeappliances".format(base_url)
        response = requests.request("GET", url, headers=get_header_with_token(), data={})
        if response.status_code == 200:
            data = json.loads(response.text)
        else:
            raise RuntimeError("failure in request {} ,{}".format(response.status_code, response.text))
    else:
        data = example_files.read_homeappliances_example()
    return data["data"]["homeappliances"]


def get_haid(m_home_appliance) -> str:
    return m_home_appliance["haId"]


def get_status(haid: str) -> dict:
    data: dict
    if not test_intern:
        url = "{}/api/homeappliances/{}/status".format(base_url, haid)
        response = requests.request("GET", url, headers=get_header_with_token(), data={})
        if response.status_code == 200:
            data = json.loads(response.text)
        else:
            raise RuntimeError("failure in request")
    else:
        data = example_files.read_status_example()

    return data["data"]["status"]


def is_washer_status_door_open(i_status) -> bool:
    for pair in i_status:
        if pair['key'].__eq__('BSH.Common.Status.DoorState') and pair['value'].__eq__(
                'BSH.Common.EnumType.DoorState.Open'):
            return True
        pass
    return False


def bool_to_int(m_in_bool: bool):
    if m_in_bool:
        return 1
    return 0


def is_washer_status_active(i_status: dict) -> bool:
    for pair in i_status:
        if pair[NAME_KEY].__eq__('BSH.Common.Status.OperationState') and pair['value'].__eq__(
                'BSH.Common.EnumType.OperationState.Inactive'):
            return False
        pass
    return True


def get_programs_active_info(haid: str):
    data: dict
    if not test_intern:
        url = "{}/api/homeappliances/{}/programs/active".format(base_url, haid)
        response = requests.request("GET", url, headers=get_header_with_token(), data={})
        if response.status_code == 200:
            data = json.loads(response.text)
        else:
            raise RuntimeError("failure in request {} ,{}".format(response.status_code, response.text))
    else:
        data = example_files.read_active_example()
    return data["data"]


def get_washer_programs_active_spin_speed(m_active_info: dict) -> int:
    """
    :param m_active_info:
    :return: int
    """
    options = m_active_info['options']
    speed: int = 0
    for option in options:
        key = option[NAME_KEY]
        value = option[NAME_VALUE]
        if key.__eq__('LaundryCare.Washer.Option.SpinSpeed'):
            try:
                value = value.split('LaundryCare.Washer.EnumType.SpinSpeed.RPM')[1]
                speed = int(value)
            except ValueError:
                pass
    return speed


def get_washer_programs_active_process_phase(m_active_info: dict) -> str:
    """
    :param m_active_info:
    :return: int
    """
    options = m_active_info['options']
    progress_phase: str = ''
    for option in options:
        key = option[NAME_KEY]
        value = option[NAME_VALUE]
        if key.__eq__('LaundryCare.Common.Option.ProcessPhase'):
            progress_phase = value.split('LaundryCare.Common.EnumType.ProcessPhase.')[1]
    return progress_phase


def get_washer_programs_active_program_progress(m_active_info: dict) -> int:
    """
    :param m_active_info:
    :return: int
    """
    options = m_active_info['options']
    progress: int = 0
    for option in options:
        key = option[NAME_KEY]
        value = option[NAME_VALUE]
        if key.__eq__('BSH.Common.Option.ProgramProgress'):
            progress = value
    return progress


def get_washer_programs_active_name(m_active_info) -> str:
    key: str = m_active_info[NAME_KEY]
    key = key.split('LaundryCare.Washer.Program.')[1]
    return key


def read_config():
    global base_url
    global refresh_token
    global encoded_data_base_auth
    global access_token
    config_file_name = 'config.yaml'

    client_id: str
    client_secret: str = ""

    dir_path: str = os.path.join(os.path.dirname(__file__), config_file_name)

    # name_client_secret = 'client_secret'
    with open(dir_path, 'r') as f:
        config = yaml.safe_load(f)

    base_url = config[NAME_BASE_URL]
    if not base_url:
        raise RuntimeError("{} was not set correctly in {}".format(NAME_BASE_URL, config_file_name))

    login_data = config['login']
    if not login_data:
        raise RuntimeError("{} was not set correctly in {}".format('login', config_file_name))

    refresh_token = login_data[NAME_REFRESH_TOKEN]
    if not refresh_token:
        raise RuntimeError("{} was not set correctly in {}".format(NAME_REFRESH_TOKEN, config_file_name))

    client_id = login_data[NAME_CLIENT_ID]
    if not refresh_token:
        raise RuntimeError("{} was not set correctly in {}".format(NAME_REFRESH_TOKEN, config_file_name))
    # client_secret = login_data[name_client_secret]

    base: str = "{}:{}".format(client_id, client_secret)
    data_bytes = base.encode(ENCODING)
    encoded_data_base_auth = base64.b64encode(data_bytes).decode(ENCODING)
    access_token = get_access_token(encoded_data_base_auth)
    pass


def get_washers_json():
    washers = []
    home_appliances = get_home_appliances()
    for home_appliance in home_appliances:
        if home_appliance['type'].upper().__eq__("WASHER"):
            values = {'is_connected': home_appliance['connected'],
                      'connected_int': bool_to_int(home_appliance['connected'])}
            washer = home_appliance
            washer['name'] = home_appliance['name'].strip()
            del washer['connected']
            haid = get_haid(home_appliance)
            status = get_status(haid)
            values['door_open_int'] = bool_to_int(is_washer_status_door_open(status))
            values['is_door_open'] = is_washer_status_door_open(status)
            values['active_int'] = bool_to_int(is_washer_status_active(status))
            values['is_active'] = is_washer_status_active(status)
            values['active_int'] = bool_to_int(is_washer_status_active(status))
            if is_washer_status_active(status):
                active_info: dict = get_programs_active_info(haid)
                values["programs_active_spin_speed"] = get_washer_programs_active_spin_speed(active_info)
                values["programs_active_name"] = get_washer_programs_active_name(active_info)
                values["programs_active_program_progress"] = get_washer_programs_active_program_progress(active_info)
                values["programs_active_process_phase"] = get_washer_programs_active_process_phase(active_info)
            washer['v'] = values
            washers.append(washer)
        pass
    return json.dumps(washers)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process some parameters.")
    parser.add_argument('-t', '--type', type=str, help='device type, with allowed values like: w, washer',
                        required=True)
    read_config()
    args = parser.parse_args()

    allowed_types = ['W', 'WASHER']

    if not args.type or not args.type.upper() in allowed_types:
        err: str = "This device type is not defined yet. Defined types are {}".format(allowed_types)
        raise ValueError(err)

    if args.type.upper().__eq__('WASHER') or args.type.upper().__eq__('W'):
        print(get_washers_json())
