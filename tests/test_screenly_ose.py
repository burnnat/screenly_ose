#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `screenly_ose` package."""

import logging
import json

import pytest
import asyncio
import aiohttp

from screenly_ose import Screenly

_LOGGER = logging.getLogger(__name__)

# CaseControlledTestServer originally written by Julien Hartmann
# Licensed under CC Attribution 4.0 International License
# See https://solidabstractions.com/2018/testing-aiohttp-client
class CaseControlledTestServer(aiohttp.test_utils.RawTestServer):
    def __init__(self, **kwargs):
        super().__init__(self._handle_request, **kwargs)
        self._requests = asyncio.Queue()
        self._responses = {}

    async def close(self):
        """ Cancel all pending requests before closing. """
        for future in self._responses.values():
            future.cancel()
        await super().close()

    async def _handle_request(self, request):
        """ Push request to test case and wait until it provides a response. """
        self._responses[id(request)] = response = asyncio.Future()
        self._requests.put_nowait(request)
        try:
            return await response
        finally:
            del self._responses[id(request)]

    async def receive_request(self):
        """ Wait until test server receives a request. """
        return await self._requests.get()

    def send_response(self, request, *args, **kwargs):
        """ Send web response from test case to client code. """
        response = aiohttp.web.Response(*args, **kwargs)
        self._responses[id(request)].set_result(response)

@pytest.mark.asyncio
async def test_list_assets():
    async with CaseControlledTestServer() as server, aiohttp.ClientSession() as websession:
        loop = asyncio.get_event_loop()
        await server.start_server(loop)

        screenly = Screenly(websession, 'localhost', port=server.port)
        task = loop.create_task(screenly.list_assets())

        request = await server.receive_request()
        assert request.method == 'GET'
        assert request.path_qs == '/api/v1.2/assets'

        result = []

        item_a = {}
        item_a['asset_id'] = "572a7750ed0e4d74b757e1cd36e343b7"
        item_a['mimetype'] = "webpage"
        item_a['name'] = "Hacker News"
        item_a['end_date'] = "2025-04-27T09:42:00+00:00"
        item_a['is_enabled'] = 1
        item_a['nocache'] = 0
        item_a['is_active'] = 1
        item_a['uri'] = "https://news.ycombinator.com"
        item_a['skip_asset_check'] = 0
        item_a['duration'] = 30
        item_a['play_order'] = 1
        item_a['start_date'] = "2019-04-27T09:42:00+00:00"
        item_a['is_processing'] = 0
        result.append(item_a)

        item_b = {}
        item_b['asset_id'] = "71ac3c6270d74b8f952eca5a0d5f8f3d"
        item_b['mimetype'] = "webpage"
        item_b['name'] = "Google"
        item_b['end_date'] = "2025-04-29T10:06:00+00:00"
        item_b['is_enabled'] = 1
        item_b['nocache'] = 0
        item_b['is_active'] = 0
        item_b['uri'] = "https://www.google.com"
        item_b['skip_asset_check'] = 0
        item_b['duration'] = 30
        item_b['play_order'] = 2
        item_b['start_date'] = "2019-04-29T10:06:00+00:00"
        item_b['is_processing'] = 0
        result.append(item_b)

        server.send_response(request, content_type='application/json', text=json.dumps(result))

        response = await task

        asset = response[0]
        assert asset['id'] == item_a['asset_id']
        assert asset['name'] == item_a['name']
        assert asset['type'] == item_a['mimetype']
        assert asset['enabled'] == True
        assert asset['active'] == True

        asset = response[1]
        assert asset['id'] == item_b['asset_id']
        assert asset['name'] == item_b['name']
        assert asset['type'] == item_b['mimetype']
        assert asset['enabled'] == True
        assert asset['active'] == False

@pytest.mark.asyncio
async def test_get_current_asset():
    async with CaseControlledTestServer() as server, aiohttp.ClientSession() as websession:
        loop = asyncio.get_event_loop()
        await server.start_server(loop)

        screenly = Screenly(websession, 'localhost', port=server.port)
        task = loop.create_task(screenly.get_current_asset())

        request = await server.receive_request()
        assert request.method == 'GET'
        assert request.path_qs == '/api/v1/viewer_current_asset'

        result = {}
        result['asset_id'] = "572a7750ed0e4d74b757e1cd36e343b7"
        result['mimetype'] = "webpage"
        result['name'] = "Hacker News"
        result['end_date'] = "2025-04-27T09:42:00+00:00"
        result['is_enabled'] = 1
        result['nocache'] = 0
        result['is_active'] = 1
        result['uri'] = "https://news.ycombinator.com"
        result['skip_asset_check'] = 0
        result['duration'] = 30
        result['play_order'] = 1
        result['start_date'] = "2019-04-27T09:42:00+00:00"
        result['is_processing'] = 0
        server.send_response(request, content_type='application/json', text=json.dumps(result))

        asset = await task
        assert asset['id'] == result['asset_id']
        assert asset['name'] == result['name']
        assert asset['type'] == result['mimetype']

@pytest.mark.asyncio
async def test_next_asset():
    async with CaseControlledTestServer() as server, aiohttp.ClientSession() as websession:
        loop = asyncio.get_event_loop()
        await server.start_server(loop)

        screenly = Screenly(websession, 'localhost', port=server.port)
        task = loop.create_task(screenly.next_asset())

        request = await server.receive_request()
        assert request.method == 'GET'
        assert request.path_qs == '/api/v1/assets/control/next'

        message = "Asset switched"
        server.send_response(request, content_type='application/json', text=json.dumps(message))

        result = await task
        assert result == True

@pytest.mark.asyncio
async def test_previous_asset():
    async with CaseControlledTestServer() as server, aiohttp.ClientSession() as websession:
        loop = asyncio.get_event_loop()
        await server.start_server(loop)

        screenly = Screenly(websession, 'localhost', port=server.port)
        task = loop.create_task(screenly.previous_asset())

        request = await server.receive_request()
        assert request.method == 'GET'
        assert request.path_qs == '/api/v1/assets/control/previous'

        message = "Asset switched"
        server.send_response(request, content_type='application/json', text=json.dumps(message))

        result = await task
        assert result == True

@pytest.mark.asyncio
async def test_switch_asset():
    async with CaseControlledTestServer() as server, aiohttp.ClientSession() as websession:
        loop = asyncio.get_event_loop()
        await server.start_server(loop)

        screenly = Screenly(websession, 'localhost', port=server.port)
        task = loop.create_task(screenly.switch_asset('7fe4d05e8e4c42e5a827977f750721ea'))

        request = await server.receive_request()
        assert request.method == 'GET'
        assert request.path_qs == '/api/v1/assets/control/asset&7fe4d05e8e4c42e5a827977f750721ea'

        message = "Asset switched"
        server.send_response(request, content_type='application/json', text=json.dumps(message))

        result = await task
        assert result == True