import score
import tkinter as tk

LABEL_FONT = ("", 12, "bold")


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(master=self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, LiveMatch, Fixture):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.startMenu(parent, controller)

    def startMenu(self, parent, controller):
        self.livebtn = tk.Button(master=self, text="Live Matches",
                                 font=("", 16, "bold"),
                                 command=lambda: controller.show_frame("LiveMatch"))
        fixturebtn = tk.Button(master=self, text="Fixture",
                               font=("", 16, "bold"),
                               command=lambda: controller.show_frame("Fixture"))
        self.livebtn.pack(fill="x", anchor="center")
        fixturebtn.pack(fill="x", anchor="center")


class LiveMatch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.showLive()
        self.goBack(controller)

    def showLive(self):
        liveMatches = score.getLiveMatches()
        for comp in liveMatches:
            if len(comp) == 1:
                # continue
                pass
            label = tk.Label(master=self, text=comp[0], borderwidth="4",
                             justify="left", anchor="e",
                             font=LABEL_FONT, fg="blue")
            label.pack()
            for matches in comp[1:]:
                match = matches[0] + " " + matches[1] + \
                    " " + " " + matches[2] + " " + matches[3]
                tk.Label(master=self, text=match, font="12").pack()

    def goBack(self, controller):
        backbtn = tk.Button(master=self, text="Back",
                            command=lambda: controller.show_frame("StartPage"))
        backbtn.pack(fill="x")


class Fixture(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.showFixture()
        self.goBack(controller)

    def showFixture(self):
        fixture = score.getFixture("2017-05-08")
        for comp in fixture:
            if len(comp) == 1:
                # continue
                pass
            compName = comp[0]
            tk.Label(master=self, text=compName, font=LABEL_FONT, fg="blue").pack()
            for matches in comp[1:]:
                match = matches[0] + " " + matches[1] + " " + matches[2]
                tk.Label(master=self, text=match).pack()

    def goBack(self, controller):
        backbtn = tk.Button(master=self, text="Back",
                            command=lambda: controller.show_frame("StartPage"))
        backbtn.pack(fill="x")


if __name__ == "__main__":
    root = App()
    root.mainloop()
