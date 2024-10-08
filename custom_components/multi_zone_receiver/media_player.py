"""Media Player platform for Multi Zone Receiver."""

import asyncio
from collections.abc import Mapping
import logging
from typing import Any

from homeassistant.components.media_player import (
    ATTR_INPUT_SOURCE,
    ATTR_MEDIA_VOLUME_LEVEL,
    ATTR_MEDIA_VOLUME_MUTED,
    ATTR_SOUND_MODE,
    DOMAIN as MEDIA_PLAYER_DOMAIN,
    SERVICE_SELECT_SOUND_MODE,
    SERVICE_SELECT_SOURCE,
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    SERVICE_VOLUME_DOWN,
    SERVICE_VOLUME_MUTE,
    SERVICE_VOLUME_SET,
    SERVICE_VOLUME_UP,
)

from . import MultiZoneReceiverConfigEntry
from .const import (
    ATTR_ACTIVE,
    ATTR_AVAILABLE,
    ATTR_DEFAULT,
    ATTR_OFF_ZONES,
    ATTR_ZONES,
    DEFAULT_NAME,
    DOMAIN,
    MEDIA_PLAYER,
    SERVICE_CONFIGURE_ZONES_WITH_SOURCE,
    SERVICE_TOGGLE_POWER,
    SERVICE_TOGGLE_VOLUME_MUTE,
    SERVICE_TURN_ON_WITH_SOURCE,
)
from .entity import MultiZoneReceiverZoneEntity

_LOGGER: logging.Logger = logging.getLogger(__package__)

MULTI_ZONE_SUPPORTED_FEATURES = (
    MediaPlayerEntityFeature.VOLUME_SET
    | MediaPlayerEntityFeature.VOLUME_MUTE
    | MediaPlayerEntityFeature.VOLUME_STEP
    | MediaPlayerEntityFeature.TURN_ON
    | MediaPlayerEntityFeature.TURN_OFF
    | MediaPlayerEntityFeature.SELECT_SOURCE
    | MediaPlayerEntityFeature.SELECT_SOUND_MODE
)


async def async_setup_entry(
    hass, entry: MultiZoneReceiverConfigEntry, async_add_devices
):
    """Setup media_player platform."""
    main_zone_key = entry.runtime_data.main_zone_key
    only_receiver = MultiZoneReceiverMediaPlayer(entry, main_zone_key)
    async_add_devices([only_receiver])
    only_receiver.async_register_hass_custom_actions(hass)


class MultiZoneReceiverMediaPlayer(MultiZoneReceiverZoneEntity, MediaPlayerEntity):
    """multi_zone_receiver media_player class. Based on https://github.com/home-assistant/core/blob/dev/homeassistant/components/media_player/__init__.py"""

    _attr_device_class = MediaPlayerDeviceClass.RECEIVER
    _attr_supported_features = MULTI_ZONE_SUPPORTED_FEATURES

    @property
    def name(self):
        """Return the name of the media_player."""
        return f"{DEFAULT_NAME}_{MEDIA_PLAYER}"

    @property
    def unique_id_suffix(self):
        """Return a second half of ID to use for this entity."""
        return "media_player"

    def _get_state_tracked_entities_list(self) -> list:
        """The entities that this entity should track"""
        return self.get_all_zones()

    def _get_extra_state_attributes(self) -> Mapping[str, Any] | None:
        final_dict = {
            ATTR_ENTITY_ID: self.get_all_zones(),
            ATTR_ACTIVE: self.get_default_zones(),
            ATTR_AVAILABLE: self.get_all_zones(),
            ATTR_DEFAULT: self.get_default_zones(),
        }
        return dict(final_dict)

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        """Return the state attributes of the sensor."""
        return self._get_extra_state_attributes()

    @property
    def state(self) -> MediaPlayerState | None:
        """Return the state of the device."""
        return self._get_state_value_for_zone(self.main_zone_entity)

    async def _async_turn_on(self, zones=None) -> None:
        """Turn on media player."""
        if not zones:
            zones = self.default_zones
        # FIXME: check entity values instead of pausing
        i = 0
        for entity in zones:
            sleep_time = self.other_zone_on_delay_seconds
            if i == 0:
                sleep_time = 0
            _LOGGER.debug("Turning on iteration i %s will wait for: %s", i, sleep_time)
            await asyncio.sleep(sleep_time)
            await self.hass.services.async_call(
                MEDIA_PLAYER_DOMAIN,
                SERVICE_TURN_ON,
                {},
                blocking=True,
                target={ATTR_ENTITY_ID: entity},
                context=self._context,
            )
            i += 1

    async def async_turn_on(self) -> None:
        """Turn on media player."""
        await self._async_turn_on(zones=self.default_zones)

    async def _async_turn_off(self, zones=None) -> None:
        """Turn off media player."""
        if not zones:
            zones = self.default_zones
        await self.hass.services.async_call(
            MEDIA_PLAYER_DOMAIN,
            SERVICE_TURN_OFF,
            {},
            blocking=True,
            target={ATTR_ENTITY_ID: zones},
            context=self._context,
        )

    async def async_turn_off(self) -> None:
        """Turn off media player."""
        await self._async_turn_off(zones=self.default_zones)

    async def _async_volume_up(self, zones=None) -> None:
        """Volume up the media player."""
        if not zones:
            zones = self.default_zones
        await self.hass.services.async_call(
            MEDIA_PLAYER_DOMAIN,
            SERVICE_VOLUME_UP,
            {},
            blocking=True,
            target={ATTR_ENTITY_ID: zones},
            context=self._context,
        )

    async def async_volume_up(self) -> None:
        """Volume up the media player."""
        await self._async_volume_up(zones=self.default_zones)

    async def _async_volume_down(self, zones=None) -> None:
        """Volume down the media player."""
        if not zones:
            zones = self.default_zones
        await self.hass.services.async_call(
            MEDIA_PLAYER_DOMAIN,
            SERVICE_VOLUME_DOWN,
            {},
            blocking=True,
            target={ATTR_ENTITY_ID: zones},
            context=self._context,
        )

    async def async_volume_down(self) -> None:
        """Volume down the media player."""
        await self._async_volume_down(zones=self.default_zones)

    async def _async_set_volume_level(self, volume: float, zones=None) -> None:
        """Set volume level, range 0..1."""
        if not zones:
            zones = self.default_zones
        await self.hass.services.async_call(
            MEDIA_PLAYER_DOMAIN,
            SERVICE_VOLUME_SET,
            {ATTR_MEDIA_VOLUME_LEVEL: volume},
            blocking=True,
            target={ATTR_ENTITY_ID: zones},
            context=self._context,
        )

    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        await self._async_set_volume_level(volume, zones=self.default_zones)

    async def _async_mute_volume(self, mute: bool, zones=None) -> None:
        """Mute the volume."""
        if not zones:
            zones = self.default_zones
        await self.hass.services.async_call(
            MEDIA_PLAYER_DOMAIN,
            SERVICE_VOLUME_MUTE,
            {ATTR_MEDIA_VOLUME_MUTED: mute},
            blocking=True,
            target={ATTR_ENTITY_ID: zones},
            context=self._context,
        )

    async def async_mute_volume(self, mute: bool) -> None:
        """Mute the volume."""
        await self._async_mute_volume(mute, zones=self.default_zones)

    async def _async_select_source(self, source: str, zones=None) -> None:
        """Select input source."""
        if not zones:
            zones = self.default_zones
        await self.hass.services.async_call(
            MEDIA_PLAYER_DOMAIN,
            SERVICE_SELECT_SOURCE,
            {ATTR_INPUT_SOURCE: source},
            blocking=True,
            target={ATTR_ENTITY_ID: zones},
            context=self._context,
        )

    async def async_select_source(self, source: str) -> None:
        """Select input source."""
        await self._async_select_source(source, zones=self.default_zones)

    async def _async_select_sound_mode(self, sound_mode: str, zones=None) -> None:
        """Select sound mode."""
        if not zones:
            zones = self.default_zones
        await self.hass.services.async_call(
            MEDIA_PLAYER_DOMAIN,
            SERVICE_SELECT_SOUND_MODE,
            {ATTR_SOUND_MODE: sound_mode},
            blocking=True,
            target={ATTR_ENTITY_ID: zones},
            context=self._context,
        )

    async def async_select_sound_mode(self, sound_mode: str) -> None:
        """Select sound mode."""
        await self._async_select_sound_mode(sound_mode, zones=self.default_zones)

    def _get_zone_entities(self, call_data, default_value=None):
        # TODO: handle default better
        if default_value is None:
            default_value = self.zone_keys
        zones = call_data.get(ATTR_ZONES, default_value)
        _LOGGER.debug("_get_zones zones: %s", zones)
        final_zones = []
        for zone in zones:
            zone_entity = self.zones[zone]
            final_zones.append(zone_entity)
        return list(final_zones)

    def _get_off_zone_entities(self, call_data):
        # TODO: handle default better
        zones = call_data.get(ATTR_OFF_ZONES, [])
        _LOGGER.debug("_get_off_zones zones: %s", zones)
        if zones and not isinstance(zones, list):
            zones = list(zones)
        final_zones = []
        for zone in zones:
            zone_entity = self.zones[zone]
            final_zones.append(zone_entity)
        return list(final_zones)

    def _get_source(self, call_data):
        source = call_data.get(ATTR_INPUT_SOURCE)
        return source

    async def handle_toggle_mute(self, call):
        """Handle the service action call."""
        # FIXME: this doesn't actually work yet
        _LOGGER.debug("handle_toggle_mute call: %s", call)
        zones = self._get_zone_entities(call.data)
        await self._async_mute_volume(True, zones=zones)

    async def handle_volume_up(self, call):
        """Handle the service action call."""
        _LOGGER.debug("handle_volume_up call: %s", call)
        zones = self._get_zone_entities(call.data)
        await self._async_volume_up(zones=zones)

    async def handle_volume_down(self, call):
        """Handle the service action call."""
        _LOGGER.debug("handle_volume_down call: %s", call)
        zones = self._get_zone_entities(call.data)
        await self._async_volume_down(zones=zones)

    async def handle_volume_set(self, call):
        """Handle the service action call."""
        _LOGGER.debug("handle_volume_set call: %s", call)
        zones = self._get_zone_entities(call.data)
        volume_level = call.data.get(ATTR_MEDIA_VOLUME_LEVEL)
        await self._async_set_volume_level(volume_level, zones=zones)

    async def handle_volume_mute(self, call):
        """Handle the service action call."""
        _LOGGER.debug("handle_volume_mute call: %s", call)
        zones = self._get_zone_entities(call.data)
        volume_mute = call.data.get(ATTR_MEDIA_VOLUME_MUTED)
        await self._async_mute_volume(volume_mute, zones=zones)

    async def handle_toggle_power(self, call):
        """Handle the service action call."""
        # FIXME: this doesn't actually work yet
        _LOGGER.debug("handle_toggle_power call: %s", call)
        zones = self._get_zone_entities(call.data)
        await self._async_mute_volume(True, zones=zones)

    async def handle_turn_on(self, call):
        """Handle the service action call."""
        _LOGGER.debug("handle_turn_on call: %s", call)
        zones = self._get_zone_entities(call.data)
        await self._async_turn_on(zones=zones)

    async def handle_turn_off(self, call):
        """Handle the service action call."""
        _LOGGER.debug("handle_turn_off call: %s", call)
        zones = self._get_zone_entities(call.data)
        await self._async_turn_off(zones=zones)

    async def handle_turn_on_with_source(self, call):
        """Handle the service action call."""
        _LOGGER.debug("handle_turn_on_with_source call: %s", call)
        zones = self._get_zone_entities(call.data)
        source = self._get_source(call.data)
        await self._async_turn_on(zones=zones)
        _LOGGER.debug(
            "handle_turn_on_with_source call: %s turned on, now set source", call
        )
        await self._async_select_source(source, zones=zones)

    async def handle_configure_zones_with_source(self, call):
        """Handle the service action call."""
        _LOGGER.debug("handle_configure_zones_with_source call: %s", call)
        on_zones = self._get_zone_entities(call.data, default_value=[])
        off_zones = self._get_off_zone_entities(call.data)
        if on_zones:
            _LOGGER.debug(
                "handle_configure_zones_with_source call: %s found on_zones", call
            )
            await self._async_turn_on(zones=on_zones)
            source = self._get_source(call.data)
            _LOGGER.debug(
                "handle_configure_zones_with_source call: %s turned on, now set source: %s",
                call,
                source,
            )
            await self._async_select_source(source, zones=on_zones)
        if off_zones:
            _LOGGER.debug(
                "handle_configure_zones_with_source call: %s found off_zones", call
            )
            await self._async_turn_off(zones=off_zones)
        _LOGGER.debug(
            "handle_configure_zones_with_source call: %s is now all done", call
        )

    async def handle_select_source(self, call):
        """Handle the service action call."""
        _LOGGER.debug("handle_select_source call: %s", call)
        zones = self._get_zone_entities(call.data)
        source = self._get_source(call.data)
        await self._async_select_source(source, zones=zones)

    async def handle_select_sound_mode(self, call):
        """Handle the service action call."""
        _LOGGER.debug("handle_select_sound_mode call: %s", call)
        zones = self._get_zone_entities(call.data)
        sound_mode = call.data.get(ATTR_SOUND_MODE)
        await self._async_select_sound_mode(sound_mode, zones=zones)

    def async_register_hass_custom_actions(self, hass):
        """Register all the custom service actions."""
        hass.services.async_register(
            DOMAIN, SERVICE_TOGGLE_VOLUME_MUTE, self.handle_toggle_mute
        )
        hass.services.async_register(DOMAIN, SERVICE_VOLUME_UP, self.handle_volume_up)
        hass.services.async_register(
            DOMAIN, SERVICE_VOLUME_DOWN, self.handle_volume_down
        )
        hass.services.async_register(DOMAIN, SERVICE_VOLUME_SET, self.handle_volume_set)
        hass.services.async_register(
            DOMAIN, SERVICE_VOLUME_MUTE, self.handle_volume_mute
        )
        hass.services.async_register(DOMAIN, SERVICE_TURN_ON, self.handle_turn_on)
        hass.services.async_register(
            DOMAIN, SERVICE_TURN_ON_WITH_SOURCE, self.handle_turn_on_with_source
        )
        hass.services.async_register(
            DOMAIN,
            SERVICE_CONFIGURE_ZONES_WITH_SOURCE,
            self.handle_configure_zones_with_source,
        )
        hass.services.async_register(DOMAIN, SERVICE_TURN_OFF, self.handle_turn_off)
        hass.services.async_register(
            DOMAIN, SERVICE_TOGGLE_POWER, self.handle_toggle_power
        )
        hass.services.async_register(
            DOMAIN, SERVICE_SELECT_SOURCE, self.handle_select_source
        )
        hass.services.async_register(
            DOMAIN, SERVICE_SELECT_SOUND_MODE, self.handle_select_sound_mode
        )
