"""Binary sensor platform for Multi Zone Receiver."""
from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import BINARY_SENSOR
from .const import BINARY_SENSOR_DEVICE_CLASS
from .const import DEFAULT_NAME
from .entity import MultiZoneReceiverEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    async_add_devices([MultiZoneReceiverBinarySensor(entry)])


class MultiZoneReceiverBinarySensor(MultiZoneReceiverEntity, BinarySensorEntity):
    """multi_zone_receiver binary_sensor class."""

    @property
    def name(self):
        """Return the name of the binary_sensor."""
        return f"{DEFAULT_NAME}_{BINARY_SENSOR}"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return BINARY_SENSOR_DEVICE_CLASS

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return True
