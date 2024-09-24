"""
Custom integration to integrate Multi Zone Receiver with Home Assistant.

For more details about this integration, please refer to
https://github.com/jzucker2/multi-zone-receiver
"""

from dataclasses import dataclass
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.reload import async_setup_reload_service

from .const import (
    CONF_OTHER_ZONE_ON_DELAY_SECONDS,
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


class ZoneException(Exception):
    pass


@dataclass
class Zone:
    zone_key: str
    zone_number: int
    zone_entity: str
    volume_step: float

    @classmethod
    def from_input_dict(cls, zone_key: str, zone_number: int, input_dict: dict):
        volume_step = input_dict[CONF_VOLUME_STEP]
        zone_entity = input_dict[zone_key]
        return cls(
            zone_key=zone_key,
            zone_number=zone_number,
            zone_entity=zone_entity,
            volume_step=volume_step,
        )

    @property
    def zone_name(self):
        if self.zone_key == CONF_ZONE_1:
            return "Main"
        elif self.zone_key == CONF_ZONE_2:
            return "Zone 2"
        elif self.zone_key == CONF_ZONE_3:
            return "Zone 3"
        raise ZoneException(f"invalid zone ({self})")

    @classmethod
    def _make_safe_zone_name(self, zone_key):
        return zone_key.replace(" ", "_").replace("-", "_").lower()

    def _get_safe_zone_name(self):
        return self._make_safe_zone_name(self.zone_key)

    @property
    def safe_zone_name(self):
        return self._get_safe_zone_name()


@dataclass
class MultiZoneReceiverData:
    name: str
    volume_step: float
    other_zone_on_delay_seconds: float
    all_zones: dict[str, Zone]
    zone_keys: list[str]

    @classmethod
    def from_entry(cls, entry: MultiZoneReceiverConfigEntry):
        _LOGGER.debug(
            "Processing data config entry: %s with entry.data: %s", entry, entry.data
        )
        name = entry.data.get(CONF_NAME)
        volume_step = entry.data.get(CONF_VOLUME_STEP)
        other_zone_on_delay_seconds = entry.data.get(CONF_OTHER_ZONE_ON_DELAY_SECONDS)
        zone_input_data = dict(entry.data)
        all_zones_dict = {
            CONF_ZONE_1: Zone.from_input_dict(CONF_ZONE_1, 1, zone_input_data),
            CONF_ZONE_2: Zone.from_input_dict(CONF_ZONE_2, 2, zone_input_data),
            CONF_ZONE_3: Zone.from_input_dict(CONF_ZONE_3, 3, zone_input_data),
        }
        zone_keys = [
            CONF_ZONE_1,
            CONF_ZONE_2,
            CONF_ZONE_3,
        ]
        return cls(
            name=name,
            volume_step=volume_step,
            other_zone_on_delay_seconds=other_zone_on_delay_seconds,
            all_zones=all_zones_dict,
            zone_keys=zone_keys,
        )

    def _get_zone_entity(self, zone_key):
        return self.all_zones[zone_key].zone_entity

    def _get_zone_display_name(self, zone_key):
        return self.all_zones[zone_key].zone_name

    def _get_zone_safe_name(self, zone_key):
        return self.all_zones[zone_key].safe_zone_name

    @property
    def zones(self):
        return dict(
            {
                CONF_ZONE_1: self._get_zone_entity(CONF_ZONE_1),
                CONF_ZONE_2: self._get_zone_entity(CONF_ZONE_2),
                CONF_ZONE_3: self._get_zone_entity(CONF_ZONE_3),
            }
        )

    def get_main_zone(self):
        return self._get_zone_entity(CONF_ZONE_1)

    @property
    def main_zone_key(self):
        return CONF_ZONE_1

    def get_main_zone_display_name(self):
        return self._get_zone_display_name(CONF_ZONE_1)

    def get_all_zones_list(self):
        return list(self.all_zones.values())

    def get_all_zones(self):
        return list([z.zone_entity for z in self.get_all_zones_list()])


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
