""" The KlikAanKlinUit integration """
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.LIGHT
]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up KlikAanKlikUit (ICS2000) from a config entry."""
    _LOGGER.debug("Setting up KlikAanKlikUit (ICS2000) entry")

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True
