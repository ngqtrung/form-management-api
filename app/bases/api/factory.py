import importlib
import inspect
import os

from app.bases.api.resource import Resource


def install_resources(app, package_name="app.api"):
    """Walk `package_name` recursively, importing every subpackage's `__init__`
    module and registering every Resource subclass it defines (with a non-None
    `endpoint`) as a Flask url rule.
    """
    package = importlib.import_module(package_name)
    root_dir = os.path.dirname(package.__file__)
    root_pack = package.__name__.split(".")

    registered_names = set()

    for dir_path, dir_names, _file_names in os.walk(root_dir):
        dir_names[:] = [d for d in dir_names if d != "__pycache__"]

        rel = os.path.relpath(dir_path, root_dir)
        pack_parts = root_pack if rel == "." else root_pack + rel.replace(os.sep, "/").split("/")
        module_name = ".".join(pack_parts)

        module = importlib.import_module(module_name)

        for _name, candidate in inspect.getmembers(module, inspect.isclass):
            if not issubclass(candidate, Resource) or candidate is Resource:
                continue
            if not candidate.endpoint or candidate.__name__ in registered_names:
                continue
            registered_names.add(candidate.__name__)
            app.add_url_rule(candidate.endpoint, view_func=candidate.as_view(candidate.__name__))
