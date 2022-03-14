from homework05.api import get_friends
import igraph
def get_network(users_ids, as_edgelist=True):
    edges = []
    if as_edgelist:
        for x, x_id in enumerate(users_ids):
            try:
                friends_ids_x = get_friends(x_id)
                for y, y_id in enumerate(users_ids):
                    if y_id in friends_ids_x:
                        edges.append((x, y))
            except:
                pass

    if as_edgelist:
        return edges


def draw_graph(id_for_graph):
    friends = get_friends(id_for_graph, 'last_name')
    vertices = [i['last_name'] for i in friends]
    myedges = get_network(get_friends(id_for_graph), as_edgelist=True)
    edges = myedges
    g = igraph.Graph(vertex_attrs={"label": vertices},
              edges=edges, directed=False)
    g.simplify(multiple=True, loops=True)
    N = len(vertices)
    visual_style = {}
    visual_style["vertex_size"] = 8
    visual_style["vertex_label"] = g.vs["label"]
    visual_style["bbox"] = (1000, 1000)
    visual_style["margin"] = 100
    visual_style["vertex_label_dist"] = 1.6
    visual_style["vertex_label_color"] = "black"
    visual_style["edge_color"] = "gray"
    visual_style["autocurve"] = True
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=100000,
        area=N ** 2,
        repulserad=N ** 2)
    igraph.plot(g, str(id_for_graph) + ".png", **visual_style)


if __name__ == '__main__':
    draw_graph(175767409)