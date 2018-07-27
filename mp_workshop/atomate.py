"""
Module containing helper code for the atomate lesson
"""

from graphviz import Digraph

def wf_to_graph(workflow):
    """
    Creates a directed acyclic graph corresponding
    to the workflow..

    Args:
        workflow (Workflow): workflow to be graphed

    """
    # Create the dag
    dot = Digraph(comment=workflow.name, graph_attr={"rankdir":'LR'})
    for fw in workflow.fws:
        dot.node(str(fw.fw_id), label=fw.name)

    for start, targets in workflow.links.items():
        for target in targets:
            dot.edge(str(start), str(target))
    return dot
