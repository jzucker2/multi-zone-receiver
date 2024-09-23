"""Sensor platform for Multi Zone Receiver."""

from homeassistant.components.media_player import MediaPlayerState

from . import MultiZoneReceiverConfigEntry
from .entity import MultiZoneReceiverEntity


async def async_setup_entry(
    hass, entry: MultiZoneReceiverConfigEntry, async_add_devices
):
    """Setup sensor platform."""
    async_add_devices(
        [
            MultiZoneReceiverStateSensor(entry),
            MultiZoneReceiverSourceSensor(entry),
            MultiZoneReceiverVolumeSensor(entry),
        ]
    )


class MultiZoneReceiverStateSensor(MultiZoneReceiverEntity):
    """multi_zone_receiver Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.main_zone_name} State"

    @property
    def unique_id_suffix(self):
        """Return a second half of ID to use for this entity."""
        return "state"

    @property
    def state(self) -> MediaPlayerState | None:
        """Return the state of the zone."""
        return self._get_state_value_for_zone(self.main_zone_entity)

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:audio-video"


class MultiZoneReceiverSourceSensor(MultiZoneReceiverEntity):
    """multi_zone_receiver Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.main_zone_name} Source"

    @property
    def unique_id_suffix(self):
        """Return a second half of ID to use for this entity."""
        return "source"

    @property
    def source(self) -> str | None:
        """Return the current input source."""
        return self._get_source_for_zone(self.main_zone_entity)

    @property
    def state(self) -> str | None:
        """Return the state of the zone."""
        return self.source

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:import"


class MultiZoneReceiverVolumeSensor(MultiZoneReceiverEntity):
    """multi_zone_receiver Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.main_zone_name} Volume"

    @property
    def unique_id_suffix(self):
        """Return a second half of ID to use for this entity."""
        return "volume"

    @property
    def volume_level(self) -> float | None:
        """Return the volume level of the zone."""
        return self._get_volume_level(self.main_zone_entity)

    @property
    def state(self) -> float | None:
        """Return the state of the zone."""
        return self.volume_level
