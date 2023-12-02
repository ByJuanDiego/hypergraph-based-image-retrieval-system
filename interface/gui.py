from tkinter import filedialog, Tk, Label, Button
from PIL import Image, ImageTk
from typing import List
import os
import math

from graph.essential import Graph
from graph.embeddings.full_body_3D import get_graph_from_full_body_image, get_pose_model

from indexing.indexes import HyperGraph
from retrieval.algorithms import knn_retrieval
from dataset.pickle import load_activity_per_image


class GUI:
    _hyper_graphs: List[HyperGraph]
    _pose_model = get_pose_model()

    _query_path: str = ""
    _labels: List[str]
    _tags = None

    _width = 1080
    _height = 1080

    def __init__(self, hyper_graphs: List[HyperGraph], labels: List[str]):
        self._hyper_graphs = hyper_graphs
        self._labels = labels
        self._tags = load_activity_per_image()

    def run(self):
        margin_left = margin_top = 5
        query_width = math.floor(0.25*self._width)
        btn_width   = math.floor(0.03*self._width)
        result_width = math.floor(0.75*self._width)
        def browse_files():
            filename = filedialog.askopenfilename(
                initialdir=os.getcwd(),
                title="Select a File",
                filetypes=(("Images files", "*.jpg*"),
                           ("Images files", "*.jpeg*"),
                           ("all files", "*.*")))

            if not filename:
                return

            clear_query_outputs()
            print(filename)
            pil_image = Image.open(filename)
            x, y = pil_image.size
            pil_image = pil_image.resize((query_width, query_width))
            img = ImageTk.PhotoImage(pil_image)

            label = Label(window)
            label.image = img  # Retain reference to the image object
            label.configure(image=img)  # Set the image to the label
            label.place(x=margin_left, y=margin_top)  # Adjust x, y coordinates as needed

            self._query_path = filename

        def query():
            if not self._query_path:
                return

            k = 6
            graph_query: Graph = get_graph_from_full_body_image(
                path=self._query_path,
                pose_model=self._pose_model,
                threshold=0.0
            )

            result_paths: List[List[str]] = []
            for hyper_graph in self._hyper_graphs:
                result_paths.append(knn_retrieval(hyper_graph, graph_query, k=k))

            [print(x) for x in result_paths]
            for result in result_paths:
                for path in result:
                    print(self._tags.get(path.split('/')[1], {}))
                print()

            for i in range(len(result_paths)):
                x = int(result_width) // len(result_paths)
                y = math.floor(0.8*x)

                method_label = Label(window, text=self._labels[i], height=1, width=18)
                method_label.place(x=query_width + i*x, y=0)

                for j, filename in enumerate(result_paths[i]):
                    pil_image = Image.open(filename)

                    pil_image = pil_image.resize((x, y))
                    img = ImageTk.PhotoImage(pil_image)

                    label = Label(window)
                    label.image = img  # Retain reference to the image object
                    label.configure(image=img)  # Set the image to the label
                    label.place(x=query_width + i*x, y=20+margin_top + j*y)  # Adjust x, y coordinates as needed

        def clear_query_outputs():
            # Destroy all labels and images created during the query
            for widget in window.winfo_children():
                if isinstance(widget, Label):
                    widget.destroy()

        # Create the root window
        window = Tk()

        # Set window title
        window.title("Image Retrieval System Demo")

        # Set window size
        window.geometry(str(self._width) + "x" + str(self._height))

        # Set window background color
        window.config(background="white")

        button_explore = Button(window,
                                text="Browse Files",
                                command=browse_files,
                                width=btn_width)

        button_exit = Button(window,
                             text="Exit",
                             command=exit,
                             width=btn_width)

        button_query = Button(window,
                              text="Search",
                              command=query,
                              width=btn_width)

        button_clear = Button(window,
                              text="Clear",
                              command=clear_query_outputs,
                              width=btn_width)

        btns = [button_explore, button_exit, button_query, button_clear]

        for i, btn in enumerate(btns):
            btn.place(x=margin_left+10, y=(self._height/3) + i*50)

        # Let the window wait for any events
        window.mainloop()
