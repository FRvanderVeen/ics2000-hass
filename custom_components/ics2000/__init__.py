""" The KlikAanKlinUit integration """
from __future__ import annotations

import logging

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.LIGHT,
    Platform.SENSOR
]

async def async_setup_entry(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up KlikAanKlikUit (ICS2000) from a config entry."""
    _LOGGER.debug("Setting up KlikAanKlikUit (ICS2000) entry")

    await hass.config_entries.async_forward_entry_setups(config, PLATFORMS)
    
    return True
