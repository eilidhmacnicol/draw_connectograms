def draw_connectogram(
    graph=None,
    node_labels=None,
    direction='both',
    cbar_label=None,
    cbar_max=None
):
    import matplotlib.pyplot as plt
    import networkx as nx
    from nxviz import (annotate, nodes, layouts, utils, edges, lines, plots)
    import pandas as pd
    
    ### set up graph object ###
    G = nx.from_numpy_matrix(graph)

    labels_df = pd.read_csv(node_labels)

    if G.number_of_nodes() != labels_df.shape[0]:
        raise ValueError("Label and matrix dimensions do not match.")

    labels_df['label'] =  [f"{labels_df['hemi'][x]} {labels_df['group_name'][x]}" for x in labels_df.index]

    nx.set_node_attributes(G, dict(zip(labels_df.index, labels_df.ROI)), name="ROIs")
    nx.set_node_attributes(G, dict(zip(labels_df.index, labels_df.label)), name="label")
    nx.set_node_attributes(G, dict(zip(labels_df.index, labels_df.grouping)), name="grouping")
    nx.set_node_attributes(G, dict(zip(labels_df.index, labels_df.group_name)), name="group name")

    ### set up plot ###
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
    
    if not label:
        label="connectivity"

    annotate.colormapping(
        data=et["weight"],
        legend_kwargs={
            "shrink": 0.75,
            "pad": 0.25,
            "label": cbar_label
        },
        ax=ax,
        colorbar_max=cbar_max,
    )

    plots.despine()
    plots.rescale(G)
    plots.aspect_equal()

    fig = plt.gcf()

    return fig