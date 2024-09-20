"""Sensor platform for Multi Zone Receiver."""

from homeassistant.components.media_player import MediaPlayerState
from homeassistant.components.sensor import SensorDeviceClass

from . import MultiZoneReceiverConfigEntry
from .const import DEFAULT_NAME, SENSOR
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
        return f"{DEFAULT_NAME}_{SENSOR}_State"

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
        return f"{DEFAULT_NAME}_{SENSOR}_Source"

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

    _attr_device_class = SensorDeviceClass.VOLUME

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}_Volume"

    @property
    def volume_level(self) -> float | None:
        """Return the volume level of the zone."""
        return self._get_volume_level(self.main_zone_entity)

    @property
    def state(self) -> float | None:
        """Return the state of the zone."""
        return self.volume_level
