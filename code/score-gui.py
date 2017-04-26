import score
import tkinter as tk

root = tk.Tk()

def showComp():
    liveMatches = score.getLiveMatches()
    for comp in liveMatches:
        label = tk.Label(master=root, text=comp[0], borderwidth="4", justify="left", 
            anchor="e", font="-weight bold", fg="blue")
        label.pack()
        if len(comp) == 1:
            tk.Label(master=root, text="No Match!", font="12").pack()
            continue
        for matches in comp[1:]:
            match = matches[0] + " " + matches[1] + " " + " " + matches[2] + " " + matches[3]
            tk.Label(master=root, text=match, font="12").pack()


if __name__ == "__main__":
    showComp()

root.mainloop()