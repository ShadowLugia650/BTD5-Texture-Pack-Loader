import global_vars
from PIL import Image
from zipfile import ZipFile
import os


class TexturePack:
    def __init__(self, name, desc, image):
        self.name = name
        self.desc = desc
        self.img = image


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


def open_pack(filename : str):
    l = locals()
    z = ZipFile(filename)
    txt = z.read("info.txp")
    images = []
    for i in z.infolist():
        if i.filename.endswith(".png"): images.append(Image.open(z.open(i)).convert("RGBA"))
    name = filename.split(global_vars.game_folder+"/texturepacks/")[1].split(".")[0]
    desc = ""
    exec(txt, globals(), l)
    name, desc = l["name"], l["desc"]
    return TexturePack(name, desc, images[0])


def construct_pack():
    im = Image.open("res/base.png").convert("RGBA")
    for packname in global_vars.active_packs:
        pack = global_vars.packs[packname]
        im.paste(pack.img, mask=pack.img)
    im.save("res/InGame.png")