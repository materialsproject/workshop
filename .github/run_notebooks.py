""" Python script to run notebooks in the directory they exist in """
import os

import nbformat
import yaml
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError


run_on_master_only = ["04_materials_api", "06_new_systems"]


def recursive_get(items):
    if isinstance(items, dict):
        for v in items.values():
            yield from recursive_get(v)
    elif isinstance(items, list):
        for v in items:
            yield from recursive_get(v)
    else:
        yield items


with open("mkdocs.yml") as f:
    mkdocs_config = yaml.load(f)

notebooks = [
    item
    for item in recursive_get(mkdocs_config.get("nav", {}))
    if item.endswith(".ipynb")
]

if os.environ.get("PR", "") != "":
    notebooks = [
        nb for nb in notebooks if not any(avoid in nb for avoid in run_on_master_only)
    ]

os.chdir("workshop")
for notebook in notebooks:
    print(f"Loading {notebook}")
    nb = nbformat.read(notebook, as_version=4)

    for cell in nb.cells:
        if cell.get("cell_type", "") == "code" and "no-execute" in cell.get(
            "metadata", {}
        ).get("tags", []):
            cell["cell_type"] = "markdown"

    client = NotebookClient(
        nb,
        timeout=600,
        resources={"metadata": {"path": os.path.dirname(notebook)}},
    )
    try:
        client.execute()
        nbformat.write(nb, notebook)
    except CellExecutionError:
        msg = 'Error executing the notebook "%s".\n\n' % notebook
        print(msg)
        raise
