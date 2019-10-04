from windows import *
import global_vars

if __name__ == "__main__":
    global_vars.main_window = MainWindow()
    global_vars.main_window.after(100, global_vars.main_window.draw)
    global_vars.main_window.mainloop()