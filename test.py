import unittest
from glob import glob
import tempfile
import subprocess
import os
import nbformat
from mp_workshop.atomate import wf_to_graph
from fireworks import LaunchPad


# Put any notebooks to be excluded here

EXCLUDE_NBS = {
    "lessons/atomate",
    "lessons/pymatgen"
}
module_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

EXPECTED_ERRORS = {
    "lessons/python_primer/5 - Lists.ipynb": 0, # Exception examples
    "lessons/python_primer/8 - Writing Functions.ipynb": 0, # Fill in example
}

class FireworksConfigTest(unittest.TestCase):
    def test_config(self):
        from fireworks.fw_config import LAUNCHPAD_LOC
        import nose; nose.tools.set_trace()
        lpad = LaunchPad.auto_load()
        self.assertEqual(lpad.fireworks.database.name, "mp_workshop")


class NotebookTest(unittest.TestCase):
    def setUp(self):
        # Get all ipynb files
        all_nbs = set(glob("lessons/**/*.ipynb"))
        # for path in all_nbs:
        self.nb_paths = [path for path in all_nbs
                         if not any([path.startswith(e) for e in EXCLUDE_NBS])]
        self.nb_paths = sorted(self.nb_paths)

    def test_nbs(self):
        for path in self.nb_paths:
            nb, errors = _notebook_run(os.path.join(module_dir, path))
            expected_errors = EXPECTED_ERRORS.get(path, 0)
            self.assertEqual(len(errors), expected_errors,
                             msg="Errors in nb {} found: {}".format(path, errors))


def _notebook_run(path):
    """
    Execute a notebook via nbconvert and collect output.

    Taken from
    https://blog.thedataincubator.com/2016/06/testing-jupyter-notebooks/

    Args:
        path (str): file path for the notebook object

    Returns: (parsed nb object, execution errors)

    """
    dirname, __ = os.path.split(path)
    os.chdir(dirname)
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=300",
                "--ExecutePreprocessor.allow_errors=True",
                "--output", fout.name, path]
        subprocess.check_call(args)

        fout.seek(0)
        nb = nbformat.read(fout, nbformat.current_nbformat)

    errors = [output for cell in nb.cells if "outputs" in cell
              for output in cell["outputs"]\
              if output.output_type == "error"]

    return nb, errors


if __name__ == "__main__":
    unittest.main()
