import global_vars
from PIL import Image
from zipfile import ZipFile
import os, shutil


class TexturePack:
    def __init__(self, name, desc, ver, image, xml):
        self.name = name
        self.desc = desc
        self.ver = ver
        self.img = image
        self.xml = xml

def find_textures():
    for filename in os.listdir(global_vars.game_folder + "/texturepacks"):
        if filename.endswith(".zip") or filename.endswith(".texture"):
            global_vars.pack_files.append(filename)
    if global_vars.debug_mode: print("found packs: {}".format(global_vars.pack_files))
    for pack in global_vars.pack_files:
        p = open_pack(global_vars.game_folder + "/texturepacks/" + pack)
        global_vars.packs[p.name] = p
    i = 1
    for pack_name in global_vars.packs.keys():
        global_vars.main_window.sidebar.insert(i, pack_name)
        i += 1
    try:
        active = open(global_vars.game_folder+"/texturepacks/active_packs.txdata", 'r')
        packs = active.read().split("\n")
        global_vars.active_packs.extend(packs)
    except FileNotFoundError:
        pass


def open_pack(filename : str):
    l = locals()
    z = ZipFile(filename)
    txt = z.read("info.txp")
    images = []
    xml = None
    for i in z.infolist():
        if i.filename.endswith(".png"): images.append(Image.open(z.open(i)).convert("RGBA"))
        if i.filename.endswith(".xml"): xml = z.read(i)
    name = filename.split(global_vars.game_folder+"/texturepacks/")[1].split(".")[0]
    desc = ""
    ver = None
    exec(txt, globals(), l)
    name, desc = l["name"], l["desc"]
    return TexturePack(name, desc, ver, images[0], xml)


def construct_pack():
    im = Image.open("res/{}.png".format(global_vars.mode)).convert("RGBA")
    for packname in global_vars.active_packs:
        pack = global_vars.packs[packname]
        im.paste(pack.img, mask=pack.img)
    im.save(global_vars.game_folder+"/Assets/Textures/Ultra/InGame.png")
    shutil.copy("res/InGame.xml", global_vars.game_folder+"/Assets/Textures/Ultra/InGame.xml")
    file = open(global_vars.game_folder+"/texturepacks/active_packs.txdata", "w+")
    for i in range(len(global_vars.active_packs)):
        wr = global_vars.active_packs[i] if i == len(global_vars.active_packs)-1 else global_vars.active_packs[i] + "\n"
        file.write(wr)
    file.close()