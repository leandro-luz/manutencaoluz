# from igraph import *
# import matplotlib.pyplot as plt
#
#
# def gerar_grafo(vertices, nomes):
#     g = Graph(vertices)
#     g.vs["name"] = nomes
#
#     # g.add_vertices(4)
#     # g.add_edges([(1,2),(2,3),(0,3)])
#     # plot(g, vertex_label=["A", "B", "C", "D"], vertex_color="white")
#     layout = g.layout("kk")
#     fig, ax = plt.subplots()
#     plot(g, layout=layout, target=ax)
#     g.vs["label"] = g.vs["name"]
#     # color_dict = {"m": "blue", "f": "pink"}
#     # g.vs["color"] = [color_dict[gender] for gender in g.vs["gender"]]
#     # plot(g, layout=layout, bbox=(300, 300), margin=20)
#     plot(g, layout=layout, bbox=(300, 300), margin=20, target=ax)
#
#     plt.show()
