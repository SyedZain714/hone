import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton

class InteractiveTreeVisualizer:
    def __init__(self, schema):
        self.schema = schema
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.ax.set_title('Graph Visualization')

        self.pos, self.G, self.labels = self.plot_graph(self.schema)
        self.nodes = nx.draw_networkx_nodes(self.G, pos=self.pos, ax=self.ax, node_size=3000, node_color="skyblue", node_shape="s", alpha=0.5, linewidths=40)
        self.edges = nx.draw_networkx_edges(self.G, pos=self.pos, ax=self.ax, arrows=False)
        self.texts = nx.draw_networkx_labels(self.G, pos=self.pos, labels=self.labels, ax=self.ax, font_size=8)

        self.zoom_factor = 1.1  # Zoom factor for zooming in/out
        self.pan_factor = 0.01  # Pan factor for panning left/right/up/down
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)

        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.fig.canvas.mpl_connect('button_press_event', self.on_button_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

    def plot_graph(self, d, parent_name='', pos=None, G=None, labels=None, level=0, x=0, y=0, dx=1.5, dy=1):
        if pos is None:
            pos = {}
        if G is None:
            G = nx.DiGraph()
        if labels is None:
            labels = {}

        if not isinstance(d, dict):
            return pos, G, labels

        current_name = parent_name
        G.add_node(current_name)
        labels[current_name] = parent_name
        pos[current_name] = (x, y)

        children = d.items()
        width = sum(1 for k, v in children)  # Counting keys as nodes
        next_x = x - width / 2  # Start from the leftmost point

        for k, v in children:
            child_name = f"{current_name}.{k}"
            child_width = 1  # Each key is treated as a single node width
            child_x = next_x + child_width / 2  # Center child under its parent
            next_x += child_width  # Move to the next position

            pos[child_name] = (child_x, y - dy)
            G.add_node(child_name)
            G.add_edge(current_name, child_name)
            labels[child_name] = k

            if isinstance(v, dict):
                pos, G, labels = self.plot_graph(v, child_name, pos, G, labels, level + 1, child_x, y - dy, dx, dy)

        return pos, G, labels

    def on_scroll(self, event):
        if event.button == 'up':
            self.zoom(event.xdata, event.ydata, zoom_in=True)
        elif event.button == 'down':
            self.zoom(event.xdata, event.ydata, zoom_in=False)
        plt.draw()

    def on_button_press(self, event):
        if event.button == MouseButton.LEFT:
            self.last_x = event.x
            self.last_y = event.y

    def on_mouse_move(self, event):
        if event.button == MouseButton.LEFT:
            delta_x = (event.x - self.last_x) * self.pan_factor
            delta_y = (event.y - self.last_y) * self.pan_factor
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
            self.ax.set_xlim(xlim[0] - delta_x, xlim[1] - delta_x)
            self.ax.set_ylim(ylim[0] + delta_y, ylim[1] + delta_y)
            self.last_x = event.x
            self.last_y = event.y
            plt.draw()

    def zoom(self, x, y, zoom_in=True):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        if zoom_in:
            new_xlim = (x - (x - xlim[0]) / self.zoom_factor, x + (xlim[1] - x) / self.zoom_factor)
            new_ylim = (y - (y - ylim[0]) / self.zoom_factor, y + (ylim[1] - y) / self.zoom_factor)
        else:
            new_xlim = (x - (x - xlim[0]) * self.zoom_factor, x + (xlim[1] - x) * self.zoom_factor)
            new_ylim = (y - (y - ylim[0]) * self.zoom_factor, y + (ylim[1] - y) * self.zoom_factor)
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        plt.draw()