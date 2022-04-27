def draw_connectogram(mat_file=None, node_labels=None, threshold=None, direction='both'):
    import matplotlib.pyplot as plt
    import networkx as nx
    import numpy as np
    from nxviz import (annotate, nodes, layouts, utils, edges, lines, plots)
    import pandas as pd
        
    labels_df = pd.read_csv(node_labels)

    A = np.loadtxt(mat_file, delimiter=',')  #adjacency matrix text file

    if len(A) != labels_df.shape[0]:
        raise ValueError("Label and matrix dimensions do not match.")

    if threshold:
        if direction == 'both':
            direction_vals = "abs(A)"
        elif direction == 'negative':
            direction_vals = 'A * -1'
        elif direction == 'positive':
            direction_vals = 'A'
        if threshold[0] == 'proportional':
            A_sort = np.sort(
                abs(
                    A[np.triu(A, k = 1) != 0]
                )
            )
            thresh_pct = threshold[1]/100
            thresh = int(thresh_pct*A_sort.size)
            exec(f"A[{direction_vals} < A_sort[-thresh]] = 0")
        elif threshold[0] == 'absolute':
            exec(f"A[{direction_vals} < threshold[1]] = 0")
        else:
            return
    G = nx.from_numpy_matrix(np.triu(A, k = 1))

    labels_df['label'] =  [f"{labels_df['hemi'][x]} {labels_df['group_name'][x]}" for x in labels_df.index]

    nx.set_node_attributes(G, dict(zip(labels_df.index, labels_df.ROI)), name="ROIs")
    nx.set_node_attributes(G, dict(zip(labels_df.index, labels_df.label)), name="label")
    nx.set_node_attributes(G, dict(zip(labels_df.index, labels_df.grouping)), name="grouping")
    nx.set_node_attributes(G, dict(zip(labels_df.index, labels_df.group_name)), name="group name")

    fig, ax = plt.subplots()

    # Customize node styling
    nt = utils.node_table(G)
    pos = layouts.circos(nt, group_by='label')
    cmapping = dict(zip(nt['grouping'].unique(), plt.cm.get_cmap("tab10").colors))
    nt['color_by'] = [ cmapping[x] for x in nt['grouping'] ]
    alpha = nodes.transparency(nt, alpha_by=None)
    size = nodes.node_size(nt, size_by=None)
    patches = nodes.node_glyphs(
        nt, pos, node_color=nt['color_by'], alpha=alpha, size=size
    )
    for patch in patches:
        ax.add_patch(patch)
    annotate.circos_group(G, group_by="label")

    # Customize edge styling
    et = utils.edge_table(G)
    if direction == 'both':
        edge_colour_setting = "weight"
    else:
        edge_colour_setting = None
    edge_color = edges.edge_colors(et, nt=None, color_by=edge_colour_setting, node_color_by=None)
    lw = edges.line_width(et, lw_by=None)
    alpha = edges.transparency(et, alpha_by="weight")
    patches = lines.circos(
        et, pos, edge_color=edge_color, alpha=alpha, lw=lw, aes_kw={"fc": "none"}
    )
    for patch in patches:
        ax.add_patch(patch)

    plots.despine()
    plots.rescale(G)
    plots.aspect_equal()

    fig = plt.gcf()

    return fig