"""Constants for Multi Zone Receiver."""

# Base component constants
NAME = "Multi Zone Receiver"
DOMAIN = "multi_zone_receiver"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.4.0"

ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/jzucker2/multi-zone-receiver/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
MEDIA_PLAYER = "media_player"
PLATFORMS = [BINARY_SENSOR, SENSOR, MEDIA_PLAYER]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_ZONES = "zones"
CONF_ZONE_1 = "zone_1"
CONF_ZONE_2 = "zone_2"
CONF_ZONE_3 = "zone_3"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
