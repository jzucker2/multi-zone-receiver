"""MultiZoneReceiverEntity class"""

from homeassistant.components.media_player import (
    ATTR_INPUT_SOURCE,
    ATTR_MEDIA_VOLUME_LEVEL,
    MediaPlayerState,
)
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, NAME, VERSION


class MultiZoneReceiverEntity(Entity):
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, config_entry):
        super().__init__()
        self.config_entry = config_entry

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

    @property
    def main_zone_entity(self):
        return self.get_main_zone()

    def get_zones(self):
        return self.runtime_data.zones

    @property
    def zone_names(self):
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
