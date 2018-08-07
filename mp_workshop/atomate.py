"""
Module containing helper code for the atomate lesson
"""
import os
import os.path
from graphviz import Digraph


os.environ["FW_CONFIG_FILE"] = "/home/jovyan/work/workshop-2018/mp_workshop/fireworks_config/FW_config.yaml"

si_struct_opt_path = os.path.join(os.path.dirname(__file__),"fake_vasp/Si_structure_opt")
si_static_path = os.path.join(os.path.dirname(__file__),"fake_vasp/Si_static")
si_nscf_line_path = os.path.join(os.path.dirname(__file__),"fake_vasp/Si_nscf_line")
si_nscf_uniform_path = os.path.join(os.path.dirname(__file__),"fake_vasp/Si_nscf_uniform")


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
