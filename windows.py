from tkinter import Tk, Menu, Listbox, Canvas, Frame, Button, font
from tkinter.filedialog import askdirectory
import global_vars, util


class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Bloons TD 5 Texture Loader")
        self.geometry("800x600")
        menu = Menu(self)
        self.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Select Folder", command=self.sel_folder)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=self.disp_about)
        self.sidebar = Listbox(self, width=30, height=37)
        self.sidebar.place(x=0,y=0)
        self.sideframe = Canvas(self, width=600, height=400)
        self.sideframe.place(x=200,y=0)
        self.buttons = Frame(self)
        self.buttons.place(x=675,y=570)
        self.set_buttons()
        self.selected_pack = None
        self.title_font = font.Font(root=self, family='Helvetica', size=24, weight="bold", name="TitleFont")
        self.description_font = font.Font(root=self, family="Helvetica", size=17, name="DescFont")

    def draw(self):
        if len(self.sidebar.curselection()) > 0:
            self.sideframe.create_rectangle(0, 0, 600, 600, fill="gray95")
            sel_raw = self.sidebar.get(self.sidebar.curselection())
            self.selected_pack = sel_raw.replace(" [Active]","")
            self.sideframe.create_text(10, 0, text=sel_raw, font=self.title_font, anchor="nw")
            self.sideframe.create_line(10, 50, 800, 50)
            pack_object = global_vars.packs[self.selected_pack]
            self.sideframe.create_text(10, 60, text=pack_object.desc, font=self.description_font, width=600, anchor="nw")
        self.after(100, self.draw)

    def set_buttons(self):
        def activate(self):
            global_vars.active_packs.append(self.selected_pack)
            addactive = lambda packname: packname if " [Active]" in packname else packname + " [Active]"
            sel_num = self.sidebar.curselection()[0]
            self.sidebar.delete(self.sidebar.curselection()[0])
            self.sidebar.insert(sel_num, addactive(self.selected_pack))
            util.construct_pack()
        def deactivate(self):
            try:
                global_vars.active_packs.remove(self.selected_pack)
                sel_num = self.sidebar.curselection()[0]
                new_str = self.sidebar.get(self.sidebar.curselection()[0]).replace(" [Active]","")
                self.sidebar.delete(self.sidebar.curselection()[0])
                self.sidebar.insert(sel_num, new_str)
                util.construct_pack()
            except ValueError:
                pass
        Button(self.buttons, text="Activate", command=lambda: activate(self)).grid(row=0)
        Button(self.buttons, text="Deactivate", command=lambda: deactivate(self)).grid(row=0,column=1)

    def sel_folder(self):
        global_vars.game_folder = askdirectory()
        util.find_textures()

    def disp_about(self):
        pass