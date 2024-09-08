"""Media Player platform for Multi Zone Receiver."""

from homeassistant.components.media_player import MediaPlayerEntity

from .const import DEFAULT_NAME, MEDIA_PLAYER
from .entity import MultiZoneReceiverEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup media_player platform."""
    async_add_devices([MultiZoneReceiverMediaPlayer(entry)])


class MultiZoneReceiverMediaPlayer(MultiZoneReceiverEntity, MediaPlayerEntity):
    """multi_zone_receiver media_player class. Based on https://github.com/home-assistant/core/blob/dev/homeassistant/components/media_player/__init__.py"""

    @property
    def name(self):
        """Return the name of the media_player."""
        return f"{DEFAULT_NAME}_{MEDIA_PLAYER}"

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return "multi_zone_receiver__custom_media_player_device_class"
