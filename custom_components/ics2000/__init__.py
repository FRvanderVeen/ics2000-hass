""" The KlikAanKlinUit integration """
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry, ConfigType, SOURCE_IMPORT
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.LIGHT
]

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the integration from YAML config by importing to a config entry.

    If the user has YAML configuration for this integration, start an import
    flow so the config is migrated to a Config Entry.
    """

    # If already configured, don't do anything
    if hass.config_entries.async_entries(DOMAIN):
        return True

    entries: list[dict[str, Any]] = []

    conf = config.get(DOMAIN)
    if conf is not None:
        entries.extend(conf if isinstance(conf, list) else [conf])

    legacy_light_config = config.get(Platform.LIGHT)
    if legacy_light_config is not None:
        for platform_config in legacy_light_config:
            if platform_config.get("platform") != DOMAIN:
                continue

            legacy_entry = {**platform_config}
            legacy_entry.pop("platform", None)
            entries.append(legacy_entry)

    if not entries:
        return True

    for entry in entries:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": SOURCE_IMPORT},
                data=entry,
            )
        )

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up KlikAanKlikUit (ICS2000) from a config entry."""
    _LOGGER.debug("Setting up KlikAanKlikUit (ICS2000) entry")

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True
