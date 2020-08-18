import goal
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
        liveMatches = goal.getLiveMatches()
        competitions = liveMatches['competitions']
        for comp in competitions:
            compTitle = comp['title']
            matches = comp['matches']
            if len(matches) == 0:
                continue
            label = tk.Label(master=self, text=compTitle, borderwidth="4",
                            justify="left", anchor="e",
                            font=LABEL_FONT, fg="blue")
            label.pack()
            for match in matches:
                teams = match['teams']
                homeTeamTitle = teams['home']['title']
                awayTeamTitle = teams['away']['title']
                score = match['score']
                homeScore = score['home']
                awayScore = score['away']
                state = match['state']
                match = "({}) {} {} - {} {}".format(state, homeTeamTitle, homeScore, awayScore, awayTeamTitle)
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
        fixture = goal.getFixtureMatches("2020-08-08")
        competitions = fixture['competitions']

        for comp in competitions:
            compTitle = comp['title']
            matches = comp['matches']
            if len(matches) == 0:
                continue
            label = tk.Label(master=self, text=compTitle, borderwidth="4",
                            justify="left", anchor="e",
                            font=LABEL_FONT, fg="blue")
            label.pack()
            for match in matches:
                teams = match['teams']
                homeTeamTitle = teams['home']['title']
                awayTeamTitle = teams['away']['title']
                matchTime = match['time']
                match = "{} | {} - {}".format(matchTime, homeTeamTitle, awayTeamTitle)
                tk.Label(master=self, text=match, font="12").pack()

    def goBack(self, controller):
        backbtn = tk.Button(master=self, text="Back",
                            command=lambda: controller.show_frame("StartPage"))
        backbtn.pack(fill="x")


if __name__ == "__main__":
    root = App()
    root.mainloop()
