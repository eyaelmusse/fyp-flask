import networkx as nx
import os
import numpy as np
import pandas as pd


class ClassFeature:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

''' Class features are calculated for each method's cfg, then averaged out '''
class ClassFeatures:
    def __init__(self) -> None:
        # Number of vertices in the CFG 
        self.vertices_count = []
        # The number of edges in CFG
        self.edges_count = []
        # the minimum eccentricity of the CFG.
        self.radius = []
        # the maximum eccentricity of the CFG.
        self.diameter = []
        # size of the set of nodes with eccentricity equal to the radius.
        self.centre = []
        # size of the set of nodes with eccentricity equal to the diameter.
        self.periphery = []
        # the sum of path length d(u, v) between all node pairs, normalized by n × (n − 1). n is the total number of nodes in the CFG.
        self.ave_shortest_path_len = []
        self.ave_shortest_path_len_undirected = []
        # measure of how well connected a graph is
        self.algebraic_connectivity = []
        # average node degrees 
        self.ave_graph_degree  = []    
        # measures how many edges are in a graph compared to the maximum possible edges
        self.density = []
        # the minimum number of vertices/nodes that must be removed to disconnect the graph
        self.vertex_connectivity = []
        # the minimum number of edges that must be removed to disconnect the graph
        self.edge_connectivity = []
        # the fraction of possible triangles present in the CFG, averaged
        self.transitivity = []
        # size of the min cardinality edge cover of the graph as a set of edges
        self.min_edge_cover = []

        # # measures the percentage of methods in a class having Mc-Cabe’s cyclomatic complexity greater than 10.
        # cc10_percentage : float = 0
        # cc10_percentage_count = 0  # number of methods having Mc-Cabe’s cyclomatic complexity greater than 10.

    ''' Parse another method cfg '''
    def add_cfg(self, cfg: nx.DiGraph):
        undirected_cfg = nx.Graph(cfg)

        self.vertices_count.append(cfg.number_of_nodes())
        self.edges_count.append(len(cfg.edges))
        self.radius.append(nx.radius(undirected_cfg))
        self.diameter.append(nx.diameter(undirected_cfg))
        self.centre.append(len(nx.center(undirected_cfg)))
        self.periphery.append(len(nx.periphery(undirected_cfg)))
        self.ave_shortest_path_len.append(nx.average_shortest_path_length(cfg))
        self.ave_shortest_path_len_undirected.append(nx.average_shortest_path_length(undirected_cfg))
        self.algebraic_connectivity.append(nx.algebraic_connectivity(undirected_cfg))
        degree_list = [x[1] for x in cfg.degree()]
        self.ave_graph_degree.append(np.average(degree_list))
        self.density.append(nx.density(cfg))
        self.vertex_connectivity.append(nx.node_connectivity(undirected_cfg))
        self.edge_connectivity.append(nx.edge_connectivity(undirected_cfg))
        self.min_edge_cover.append(len(nx.min_edge_cover(undirected_cfg)))
        self.transitivity.append(nx.transitivity(undirected_cfg))
    
    def get_features(self):
        features = []
        features.append(ClassFeature("Vertex total", sum(self.vertices_count)))
        features.append(ClassFeature("Edges total", sum(self.edges_count)))
        features.append(ClassFeature("Min edges", min(self.edges_count)))
        features.append(ClassFeature("Max edges", max(self.edges_count)))
        features.append(ClassFeature("Min vertices", min(self.vertices_count)))
        features.append(ClassFeature("Max vertices", max(self.vertices_count)))

        # averaged for all methods in a class
        features.append(ClassFeature("Radius", np.average(self.radius)))
        features.append(ClassFeature("Diameter", np.average(self.diameter)))
        features.append(ClassFeature("Centre", np.average(self.centre)))
        features.append(ClassFeature("Periphery", np.average(self.periphery)))
        features.append(ClassFeature("Average shortest path length", np.average(self.ave_shortest_path_len)))
        features.append(ClassFeature("Average shortest path length (undirected)", np.average(self.ave_shortest_path_len_undirected)))
        features.append(ClassFeature("Algebraic connectivity", np.average(self.algebraic_connectivity)))
        features.append(ClassFeature("Average graph Degree", np.average(self.ave_graph_degree)))
        features.append(ClassFeature("Density", np.average(self.density)))
        features.append(ClassFeature("Max density", max(self.density)))
        features.append(ClassFeature("Vertex connectivity", np.average(self.vertex_connectivity)))
        features.append(ClassFeature("Edge connectivity", np.average(self.edge_connectivity)))
        features.append(ClassFeature("Min edge cover", np.average(self.min_edge_cover)))
        features.append(ClassFeature("Transivity", np.average(self.transitivity)))

        features.append(ClassFeature("Standard deviation of average graph degree", np.std(self.ave_graph_degree)))
        return features


# --- calculate and write stats
def parse_cfg(current_dir):
    nx_csv_name = "cfg_stats.csv"
    need_header = True
    csv_file = open(os.path.join(current_dir, nx_csv_name), "w")

    classes_directory = os.path.join(current_dir, "evosuite-graphs/")
    # for each class
    for class_name in os.listdir(classes_directory):
        class_path = os.path.join(classes_directory, class_name)
        classfeatures = ClassFeatures()

        cfg_folder = os.path.join(class_path, "ACFG/")  # actual control flow graphs
        try:
            method_list = os.listdir(cfg_folder)
        except FileNotFoundError:
            print(f"ACFG not found: {class_path}")
        # for each method in a class
        for function_graph in method_list:
            graph_path = os.path.join(cfg_folder, function_graph)
            if os.path.isfile(graph_path) and os.path.splitext(function_graph)[-1].lower() == ".dot":
                try:
                    graph = nx.nx_agraph.read_dot(graph_path)
                except Exception as e:
                    print(f"Failed reading {e}")
                    continue
                classfeatures.add_cfg(graph)
        
        # class name
        try:
            features = classfeatures.get_features()
        except ValueError as e:
            print(f"Skipping! Failed parsing: {e}")
            continue

        features.insert(0, ClassFeature("TARGET_CLASS", class_name))  # at start, for FinalMerge compatibility
        # for merging with javaparser, which doesn't record the name of anonymous classes properly (i.e doesn't use $)
        features.append(ClassFeature("DotClass", class_name.replace("$", ".")))
        
        if need_header:
            for feature in features:
                csv_file.write(f"{feature.name},")
            csv_file.write("\n")
            need_header = False
        
        for feature in features:
            csv_file.write(f"{feature.value},")
        csv_file.write("\n")

    csv_file.close()
parse_cfg("targ_files/9661ad8a-1d02-4e98-b6d1-0a083d8d4dfa")

def merge_javaparser(current_dir):
    nx_csv_name = "cfg_stats.csv"

    with open(os.path.join(current_dir, "jpnX.csv"), "w") as merged_csv:
        nx_csv = open(os.path.join(current_dir, nx_csv_name), "r")

        jp_output = os.path.join(current_dir, "jp_output")
        jp_filename = next((f for f in os.listdir(jp_output) if f.endswith('_javaparser.csv')), None)
        if jp_filename is None:
            raise FileNotFoundError("JavaParser CSV file not found in the current directory.")
        jp_csv = open(os.path.join(jp_output, jp_filename), "r")

        nx_data = pd.read_csv(nx_csv)
        jp_data = pd.read_csv(jp_csv)

        nx_csv.close()
        jp_csv.close()

        # make headers match
        jp_data = jp_data.rename(columns={"TARGET_CLASS": "DotClass"})

        # outer so that jp classes that dont have a matching nx class (e.g. couldn't run it on project) are preserved
        merged_data = nx_data.merge(jp_data, on="DotClass")

        # remove unneeded columns
        merged_data.drop("DotClass", axis=1)
        merged_data.drop("File", axis=1)

        merged_data.to_csv(merged_csv,index=False)
