[![Binder](https://mybinder.org/badge_logo.svg)](https://gke.mybinder.org/v2/gh/materialsproject/workshop/1.0.8)

## Materials Project Workshop

Assets for the Materials Project workshop.

*This repository is under development for our August 2019 workshop. There may be changes up until the day(s) of the workshop. Click [here](https://github.com/materialsproject/workshop/releases) for a snapshot of the 2018 workshop assets.*

## Tests

The following will check that all notebooks run properly.

```python
python setup.py install
pip install -r requirements.txt
python test.py
```

If you get an error like
> `jupyter_client.kernelspec.NoSuchKernel: No such kernel named <ENVNAME>`

then that notebook expects to be run using an IPython kernel with that name. With your Python environment activated, run
```
python -m ipykernel install --user --name <ENVNAME>
```
where `<ENVNAME>` is the name in the error message, e.g. `conda-env-mp-py`. This will ensure that the notebook uses your local environment. to run itself.

