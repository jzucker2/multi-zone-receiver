"""Adds config flow for Multi Zone Receiver."""

import asyncio
import logging

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from .const import (
    CONF_VOLUME_STEP,
    CONF_ZONE_1,
    CONF_ZONE_2,
    CONF_ZONE_3,
    DEFAULT_VOLUME_STEP,
    DOMAIN,
    PLATFORMS,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)

# This is the schema that used to display the UI to the user. This simple
# schema has a single required host field, but it could include a number of fields
# such as username, password etc. See other components in the HA core code for
# further examples.
# Note the input displayed to the user will be translated. See the
# translations/<lang>.json file and strings.json. See here for further information:
# https://developers.home-assistant.io/docs/config_entries_config_flow_handler/#translations
# At the time of writing I found the translations created by the scaffold didn't
# quite work as documented and always gave me the "Lokalise key references" string
# (in square brackets), rather than the actual translated value. I did not attempt to
# figure this out or look further into it.
DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_ZONE_1): cv.entity_id,
        vol.Required(CONF_ZONE_2): cv.entity_id,
        vol.Required(CONF_ZONE_3): cv.entity_id,
        # vol.Required(CONF_ZONE_1): cv.entity_domain(MEDIA_PLAYER),
        # vol.Required(CONF_ZONE_2): cv.entity_domain(MEDIA_PLAYER),
        # vol.Required(CONF_ZONE_3): cv.entity_domain(MEDIA_PLAYER),
        # vol.Required(CONF_ZONE_1): str,
        # vol.Required(CONF_ZONE_2): str,
        # vol.Required(CONF_ZONE_3): str,
        vol.Optional(CONF_VOLUME_STEP, default=DEFAULT_VOLUME_STEP): vol.Coerce(float),
    }
)


class MultiZoneReceiverFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for multi_zone_receiver."""

    VERSION = 2

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            valid = await self._test_credentials(user_input)
            if valid:
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )
            else:
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MultiZoneReceiverOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=self._errors,
        )

    async def _test_credentials(self, user_input):
        """Return true if credentials is valid."""
        try:
            # perform a test here
            _LOGGER.debug("Test credentials user_input: %s", user_input)
            await asyncio.sleep(0)
            return True
        except Exception:  # pylint: disable=broad-except
            pass
        return False


class MultiZoneReceiverOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for multi_zone_receiver."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_NAME), data=self.options
        )
