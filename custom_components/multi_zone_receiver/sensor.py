"""Sensor platform for Multi Zone Receiver."""

from homeassistant.components.media_player import MediaPlayerState

from . import MultiZoneReceiverConfigEntry
from .entity import MultiZoneReceiverZoneEntity


async def async_setup_entry(
    hass, entry: MultiZoneReceiverConfigEntry, async_add_devices
):
    """Setup sensor platform."""
    final_sensor_list = []
    for zone_key in entry.runtime_data.zone_keys:
        final_sensor_list.extend(
            [
                MultiZoneReceiverStateSensor(entry, zone_key),
                MultiZoneReceiverSourceSensor(entry, zone_key),
                MultiZoneReceiverVolumeSensor(entry, zone_key),
            ]
        )
    async_add_devices(final_sensor_list)


class MultiZoneReceiverStateSensor(MultiZoneReceiverZoneEntity):
    """multi_zone_receiver Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.zone_name} State"

    @property
    def unique_id_suffix(self):
        """Return a second half of ID to use for this entity."""
        return f"{self.zone_safe_name}_state"

    @property
    def state(self) -> MediaPlayerState | None:
        """Return the state of the zone."""
        return self._get_state_value_for_zone(self.zone_entity)

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:audio-video"


class MultiZoneReceiverSourceSensor(MultiZoneReceiverZoneEntity):
    """multi_zone_receiver Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.zone_name} Source"

    @property
    def unique_id_suffix(self):
        """Return a second half of ID to use for this entity."""
        return f"{self.zone_safe_name}_source"

    @property
    def state(self) -> str | None:
        """Return the state of the zone."""
        return self.source

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:import"


class MultiZoneReceiverVolumeSensor(MultiZoneReceiverZoneEntity):
    """multi_zone_receiver Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.zone_name} Volume"

    @property
    def unique_id_suffix(self):
        """Return a second half of ID to use for this entity."""
        return f"{self.zone_safe_name}_volume"

    @property
    def state(self) -> float | None:
        """Return the state of the zone."""
        return self.volume_level

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:volume-medium"
