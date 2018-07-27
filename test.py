import unittest
from glob import glob
import tempfile
import subprocess
import os
import nbformat


# Put any notebooks to be excluded here

EXCLUDE_NBS = {
    "lessons/atomate",
    "lessons/pymatgen"
}
module_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

class NotebookTest(unittest.TestCase):
    def setUp(self):
        # Get all ipynb files
        all_nbs = set(glob("lessons/**/*.ipynb"))
        # for path in all_nbs:
        self.nb_paths = [path for path in all_nbs 
                         if not any([path.startswith(e) for e in EXCLUDE_NBS])]
        self.nb_paths = sorted(self.nb_paths)
        self.nb_paths = [os.path.join(module_dir, path) for path in self.nb_paths]

    def test_nbs(self):
        for path in self.nb_paths:
            nb, errors = _notebook_run(path)
            self.assertIsNone(errors, "Errors in nb {} found: {}".format(
                path, errors))


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
