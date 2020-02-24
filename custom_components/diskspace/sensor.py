"""Sensor platform for Local Diskspace"""
import datetime
import logging
import shutil

import homeassistant.helpers.config_validation as cv
import voluptuous as vol 
from homeassistant.components.sensor import PLATFORM_SCHEMA 
from homeassistant.const import CONF_NAME, CONF_ICON 
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

__version__ = "v0.1"
_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = []

CONF_PATH = "path"
CONF_UOM = "unit_of_measure"

DEFAULT_UOM = "GB"
DEFAULT_ICON = "mdi:harddisk"
DEFAULT_PATH = "/"

MIN_TIME_BETWEEN_UPDATES = datetime.timedelta(seconds=60)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_PATH, default=DEFAULT_PATH): cv.string,
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_ICON, default=DEFAULT_ICON): cv.string,
        vol.Required(CONF_UOM, default=DEFAULT_UOM): cv.string,
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    "Setup Platform"
    add_entities(
        [
            DiskSpaceSensor(
                name=config[CONF_NAME],
                path=config[CONF_PATH],
                icon=config[CONF_ICON],
                uom=config[CONF_UOM],
            )
        ]
    )

class DiskSpaceSensor(Entity):
    def __init__(self, name: str, path: str, icon: str, uom: str):
        self._state = None
        self._icon = icon
        self._attributes = {}
        self._path = path
        self._uom = uom
        self._name = name

    @property
    def name(self):
        return "Disk Space " + self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return self._icon

    @property
    def state_attributes(self):
        return self._attributes

    @property
    def unit_of_measurement(self):
        return self._uom

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        self._attributes = {}
        self._state = 0

        try:
            total, used, free = shutil.disk_usage(self._path)
        except Exception as err:
            _LOGGER.warning("Other Error: %s", err)

        if self._uom == "GB":
            self._attributes["total"] = total // (10 ** 9)
            self._attributes["used"] = used // (10 ** 9)
            self._attributes["free"] = free // (10 ** 9)
        elif self._uom == "MB":
            self._attributes["total"] = total // (10 ** 6)
            self._attributes["used"] = used // (10 ** 6)
            self._attributes["free"] = free // (10 ** 6)
        elif self._uom == "TB":
            self._attributes["total"] = total // (10 ** 12)
            self._attributes["used"] = used // (10 ** 12)
            self._attributes["free"] = free // (10 ** 12)
        else:
            self._attributes["total"] = total
            self._attributes["used"] = used
            self._attributes["free"] = free

        self._attributes["percentage_free"] = round((free / total) * 100, 1)
        self._state = self._attributes["free"]
