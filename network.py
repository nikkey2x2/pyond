import json
import asyncio

from concurrent.futures import ThreadPoolExecutor
from .logic_engine import PyondLogicEngine
from .log import logger

__all__ = ['PyondServer']


class PyondServer:

    def __init__(self, world, threads_num=5,
                 logic_engine=PyondLogicEngine,
                 threads_executor=ThreadPoolExecutor):
        logger.debug("Creating server...")
        self.world = world
        self.ticktime = 1.0 / 10 * world.tick_lag
        self.loop = asyncio.get_event_loop()
        self.coroutine = asyncio.start_server(self._handle_client,
                                              world.address, world.port,
                                              loop=self.loop)
        self.server = self.loop.run_until_complete(self.coroutine)
        self.pool = threads_executor(max_workers=threads_num)
        self.logic = logic_engine(self, world)
        self.clients = []

    def start(self):
        logger.info("Starting server...")
        self.ticks_task = self.loop.create_task(self._send_tick())
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.stop()
        logger.debug("Trying to stop the server...")
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.close()
        logger.info("Server stopped")
        self.world.Del()

    def _next_id(self):
        for i, cl in enumerate(self.clients):
            if cl is None:
                return i
        self.clients.append(None)
        return len(self.clients) - 1

    def _handle_client(self, reader, writer):
        id = self._next_id()
        logger.debug('(NET) New client connected, id: %d' % id)
        self.clients[id] = [writer, {}, reader]
        rh = self.loop.create_task(self._reader_handler(id, reader))

    async def _send_tick(self):
        self.tick = 0
        logger.debug('Ticks started')
        while True:
            self.loop.run_in_executor(self.pool, self._send_all)
            await asyncio.sleep(self.ticktime)
            self.tick += 1

    def send(self, id, data):
        if self.clients[id] is not None:
            self.clients[id][1].update(data)

    def disconnect(self, id):
        if self.clients[id] is not None:
            self.clients[id][2].feed_eof()

    async def _reader_handler(self, id, reader):
        alldata = b''
        while True:
            data = await reader.read(100)
            if reader.at_eof():
                self.clients[id] = None
                self.logic.disconnect(id)
                break
            alldata = b''.join((alldata, data))
            if not alldata.endswith(b'}'):
                continue
            try:
                json_data = json.loads(alldata.decode())
            except:
                logger.debug('(NET) Got wrong json-load')
                continue
            logger.debug('(NET) Received packet from %i' % id)
            self.loop.run_in_executor(self.pool, self.logic.receive,
                                      id, json_data)
            alldata = b''

    def _send_all(self):
        for cl in self.clients:
            if cl is None:
                continue
            data = cl[1]
            if not data:
                continue
            data = bytes(json.dumps(data), 'utf-8')
            cl[1].clear()
            cl[0].write(data)
            self.loop.create_task(cl[0].drain())
