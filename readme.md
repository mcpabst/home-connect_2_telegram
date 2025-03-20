# parser form Homeconnect API for Washer for telegraf to influxDB

## goal

The goal here is to collect data from Homeconnect API and show charts in Grafana

```mermaid
graph LR
    A --> B --> C --> D --> E;
    A["<a href='https://www.home-connect.com'>Home Connect</a>"]
    B["Parser"]
    C["<a href='https://www.influxdata.com/time-series-platform/telegraf'>telegraf</a>"]
    D["<a href='https://www.influxdata.com/lp/influxdb-database'>influxDB</a>"]
    E["<a href='https://grafana.com'>Grafana</a>"]
```
## intro

For using this tool you need `client_id` from your homeconnect developer application
I use in application settings **device flow** way and the generated `refresh_token`

For generate the refresh_token please a rest tool like postman and take the following step

```mermaid
graph TD
    A --> B --> C --> D --> E;
    A["Rest Call DEVICE_FLOW - POST https://{{serverUrl}}/security/oauth/device_authorization"]
    B["remember {{device}} from response"]
    C["Open link with {{device_id}} login, release"]
    D["Rest Call DEVICE_FLOW - POST https://{{serverUrl}}/security/oauth/token"]
    E["remember {{refresh_token}} from response"]
```

config.yaml 
``` 
base_url: https://api.home-connect.com
login:
  refresh_token: jujJyZWdpb24iO.....
  client_id: AAF0EA107717AC7E30....
```

## usage

just call script with:

``python homeconnect_2_telegraf_main.py -t washer``

### in telegraf config

```
[[inputs.exec]]
  commands = ["python3.8 path_to_scrip/home-connect_2_telegraf_main -t WASHER"]
  timeout = "150s"
  interval = "120s"
  data_format = "json"
  name_override = "washers"
  tag_keys = ["brand", "enumber", "haId", "name", "type", "vib"]
  json_string_fields = ["v_door_status", "v_active_status", "v_programs_active_process_phase"]
```