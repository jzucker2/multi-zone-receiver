"""
Custom integration to integrate Multi Zone Receiver with Home Assistant.

For more details about this integration, please refer to
https://github.com/jzucker2/multi-zone-receiver
"""

from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.reload import async_setup_reload_service

from .const import (
    CONF_VOLUME_STEP,
    CONF_ZONE_1,
    CONF_ZONE_2,
    CONF_ZONE_3,
    DOMAIN,
    PLATFORMS,
)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

_LOGGER: logging.Logger = logging.getLogger(__package__)

# The type alias needs to be suffixed with 'ConfigEntry'
type MultiZoneReceiverConfigEntry = ConfigEntry[MultiZoneReceiverData]


@dataclass
class MultiZoneReceiverData:
    name: str
    zones: dict[str, Any]
    volume_step: float

    @classmethod
    def from_entry(cls, entry: MultiZoneReceiverConfigEntry):
        _LOGGER.debug(
            "Processing data config entry: %s with entry.data: %s", entry, entry.data
        )
        name = entry.data.get(CONF_NAME)
        zone_1 = entry.data.get(CONF_ZONE_1)
        zone_2 = entry.data.get(CONF_ZONE_2)
        zone_3 = entry.data.get(CONF_ZONE_3)
        zones_dict = {
            CONF_ZONE_1: zone_1,
            CONF_ZONE_2: zone_2,
            CONF_ZONE_3: zone_3,
        }
        volume_step = entry.data.get(CONF_VOLUME_STEP)
        return cls(name=name, zones=zones_dict, volume_step=volume_step)

    def get_main_zone(self):
        return self.zones[CONF_ZONE_1]

    def get_all_zones(self):
        return list(self.zones.values())


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MultiZoneReceiverConfigEntry,
):
    """Set up this integration using UI."""
    # if entry.runtime_data is None:
    #     _LOGGER.info(STARTUP_MESSAGE)

    # Assign the runtime_data
    entry.runtime_data = MultiZoneReceiverData.from_entry(entry)

    await async_setup_reload_service(hass, DOMAIN, PLATFORMS)

    # Set up all platforms for this device/entry.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Reload entry when its updated.
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: MultiZoneReceiverConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        _LOGGER.debug(
            "Unloading platforms entry: %s with unload_ok: %s", entry, unload_ok
        )

    return unload_ok


async def async_reload_entry(
    hass: HomeAssistant,
    entry: MultiZoneReceiverConfigEntry,
) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
