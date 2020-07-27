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

    runs = {
        "Si-structure optimization": fake_vasp_dir / "Si_structure_opt",
        "Si-static": fake_vasp_dir / "Si_static",
        "Si-nscf uniform": fake_vasp_dir / "Si_nscf_line",
        "Si-nscf line": fake_vasp_dir / "Si_nscf_uniform",
        "Si-elastic deformation 0": fake_vasp_dir / "Si_elastic_tensor" / "0",
        "Si-elastic deformation 1": fake_vasp_dir / "Si_elastic_tensor" / "1",
    }

    return use_fake_vasp(
        workflow,
        runs,
        check_incar=False,
        check_kpoints=False,
        check_poscar=False,
        check_potcar=False,
        clear_inputs=False,
    )
