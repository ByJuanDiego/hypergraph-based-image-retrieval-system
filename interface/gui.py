import tkinter as tk

from indexing.indexes import HyperGraph


class GUI:
    _hypergraph: HyperGraph
    _window: tk.Tk

    def __init__(self):
        self._window = tk.Tk()

    def run(self):
        self._window.title("Image Retrieval System Demo")
        self._window.geometry("1000x800")

        button: tk.Button = tk.Button(self._window, text="Send query", padx=20, pady=10)
        button.place(x=50, y=50)

        self._window.mainloop()
