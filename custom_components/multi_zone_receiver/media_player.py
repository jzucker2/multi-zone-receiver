"""Media Player platform for Multi Zone Receiver."""

from homeassistant.components.media_player import (
    DOMAIN as MEDIA_PLAYER_DOMAIN,
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    SERVICE_VOLUME_DOWN,
    SERVICE_VOLUME_UP,
)

from . import MultiZoneReceiverConfigEntry
from .const import DEFAULT_NAME, MEDIA_PLAYER
from .entity import MultiZoneReceiverEntity


async def async_setup_entry(
    hass, entry: MultiZoneReceiverConfigEntry, async_add_devices
):
    """Setup media_player platform."""
    async_add_devices([MultiZoneReceiverMediaPlayer(entry)])


class MultiZoneReceiverMediaPlayer(MultiZoneReceiverEntity, MediaPlayerEntity):
    """multi_zone_receiver media_player class. Based on https://github.com/home-assistant/core/blob/dev/homeassistant/components/media_player/__init__.py"""

    _attr_device_class = MediaPlayerDeviceClass.RECEIVER

    @property
    def name(self):
        """Return the name of the media_player."""
        return f"{DEFAULT_NAME}_{MEDIA_PLAYER}"

    # @property
    # def device_class(self):
    #     """Return the device class of the sensor."""
    #     return "multi_zone_receiver__custom_media_player_device_class"

    def get_default_zones(self):
        return self.runtime_data.get_all_zones()

    async def async_turn_on(self) -> None:
        """Turn on media player."""
        await self.hass.services.async_call(
            MEDIA_PLAYER_DOMAIN,
            SERVICE_TURN_ON,
            {},
            blocking=True,
            target={ATTR_ENTITY_ID: self.get_default_zones()},
            context=self._context,
        )

    async def async_turn_off(self) -> None:
        """Turn off media player."""
        await self.hass.services.async_call(
            MEDIA_PLAYER_DOMAIN,
            SERVICE_TURN_OFF,
            {},
            blocking=True,
            target={ATTR_ENTITY_ID: self.get_default_zones()},
            context=self._context,
        )

    async def async_volume_up(self) -> None:
        """Volume up the media player."""
        await self.hass.services.async_call(
            MEDIA_PLAYER_DOMAIN,
            SERVICE_VOLUME_UP,
            {},
            blocking=True,
            target={ATTR_ENTITY_ID: self.get_default_zones()},
            context=self._context,
        )

    async def async_volume_down(self) -> None:
        """Volume down the media player."""
        await self.hass.services.async_call(
            MEDIA_PLAYER_DOMAIN,
            SERVICE_VOLUME_DOWN,
            {},
            blocking=True,
            target={ATTR_ENTITY_ID: self.get_default_zones()},
            context=self._context,
        )
