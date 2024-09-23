"""MultiZoneReceiverEntity class"""

import logging

from homeassistant.components.media_player import (
    ATTR_INPUT_SOURCE,
    ATTR_MEDIA_VOLUME_LEVEL,
    MediaPlayerState,
)
from homeassistant.core import Event, EventStateChangedData, callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_state_change_event

from .const import DOMAIN, NAME, VERSION

_LOGGER: logging.Logger = logging.getLogger(__package__)


class MultiZoneReceiverEntity(Entity):
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, config_entry):
        super().__init__()
        self.config_entry = config_entry

    async def async_added_to_hass(self) -> None:
        """Entity has been added to hass."""
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                # TODO: reduce for specific zone entities below
                self.get_all_zones(),
                self.async_update_media_player_state_callback,
            )
        )

    @property
    def updateable_states(self):
        return list(
            [
                MediaPlayerState.ON,
                MediaPlayerState.OFF,
                MediaPlayerState.PLAYING,
                MediaPlayerState.IDLE,
            ]
        )

    @callback
    def async_update_media_player_state_callback(
        self, event: Event[EventStateChangedData]
    ) -> None:
        """Handle media_player state changes."""
        new_state = event.data.get("new_state")
        entity = event.data.get("entity_id")
        _LOGGER.debug("New state from '%s': '%s'", entity, str(new_state))

        # zone = self._zones[entity]

        # if new_state.state is None:
        #     self._update_zones(zone, False)
        #     self.async_write_ha_state()
        #     return

        # self._update_zones(zone, new_state.state in self.updateable_states)
        self.async_write_ha_state()

    @property
    def runtime_data(self):
        return self.config_entry.runtime_data

    @property
    def config_entry_id(self):
        return self.config_entry.entry_id

    @property
    def unique_id_base(self):
        """Return the first half of ID to use for this entity."""
        return self.config_entry_id

    @property
    def unique_id_suffix(self):
        """Return a second half of ID to use for this entity."""
        return "base"

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.unique_id_base}{self.unique_id_suffix}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.config_entry_id)},
            "name": NAME,
            "model": VERSION,
            "manufacturer": NAME,
        }

    def get_main_zone(self):
        return self.runtime_data.get_main_zone()

    def get_main_zone_display_name(self):
        return self.runtime_data.get_main_zone_display_name()

    @property
    def main_zone_name(self):
        return self.get_main_zone_display_name()

    @property
    def zone_name(self):
        return self.main_zone_name

    @property
    def main_zone_entity(self):
        return self.get_main_zone()

    def get_zones(self):
        return self.runtime_data.zones

    @property
    def zone_keys(self):
        return self.get_zones().keys()

    @property
    def zones(self):
        return self.get_zones()

    def get_all_zones(self):
        return self.runtime_data.get_all_zones()

    def get_default_zones(self):
        return self.get_all_zones()

    @property
    def default_zones(self):
        return self.get_default_zones()

    def _get_state_value_for_zone(self, zone_entity) -> MediaPlayerState | None:
        """Return the state of the device."""
        state = self.hass.states.get(zone_entity)
        if not state:
            return state
        return state.state

    def _get_volume_level(self, zone_entity) -> float | None:
        state = self.hass.states.get(zone_entity)
        if not state:
            return state
        volume_level = state.attributes[ATTR_MEDIA_VOLUME_LEVEL]
        return volume_level

    def _get_is_on_state_for_zone(self, zone_entity) -> bool:
        current_state = self._get_state_value_for_zone(zone_entity)
        return bool(current_state != MediaPlayerState.OFF)

    def _get_source_for_zone(self, zone_entity) -> str | None:
        """Return the current input source for a zone."""
        state = self.hass.states.get(zone_entity)
        if not state:
            return state
        input_source = state.attributes[ATTR_INPUT_SOURCE]
        return input_source


class MultiZoneReceiverZoneEntity(MultiZoneReceiverEntity):
    def __init__(self, config_entry, zone_key):
        super().__init__(config_entry)
        self._zone_key = zone_key

    @property
    def zone_key(self):
        return self._zone_key

    @property
    def zone_name(self):
        return self._get_zone_display_name(self.zone_key)

    @property
    def zone_safe_name(self):
        return self._get_zone_safe_name(self.zone_key)

    @property
    def zone_entity(self):
        return self._get_zone_entity(self.zone_key)

    def _get_zone_entity(self, zone_key):
        return self.runtime_data._get_zone_entity(zone_key)

    def _get_zone_display_name(self, zone_key):
        return self.runtime_data._get_zone_display_name(zone_key)

    def _get_zone_safe_name(self, zone_key):
        return self.runtime_data._get_zone_safe_name(zone_key)
