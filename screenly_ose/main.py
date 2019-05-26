# -*- coding: utf-8 -*-

"""Main module."""

import logging
import time

import aiohttp
import async_timeout

from .const import (
    ACCEPT_ENCODING,
    ACCEPT_HEADER,
    HTTP_OK,
    NEXT_ASSET,
    PREVIOUS_ASSET,
    SWITCH_ASSET,
    CURRENT_ASSET,
    TIMEOUT_TIMES
)

_LOGGER = logging.getLogger(__name__)

class Screenly:
    """
    Screenly API class.
    Control your digital signage with Python.
    """

    def __init__(self, websession, host, port=80, encryption=False, timeout=None):
        """
        Screenly OSE controller.
        :param str host:        Hostname or IP address of device.
        :param int port:        Port to connect to. Default 80.
        :param bool encryption: Use SSL encryption when connecting.
        :param timeout:         Timeout to use for API requests.
        """
        self._host = host
        self._port = port
        self._encryption = encryption
        self._timeout = timeout
        http_proto = 'https' if self._encryption else 'http'
        self._http_url = '{http_proto}://{host}:{port}/api'.format(
            http_proto=http_proto,
            host=self._host,
            port=self._port)
        self._headers = {
            "Accept-Encoding": ACCEPT_ENCODING,
            "Accept": ACCEPT_HEADER
        }
        self.websession = websession

    async def get_current_asset(self):
        """Query the device for the asset currently being displayed."""
        response = await self.send_request(CURRENT_ASSET)

        if not response:
            return False
        try:
            return response['asset_id']
        except KeyError:
            return False

    async def next_asset(self):
        """Request the device to display the next asset."""
        response = await self.send_request(NEXT_ASSET)
        return bool(response)

    async def previous_asset(self):
        """Request the device to display the previous asset."""
        response = await self.send_request(PREVIOUS_ASSET)
        return bool(response)

    async def switch_asset(self, asset_id):
        """Request the device to display the specified asset."""
        response = await self.send_request(SWITCH_ASSET.format(id=asset_id))
        return bool(response)

    async def send_request(self, endpoint, params=None, version='v1'):
        """Send request to Screenly."""
        try:
            url = '{url}/{version}/{endpoint}'.format(
                url=self._http_url,
                version=version,
                endpoint=endpoint
            )

            _LOGGER.debug("Sending request to endpoint %s", url)

            async with self.websession.get(url=url, params=params, headers=self._headers, timeout=self._timeout) as response:
                if response.status == HTTP_OK:
                    return await response.json()
                else:
                    _LOGGER.warning("Error %d from Screenly.", response.status)
                    return False

        except (aiohttp.ClientError, aiohttp.ClientConnectionError) as e:
            _LOGGER.exception(e)
            return False

    def __get_timeout(self, endpoint):
        if endpoint in TIMEOUT_TIMES:
            return TIMEOUT_TIMES[endpoint]
        else:
            return TIMEOUT_TIMES['default']