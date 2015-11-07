#! python3.5
from pyond import *
import importlib

FILE_DIR = (".","icons","readme","sounds","Your First World!_files")
include = (
"maina",
)
maps = (
"map.dmm",
)
codeobjs = load_code(include)
world = codeobjs.get('World', PyondWorld)()
world.objects.update(codeobjs)
world.load_maps(maps)
tile=world.get_tile(8,9)
print(tile,tile[0].icon,tile[0].type(),tile[0].x,tile[0].y,tile[0].z)
server = PyondServer(world)
server.start()