"""Constants for Multi Zone Receiver tests."""

from homeassistant.const import CONF_NAME

from custom_components.multi_zone_receiver.const import (
    CONF_ZONE_1,
    CONF_ZONE_2,
    CONF_ZONE_3,
)

MOCK_CONFIG = {
    CONF_NAME: "test_name",
    CONF_ZONE_1: "test_zone_1",
    CONF_ZONE_2: "test_zone_2",
    CONF_ZONE_3: "test_zone_3",
}
