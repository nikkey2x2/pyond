import sys
from .log import logger
from .basic_objects import PyondClient

__all__ = ['PyondLogicEngine']


class PyondLogicEngine:

    def __init__(self, server, world):
        self.server = server
        self.clients = {}
        self.world = world
        self.lp = {'nikkey2x2': ['322', 1], 'or': ['not', 0]}
        self.packet_types = {'verb': self.verb,
                             'login': self.login,
                             'logout': self.logout}

    def get_client(self, id):
        return self.clients.get(id)

    def receive(self, id, data):
        if data['t'] in self.packet_types:
            if (data['t'] != 'login') and (self.clients.get(id) is None):
                return
            self.packet_types[data['t']](id, data)

    def send(self, id, data):
        self.server.send(id, data)

    def login(self, id, data):
        if ('l' in data) and ('p' in data):
            if data['l'] in self.lp:
                if data['p'] == self.lp[data['l']][0]:
                    new_client = self.world.get_class('Client', PyondClient)()
                    new_client.key = data['l']
                    new_client.New()
                    self.clients[id] = new_client
                    self.send(id, {'t': 'login', 'r': True})
                    logger.debug('(LOGIC) New client: %r' % data['l'])
                else:
                    self.send(id, {'t': 'login', 'r': False})

    def logout(self, id, data):
        self.server.disconnect(id)

    def verb(self, id, data):
        if ('n' in data):
            self.server.send({data['n']: 'got it'})

    def disconnect(self, id):
        logger.debug('(LOGIC) Disconnect, id: %i' % id)
        self.clients[id].Del()
        del self.clients[id]
