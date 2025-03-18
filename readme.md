# parser form Homeconnect API for Washer for telegraf to influxDB

## intro

for using this tool you need `client_id` from your homeconnect developer application
I use in application settings **device flow** way and the genered `refresh_token`

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