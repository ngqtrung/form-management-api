import importlib
import inspect

from flask import g, request
from flask.views import View

from app.auth.decorators import load_current_user
from app.bases.api.method_handler import MethodHandler

HTTP_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")


class MetaResource(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        # the sibling `methods` module must be defined in the resource
        # directory; all the method handler classes are declared there.
        methods_module_path = cls.__module__ + ".methods"
        try:
            methods_module = importlib.import_module(methods_module_path)
        except ModuleNotFoundError:
            return

        method_handlers = {}
        for cls_name, candidate in inspect.getmembers(methods_module, inspect.isclass):
            if not issubclass(candidate, MethodHandler) or candidate is MethodHandler:
                continue
            if cls_name.upper() not in HTTP_METHODS:
                continue
            method_handlers[cls_name.upper()] = candidate

        cls.method_handlers = method_handlers
        if method_handlers:
            cls.methods = tuple(method_handlers.keys())


class Resource(View, metaclass=MetaResource):
    # the endpoint (URL rule) of the resource; if None, this resource is
    # never registered (base classes / abstract resources).
    endpoint = None

    # a dict of {HTTP_METHOD: MethodHandler subclass}, filled in by MetaResource.
    method_handlers = {}

    def dispatch_request(self, **url_params):
        handler_class = self.method_handlers[request.method.upper()]

        current_user = load_current_user() if handler_class.auth_required else None
        if current_user is not None:
            g.current_user = current_user

        handler = handler_class(request=request, current_user=current_user, url_params=url_params)
        return handler.run()
