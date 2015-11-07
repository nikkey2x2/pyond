from pyond import *
print("main-a loaded")
__all__ = ['Mob','Mob_Player','Mob_Rat','Turf','Turf_Floor','Turf_Wall','Obj','Obj_Cheese','Obj_Scroll','Area','Area_Outside','Area_Cave','World']
class Mob(PyondMob):
    pass
class Mob_Player(Mob):
    icon = 'player.dmi'
class Mob_Rat(Mob):
    icon = 'rat.dmi'
class Turf(PyondTurf):
    pass
class Turf_Floor(Turf):
    icon = 'floor.dmi'
class Turf_Wall(Turf):
    icon = 'wall.dmi'
    density = 1
    opacity = 1
class Obj(PyondObj):
    pass
class Obj_Cheese(Obj):
    icon = 'cheese.dmi'
class Obj_Scroll(Obj):
    icon = 'scroll.dmi'
class Area(PyondArea):
    pass
class Area_Outside(Area):
    pass
class Area_Cave(Area):
    pass
class World(PyondWorld):
    name = "Your First World"
    mob = Mob_Player