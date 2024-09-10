"""
Custom integration to integrate Multi Zone Receiver with Home Assistant.

For more details about this integration, please refer to
https://github.com/jzucker2/multi-zone-receiver
"""

import asyncio
from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import Config, HomeAssistant

from .const import (
    CONF_ZONE_1,
    CONF_ZONE_2,
    CONF_ZONE_3,
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)

# The type alias needs to be suffixed with 'ConfigEntry'
type MultiZoneReceiverConfigEntry = ConfigEntry[MultiZoneReceiverData]


@dataclass
class MultiZoneReceiverData:
    name: str
    zones: dict[str, Any]

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
        return cls(name=name, zones=zones_dict)

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
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    # Assign the runtime_data
    entry.runtime_data = MultiZoneReceiverData.from_entry(entry)

    # https://developers.home-assistant.io/blog/2024/03/13/deprecate_add_run_job
    hass.async_add_job(hass.config_entries.async_forward_entry_setups(entry, PLATFORMS))

    entry.add_update_listener(async_reload_entry)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
