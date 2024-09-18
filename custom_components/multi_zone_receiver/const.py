"""Constants for Multi Zone Receiver."""

# Base component constants
NAME = "Multi Zone Receiver"
DOMAIN = "multi_zone_receiver"
VERSION = "0.6.1"

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

# Services
SERVICE_TOGGLE_VOLUME_MUTE = "toggle_volume_mute"
SERVICE_TOGGLE_POWER = "toggle_power"
SERVICE_TURN_ON_WITH_SOURCE = "turn_on_with_source"
SERVICE_CONFIGURE_ZONES_WITH_SOURCE = "configure_zones_with_source"

# Input Keys
ATTR_ZONES = "zones"
ATTR_OFF_ZONES = "off_zones"
ATTR_ACTIVE = "active"
ATTR_AVAILABLE = "available"
ATTR_DEFAULT = "default"

# Configuration and options
CONF_ENABLED = "enabled"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_ZONES = "zones"
CONF_ZONE_1 = "zone_1"
CONF_ZONE_2 = "zone_2"
CONF_ZONE_3 = "zone_3"
CONF_VOLUME_STEP = "volume_step"

# Defaults
DEFAULT_NAME = DOMAIN
DEFAULT_VOLUME_STEP = 0.1


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
