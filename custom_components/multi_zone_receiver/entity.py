"""MultiZoneReceiverEntity class"""

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
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.config_entry_id)},
            "name": NAME,
            "model": VERSION,
            "manufacturer": NAME,
        }
