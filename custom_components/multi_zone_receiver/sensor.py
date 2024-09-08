"""Sensor platform for Multi Zone Receiver."""

from .const import DEFAULT_NAME, ICON, SENSOR
from .entity import MultiZoneReceiverEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    async_add_devices([MultiZoneReceiverSensor(entry)])


class MultiZoneReceiverSensor(MultiZoneReceiverEntity):
    """multi_zone_receiver Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return "foo"

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return "multi_zone_receiver__custom_device_class"
