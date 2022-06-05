from itertools import product, combinations, chain
import networkx as nx

def edges_power_set(n):
    # the function returns all the possible edges of a graph with n nodes
    node_lst = [i for i in range(1, n + 1)]
    prod = product(node_lst, node_lst)
    lst = list(prod)
    # remove self-edges
    new_list = [(x, y) for x, y in lst if x != y]
    return chain.from_iterable(combinations(new_list, r) for r in range(n - 1, len(new_list) + 1))


def create_graph(edges, nodes):
    # create a graph from the edges and nodes
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    return graph


def is_connected(edges, nodes):
    # check if the graph is connected
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    return nx.is_connected(graph)


def is_isomorphic(graph1, graph_list):
    # check if the graph is isomorphic to one of the graphs in the list
    for graph in graph_list:
        if nx.is_isomorphic(graph1, graph):
            return True
    return False


def all_motifs(n):
    # the function returns all the motifs of a graph with n nodes
    motifs = []
    all_graphs_edges = edges_power_set(n)
    nodes = [i for i in range(1, n + 1)]
    for edges in all_graphs_edges:
        if is_connected(edges, nodes):
            graph = create_graph(edges, nodes)
            if not is_isomorphic(graph, motifs):
                motifs.append(graph)
    return motifs


def save_motifs_to_txt(motifs, n):
    # save the motifs to a txt file
    i = 1
    with open(f'ex1_n={n}_save_motifs.txt', 'w') as f:
        f.write(f'n={n}\n')
        f.write(f'count={len(motifs)}\n')
        for graph in motifs:
            f.write(f'#{i}\n')
            i += 1
            edges = list(graph.edges)
            for j in range(0, len(edges)):
                f.write(f'{edges[j][0]} {edges[j][1]}\n')
    f.close()


def sub_graphs_size_n(graph, n):
    # the function returns all the subgraphs with n nodes of a given graph
    subgraph_list = []
    nodes_combinations = list(combinations(graph.nodes, n))
    for nodes_comb in nodes_combinations:  # go over all possible subgraphs nodes
        subgraph = graph.subgraph(nodes_comb)
        subgraph_list.append(subgraph)
    return subgraph_list


def count_motifs_in_sub_graphs(graph, n):
    # the function counts the amount of each motif that isomorphic to a subgraphs of a given graph
    motifs = all_motifs(n)  # all the motifs of a graph with n nodes
    motifs_amount = [0] * len(motifs)
    sub_graphs = sub_graphs_size_n(graph, n)

    for subgraph in sub_graphs:
        for i in range(len(motifs)):
            if nx.is_isomorphic(motifs[i], subgraph):
                motifs_amount[i] += 1
    return motifs_amount, motifs


def save_ex2_to_txt(motifs_amount, motifs, n):
    # save the motifs to a txt file
    i = 1
    with open(f'ex2_motifs_appearances.txt', 'w') as f:
        f.write(f'n={n}\n')
        for i, amount in enumerate(motifs_amount):
            f.write(f'#{i + 1}\n')
            f.write(f'count={amount}\n')
            edges = list(motifs[i].edges)
            for j in range(0, len(edges)):
                f.write(f'{edges[j][0]} {edges[j][1]}\n')
    f.close()


def read_graph_from_txt(file_name):
    # read a graph from a txt file
    # we assumed that the graph is connected and n is in the first line
    graph = nx.DiGraph()
    with open(file_name, 'r') as f:
        for i, line in enumerate(f):
            # line = line.replace("\n", "")
            if i == 0:
                n = int(line)
            else:
                edge = line.split()
                graph.add_edge(int(edge[0]), int(edge[1]))
    f.close()
    return graph, n


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # 1 A) save all the motifs of size n to a txt file
    n = 2
    motifs = all_motifs(n)
    save_motifs_to_txt(motifs, n)

    # 1 B) Output the result of the program in question 1 for n = 1 to 4
    # for i in range(1, 5):
    #     motifs = all_motifs(i)
    #     save_motifs_to_txt(motifs, i)

    # 1 C) the maximal number n for which your program can complete
    # successfully within no more than 1 hour of computing time
    # i = 0
    # end, start = 0, 0
    # while end - start <= 3600:
    #     i += 1
    #     start = time()
    #     motifs = all_motifs(i)
    #     end = time()
    # print(f'The maximal number n for which your program can complete successfully within no more than 1 hour of '
    #       f'computing time is {i-1}')

    # 2) The program should output all sub-graphs of size 𝑛 and
    # count how many instances appear of each motif in each sub-graph.
    # save the sub-graphs to a txt file named ex2_motifs_appearances.txt
    # graph, n = read_graph_from_txt('enter your graph txt file name here')
    # motifs_amount, motifs = count_motifs_in_sub_graphs(graph, n)
    # save_ex2_to_txt(motifs_amount, motifs, n)

    # in order to run the example for exercise 2 you need to enter the file name ex2.txt
    # graph, n = read_graph_from_txt('ex2.txt')
    # motifs_amount, motifs = count_motifs_in_sub_graphs(graph, n)
    # save_ex2_to_txt(motifs_amount, motifs, n)


