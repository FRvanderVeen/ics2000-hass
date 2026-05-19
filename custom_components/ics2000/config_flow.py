"""Config flow for the ICS2000 integration"""
from __future__ import annotations
from typing import Any

from ics2000_python.Core import CoreException, Hub
import voluptuous as vol

from homeassistant.config_entries import _LOGGER, ConfigFlow, ConfigFlowResult, HomeAssistant
from homeassistant.const import CONF_PASSWORD, CONF_MAC, CONF_EMAIL#, CONF_IP_ADDRESS
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, CONF_SLEEP, CONF_TRIES, SLEEP_DEFAULT, TRIES_DEFAULT

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_MAC): cv.string,
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_TRIES, default=TRIES_DEFAULT): cv.positive_int,
    vol.Optional(CONF_SLEEP, default=SLEEP_DEFAULT): cv.positive_int
    # vol.Optional(CONF_IP_ADDRESS): cv.matches_regex(r'[1-9][0-9]{0,2}(\.(0|[1-9][0-9]{0,2})){2}\.[1-9][0-9]{0,2}'),
    # vol.Optional(CONF_AES): cv.matches_regex(r'[a-zA-Z0-9]{32}')
})

async def _validate_input(hass: HomeAssistant, data: dict[str, Any]) -> bool:
    """Validate the user input allows us to connect to the hub."""

    def _create_hub():
        return Hub(
            data[CONF_MAC],
            data[CONF_EMAIL],
            data[CONF_PASSWORD],
        )

    return await hass.async_add_executor_job(_create_hub)

class ICS2000ConfigFlow(ConfigFlow, domain=DOMAIN):
    """ICS2000 config flow."""
    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                hub = await _validate_input(self.hass, user_input)
            except CoreException as ce:
                _LOGGER.error(f'Error validating user input: {ce}')
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(f'kaku-{hub.mac}')
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=hub.mac, data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle reconfiguration of the integration."""
        errors: dict[str, str] = {}
        reconf_entry = self._get_reconfigure_entry()
        suggested_values = {
            CONF_MAC: reconf_entry.data[CONF_MAC],
            CONF_EMAIL: reconf_entry.data[CONF_EMAIL],
            CONF_PASSWORD: reconf_entry.data[CONF_PASSWORD],
            CONF_TRIES: reconf_entry.data.get(CONF_TRIES, TRIES_DEFAULT),
            CONF_SLEEP: reconf_entry.data.get(CONF_SLEEP, SLEEP_DEFAULT)
            #CONF_IP_ADDRESS: reconf_entry.data[CONF_IP_ADDRESS]
            #CONF_AES: reconf_entry.data[CONF_AES]
        }

        if user_input:
            try:
                hub = await _validate_input(self.hass, data={
                        **reconf_entry.data,
                        **user_input,
                    }
                )
            except CoreException as ce:
                _LOGGER.error(f'Error validating user input: {ce}')
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(f'kaku-{hub.mac}')
                self._abort_if_unique_id_mismatch()
                return self.async_update_reload_and_abort(
                    reconf_entry,
                    data_updates={
                        CONF_MAC: user_input[CONF_MAC],
                        CONF_EMAIL: user_input[CONF_EMAIL],
                        CONF_PASSWORD: user_input[CONF_PASSWORD],
                        CONF_TRIES: user_input[CONF_TRIES],
                        CONF_SLEEP: user_input[CONF_SLEEP]
                        #CONF_IP_ADDRESS: user_input[CONF_IP_ADDRESS]
                        #CONF_AES: user_input[CONF_AES]
                    },
                )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self.add_suggested_values_to_schema(
                data_schema=STEP_USER_DATA_SCHEMA,
                suggested_values=user_input or suggested_values
            ),
            errors=errors
        )

    async def async_step_import(self, import_config: dict[str, Any]) -> ConfigFlowResult:
        """Handle import from YAML `configuration.yaml`."""

        return await self.async_step_user(import_config)
