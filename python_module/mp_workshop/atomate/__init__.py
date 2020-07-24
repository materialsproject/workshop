"""
Module containing helper code for the atomate lesson
"""

from pathlib import Path

from atomate.vasp.powerups import use_fake_vasp
from fireworks import Firework, Workflow
from graphviz import Digraph


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
    "PAUSED": "#FFCFCA",
}


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
    dot = Digraph(comment=workflow.name, graph_attr={"rankdir": "LR"})
    dot.node_attr["shape"] = "rectangle"
    if isinstance(workflow, Workflow):
        for fw in workflow.fws:
            dot.node(str(fw.fw_id), label=fw.name, color=state_to_color[fw.state])

        for start, targets in workflow.links.items():
            for target in targets:
                dot.edge(str(start), str(target))
    elif isinstance(workflow, Firework):
        for n, ft in enumerate(workflow.tasks):
            # Clean up names
            name = ft.fw_name.replace("{", "").replace("}", "")
            name = name.split(".")[-1]
            dot.node(str(n), label=name)
            if n >= 1:
                dot.edge(str(n - 1), str(n))
    return dot


fake_vasp_dir = (Path(__file__).parent / "fake_vasp").resolve()


# Use this to streamline faking vasp if desired
def use_fake_vasp_workshop(workflow):
    """
    Wrapper around atomate's use_fake_vasp that will
    use designated directories in the workshop data
    store for the fake vasp in the workshop.

    Args:
    """
    if workflow.name == "Si:elastic constants":
        runs_dir = fake_vasp_dir / "Si_elastic_tensor"
        config = {
            "Si-elastic deformation 0": runs_dir / "0",
            "Si-elastic deformation 1": runs_dir / "1",
        }
        return use_fake_vasp(workflow, config)
    elif "Al" in workflow.name or "Cr" in workflow.name:
        # statements of each structure
        struct_start = workflow.fws[0].tasks[0]["structure"]
        subdir_name = f"{str(struct_start.composition).replace(' ', '')}_{struct_start.lattice.matrix[0][0]:0.2f}"
        fw_name = (
            f"{str(struct_start.composition.reduced_formula)}-structure optimization"
        )
        # the firework will always have the same name
        runs_dir = fake_vasp_dir / "Al_Cr"
        config = {fw_name: runs_dir / subdir_name}
        return use_fake_vasp(workflow, config)
    else:
        raise ValueError("Workflow {} not found".format(workflow.name))
