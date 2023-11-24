from tkinter import filedialog, Tk, Label, Button
from PIL import Image, ImageTk

from graph.essential import Graph
from graph.embeddings.full_body_3D import get_graph_from_full_body_image, get_pose_model

from indexing.indexes import HyperGraph
from retrieval.algorithms import knn_retrieval

import os


class GUI:
    _hypergraph: HyperGraph
    _pose_model = get_pose_model()

    _query_path: str = ""

    def __init__(self, hypergraph: HyperGraph):
        self._hypergraph = hypergraph

    def run(self):
        def browse_files():
            filename = filedialog.askopenfilename(
                initialdir=os.getcwd(),
                title="Select a File",
                filetypes=(("Images files", "*.jpg*"),
                           ("Images files", "*.jpeg*"),
                           ("all files", "*.*")))

            pil_image = Image.open(filename)
            pil_image = pil_image.resize((170, 250))
            img = ImageTk.PhotoImage(pil_image)

            label = Label(window)
            label.image = img  # Retain reference to the image object
            label.configure(image=img)  # Set the image to the label
            label.place(x=100, y=400)  # Adjust x, y coordinates as needed

            self._query_path = filename

        def query():
            if not self._query_path:
                return

            graph_query: Graph = get_graph_from_full_body_image(
                path=self._query_path,
                pose_model=self._pose_model,
                threshold=0.0
            )

            self._result_paths = knn_retrieval(self._hypergraph, graph_query, k=4)

            x, y = 400, 50

            for filename in self._result_paths:
                pil_image = Image.open(filename)
                pil_image = pil_image.resize((250, 170))
                img = ImageTk.PhotoImage(pil_image)

                label = Label(window)
                label.image = img  # Retain reference to the image object
                label.configure(image=img)  # Set the image to the label
                label.place(x=x, y=y)  # Adjust x, y coordinates as needed
                y += 180

        # Create the root window
        window = Tk()

        # Set window title
        window.title("Image Retrieval System Demo")

        # Set window size
        window.geometry("1400x800")

        # Set window background color
        window.config(background="white")

        button_explore = Button(window,
                                text="Browse Files",
                                command=browse_files)

        button_exit = Button(window,
                             text="Exit",
                             command=exit)

        button_query = Button(window,
                              text="Search",
                              command=query)

        button_explore.place(x=100, y=100)
        button_exit.place(x=100, y=150)
        button_query.place(x=100, y=200)

        # Let the window wait for any events
        window.mainloop()
