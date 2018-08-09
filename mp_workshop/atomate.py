"""
Module containing helper code for the atomate lesson
"""

import os
from graphviz import Digraph
from fireworks import Firework, Workflow
from atomate.vasp.powerups import use_fake_vasp

# Copied from fws
state_to_color = {
    "RUNNING": "#F4B90B",
    "WAITING": "#1F62A2",
    "FIZZLED": "#DB0051",
    "READY": "#2E92F2",
    "COMPLETED": "#24C75A",
    "RESERVED": "#BB8BC1",
    "ARCHIVED": "#7F8287",
    "DEFUSED": "#B7BCC3",
    "PAUSED": "#FFCFCA"
}

os.environ["FW_CONFIG_FILE"] = "/home/jovyan/work/workshop-2018/mp_workshop/fireworks_config/FW_config.yaml"

si_struct_opt_path = os.path.join(os.path.dirname(__file__),"fake_vasp/Si_structure_opt")
si_static_path = os.path.join(os.path.dirname(__file__),"fake_vasp/Si_static")
si_nscf_line_path = os.path.join(os.path.dirname(__file__),"fake_vasp/Si_nscf_line")
si_nscf_uniform_path = os.path.join(os.path.dirname(__file__),"fake_vasp/Si_nscf_uniform")


def wf_to_graph(workflow):
    """
    Creates and renders a graph representation of a
    workflow and firework.  Workflows are rendered as the
    control flow of the fireworks, while Fireworks are
    rendered as a sequence of Firetasks.

    Args:
        workflow (Workflow or Firework): workflow or Firework
            to be rendered
    """
    # Create the dag
    dot = Digraph(comment=workflow.name, graph_attr={"rankdir":'LR'})
    dot.node_attr['shape'] = 'rectangle'
    if isinstance(workflow, Workflow):
        for fw in workflow.fws:
            dot.node(str(fw.fw_id), label=fw.name,
                     color=state_to_color[fw.state])

        for start, targets in workflow.links.items():
            for target in targets:
                dot.edge(str(start), str(target))
    elif isinstance(workflow, Firework):
        for n, ft in enumerate(workflow.tasks):
            # Clean up names
            name = ft.fw_name.replace('{', '').replace('}', '')
            name = name.split('.')[-1]
            dot.node(str(n), label=name)
            if n >=1:
                dot.edge(str(n - 1), str(n))
    return dot

module = os.path.dirname(os.path.abspath(__file__))


# Use this to streamline faking vasp if desired
def use_fake_vasp_workshop(workflow):
    """
    Wrapper around atomate's use_fake_vasp that will
    use designated directories in the workshop data
    store for the fake vasp in the workshop.

    Args:
    """
    if workflow.name == "Ag:elastic constants":
        runs_dir = os.path.join(module, "fake_vasp", "Ag_elastic_tensor")
        config = {"Ag-elastic deformation 0": os.path.join(runs_dir, "1"),
                  "Ag-elastic deformation 1": os.path.join(runs_dir, "2")}
        return use_fake_vasp(workflow, config)
    pass
