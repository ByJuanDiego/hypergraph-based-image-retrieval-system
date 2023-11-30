from tkinter import filedialog, Tk, Label, Button
from PIL import Image, ImageTk
from typing import List
import os

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

    def __init__(self, hyper_graphs: List[HyperGraph], labels: List[str]):
        self._hyper_graphs = hyper_graphs
        self._labels = labels
        self._tags = load_activity_per_image()

    def run(self):
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
            pil_image = pil_image.resize((x // 6, y // 6))
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

            result_paths: List[List[str]] = []
            for hyper_graph in self._hyper_graphs:
                result_paths.append(knn_retrieval(hyper_graph, graph_query, k=4))

            [print(x) for x in result_paths]
            for result in result_paths:
                for path in result:
                    print(self._tags.get(path.split('/')[1], {}))
                print()

            for i in range(len(result_paths)):
                x, y = 450, 50

                method_label = Label(window, text=self._labels[i], height=1, width=28)
                method_label.place(x=x + (300 * i), y=y - 40)

                for filename in result_paths[i]:
                    pil_image = Image.open(filename)

                    pil_image = pil_image.resize((250, 170))
                    img = ImageTk.PhotoImage(pil_image)

                    label = Label(window)
                    label.image = img  # Retain reference to the image object
                    label.configure(image=img)  # Set the image to the label
                    label.place(x=x + (300 * i), y=y)  # Adjust x, y coordinates as needed
                    y += 180

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
        window.geometry("1700x800")

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

        button_clear = Button(window,
                              text="Clear",
                              command=clear_query_outputs)

        button_explore.place(x=100, y=100)
        button_exit.place(x=100, y=150)
        button_query.place(x=100, y=200)
        button_clear.place(x=100, y=250)

        # Let the window wait for any events
        window.mainloop()
