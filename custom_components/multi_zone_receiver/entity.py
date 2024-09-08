"""MultiZoneReceiverEntity class"""
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .const import NAME
from .const import VERSION


class MultiZoneReceiverEntity(Entity):
    def __init__(self, config_entry):
        super().__init__()
        self.config_entry = config_entry

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
