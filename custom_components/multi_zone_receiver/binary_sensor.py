"""Binary sensor platform for Multi Zone Receiver."""

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)

from . import MultiZoneReceiverConfigEntry
from .entity import MultiZoneReceiverZoneEntity


async def async_setup_entry(
    hass, entry: MultiZoneReceiverConfigEntry, async_add_devices
):
    """Setup binary_sensor platform."""
    async_add_devices(
        [
            MultiZoneReceiverZonePowerBinarySensor(entry, k)
            for k in entry.runtime_data.zone_keys
        ]
    )


class MultiZoneReceiverZonePowerBinarySensor(
    MultiZoneReceiverZoneEntity, BinarySensorEntity
):
    """multi_zone_receiver zone power binary_sensor class."""

    _attr_device_class = BinarySensorDeviceClass.POWER

    @property
    def name(self):
        """Return the name of the binary_sensor."""
        return f"{self.zone_name} Power"

    @property
    def unique_id_suffix(self):
        """Return a second half of ID to use for this entity."""
        return "power"

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self._get_is_on_state_for_zone(self.zone_entity)
