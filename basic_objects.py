import sys
import time
import re

from .constants import *
from .utils import type2class, class2type
from .log import logger

__all__ = ['PyondWorld', 'PyondAtom', 'PyondClient', 'PyondAtom_Movable',
           'PyondTurf', 'PyondObj', 'PyondMob', 'PyondArea']


class PyondObjectMetaclass(type):

    def __call__(self, *args, **kwargs):
        obj = type.__call__(self, *args, **kwargs)
        for i in dir(obj):
            if not i.startswith('_'):
                try:
                    setattr(obj, i, getattr(obj, i).copy())
                except:
                    pass
        return obj


class PyondDatum(metaclass=PyondObjectMetaclass):
    parent_type = '/datum'
    tag = None
    vars = []

    def type(self): return class2type(self.__class__.__name__)

    def New(self, loc=(0, 0, 0)):
        pass

    def Del(self):
        pass

    def Read(self, savefile):
        logger.debug('Datum.Read is not yet implemented')
        raise NotImplementedError

    def Topic(self, href, href_list):
        pass

    def Write(self, savefile):
        logger.debug('Datum.Write is not yet implemented')
        raise NotImplementedError


class PyondAtom(PyondDatum):   # /*/
    name = ''
    gender = 'neuter'  # 'neuter', 'female', 'male', 'plural'
    desc = ''  # Description
    suffix = ''  # Suffix, (weapon in hand)
    icon = ''
    icon_state = ''  # Icon state, door-open | door-closed
    dir = 0  # Face direction
    overlays = []  # Icon-overlays
    underlays = []  # Underlays
    visibility = 1  # Visible?
    luminosity = 0  # light-emitting
    opacity = 0  # blocks light and view if 1
    density = 0  # blocks movement
    contents = []  # Direct contents
    verbs = []  # list of available methods on class, which client can call
    world = None

    x = 0  # x on map
    y = 0  # y on map
    z = 0  # z on map

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__

    def Enter(self, O):   # Density walk-around
        return True

    def Exit(self, O):   # Mobs can't escape if 1
        return False

    def New(loc=(0, 0, 0), *args):
        pass


class PyondAtom_Movable(PyondAtom):

    def Bump(self, atom):
        if isinstance(atom, PyondMob) and (atom in self.group):
            atom.x, self.x = self.x, atom.x
            atom.y, self.y = self.y, atom.y

    def Cross(self, atom_movable):
        if isinstance(atom_movable, PyondMob) and isinstance(self, PyondMob):
            self.Bump(atom_movable)
            return False
        elif atom_movable.density and self.density:
            return False
        else:
            return True

    def Crossed(self, atom):  # Called by Move()
        pass

    def Move(self, NewLoc, Dir=0, step_x=0, step_y=0)
        pass


class PyondArea(PyondAtom):   # /area/
    pass


class PyondTurf(PyondAtom):   # /turf/
    loc = None  # container. (self in self.loc.contents = True)


class PyondObj(PyondAtom_Movable):   # /obj/
    loc = None


class PyondMob(PyondAtom_Movable):   # /mob/
    loc = None
    key = ''  # Login
    ckeysub = re.compile('\W')

    def ckey(self): ckeysub.sub('', key.lower())
    client = None  # Client object
    sight = 0  # SEEINVIS, SEEMOBS, SEEOBJS, SEETURFS, BLIND
    group = []  # List of mobs allowed to switch places
    density = 1
    online = False

    def Login():
        pass

    def Logout():
        pass


class PyondClient(metaclass=PyondObjectMetaclass):
    key = ''  # Login
    ckeysub = re.compile('\W')

    def ckey(self): ckeysub.sub('', key.lower())
    mob = None  # Client's mob
    eye = None  # Center of view
    lazy_eye = 0  # Deprecated
    dir = 0  # Direction
    address = ''  # Client ip
    statobj = None  # Stat object to show
    statpanel = ''  # Stat panel name currently visible
    script = ''  # initial script
    macro_mode = 0  # Deprecated

    def New(self, usr=None):
        if self.mob is None:
            pass

    def Del(self):
        if self.mob is not None:
            self.mob.Logout()


class PyondWorld(metaclass=PyondObjectMetaclass):   # /world/
    address = 'localhost'  # Host
    all = {}
    area = None
    byond_version = 1.0
    cache_lifespan = 30
    client = PyondClient
    clients = {}

    def contents(self): return []  # Inner contents

    cpu = 0  # deprecated
    executor = ''
    game_state = 0  # gs=1 means server is full
    host = ''
    hub = 'Exod1v.SS13'
    hub_password = 'password'
    icon_size = 32

    def log(self, text): logger.info(text)  # Logger

    loop_checks = 1
    map_format = TOPDOWN_MAP
    maps = []
    maxx = 255
    maxy = 255  # defined by map file
    maxz = 255
    mob = None
    name = ''
    objects = {}
    params = {}  # Parameters, sys.argv. n=1&m=2&l=3.
    if sys.argv[-1].find('&') > 0:
        params = dict([i.split('=') for i in sys.argv[-1].split('&')])
    port = 2508  # Port
    internet_address = 'byond://'+str(address)+':'+str(port)

    def realtime(self): return int(time.time()*10)

    reachable = True
    sleep_offline = False  # Stop world if no clients are online
    starttime = int(time.time()*10)
    status = ''
    system_type = 'MS_WINDOWS' if sys.platform == 'win32' else 'UNIX'
    tick_lag = 1  # tick_lag/0.1 = ticks per second
    fps_var = 1.0/tick_lag

    def time(self): return int(time.time()*10)-starttime

    def timeofday(self): return self.log('timeofday')

    turf = None
    url = internet_address
    version = 0
    view = (11, 11)
    visible = True

    def AddCreadits(self, player, credits, note):
        logger.debug("world.AddCredits", credits, "on", player, "note:", note)
        return True

    def ClearMedal(self, medal, player):
        logger.debug("world.ClearMedal:", medal, "on", player)

    def Del(self):
        logger.debug("world.Del")

    def Export(self, sendstr):
        logger.debug("world.Export:", sendstr)

    def GetConfig(self, config, param):
        logger.debug("world.GetConfig:", config, param)
        return ''

    def GetCredits(self, player):
        logger.debug("world.GetCredits:", player)
        return False

    def GetMedal(self, medal, player):
        logger.debug("world.GetMedal:", medal, "on", player)
        return False

    def GetScores(*args):
        logger.debug("world.GetScores", *args)
        return False

    def get_class(self, name, default=None):
        return self.objects.get(name, default)

    def get_tile(self, x, y, z=1):
        return self.maps[z][y][x]

    def Import(self):
        logger.debug("world.Import")
        return False

    def IsBanned(*args):
        logger.debug("world.IsBanned", *args)
        return False

    def IsSubscribed(player, hub="BYOND"):
        logger.debug("world.IsSubscribed:", player, hub)

    def load_maps(self, mapfiles):   # self.maps[z][y][x]
        logger.debug("Reading maps:")
        maps = [0]
        for mapfile in mapfiles:
            logger.debug("    "+mapfile)
            maxx = 0
            maxy = 0
            maxz = 0
            map = [0]
            objects = {}
            mapfs = open(mapfile)
            line = mapfs.readline()
            defpattern = re.compile('"(\w)" = \((.+)\)')
            while line != '\n':
                match = defpattern.match(line)
                objects[match.group(1)] = match.group(2).split(',')
                line = mapfs.readline()
            deflen = len(list(objects.keys())[0])
            line = mapfs.readline()
            while line != '':
                x, y, z = [int(i) for i in re.match('\((\d+)\,(\d+)\,(\d+)\) = {"', line).groups()]
                line = mapfs.readline().replace('\n', '')
                maxx = max(maxx, len(line))
                y = 1
                maplines = []
                while line != '"}':
                    maplines.append(line)
                    line = mapfs.readline().replace('\n', '')
                for line in maplines:
                    mapline = [0]
                    x = 1
                    for char in [line[i:i+deflen] for i in range(0, len(line), deflen)]:
                        tile = []
                        for object in objects[char]:
                            tc = type2class(object)
                            newobj = self.objects[tc]()
                            newobj.z = z
                            newobj.y = len(maplines) + 1 - y
                            newobj.x = x
                            newobj.world = self
                            newobj.New()
                            base = tc.split('_')[0].lower()
                            if base not in self.all:
                                self.all[base] = [newobj]
                            else:
                                self.all[base].append(newobj)
                            tile.append(newobj)
                        mapline.append(tile)
                        x += 1
                    map.insert(1, mapline)
                    y += 1
                mapfs.readline()
                line = mapfs.readline()
            maxy = max(maxy, len(map)-1)
            while len(maps) <= z:
                maps.append(0)
            maps[z] = map
        maxz = len(maps)-1
        self.maps = maps
        self.maxx = maxx
        self.maxy = maxy
        self.maxz = maxz

    def New(self):
        logger.debug("world.New")

    def OpenPort(port=0):
        logger.debug("world.OpenPort:", port)

    def PayCredits(self, player, credits):
        logger.debug("world.PayCredits:", credits, "on", player)

    def Reboot(self, reason=0):
        logger.debug("world.Reboot, reason:", reason)

    def Repop(self):
        logger.debug("world.Repop (Reboot)")

    def SetConfig(self, config, param, value):
        logger.debug("world.SetConfig:", config, param, value)

    def SetMedal(self, medal, player):
        logger.debug("world.SetMedal:", medal, "on", player)

    def Topic(self, topicstr):
        logger.debug("world.Topic:", topicstr)
