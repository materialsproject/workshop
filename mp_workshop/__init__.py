def get_viewer_link(structure, host="https://viewer.materialsproject.org"):
    """
    Generate a link to view your structure online. For use within a
    Jupyter notebook environment.
    """
    from IPython.core.display import display, HTML
    import base64
    import zlib
    import webbrowser
    import urllib.parse
    payload = structure.to_json().encode('utf-8')
    payload = zlib.compress(payload)
    payload = base64.urlsafe_b64encode(payload).decode('ascii')
    payload = "?structure={}".format(payload)
    url = urllib.parse.urljoin(host, payload)
    display(HTML("<a href='{}' target='_blank'>Click to view structure.</a>".format(url)))

from crystal_toolkit.helpers.pythreejs_renderer import display_struct
