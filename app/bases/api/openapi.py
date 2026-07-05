import re

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import jsonify

from app.bases.api.resource import Resource

SWAGGER_UI_HTML = """<!doctype html>
<html>
  <head>
    <title>Form Management API docs</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
      window.onload = () => {
        window.ui = SwaggerUIBundle({ url: "/api/openapi.json", dom_id: "#swagger-ui" });
      };
    </script>
  </body>
</html>
"""

HTTP_METHOD_MAP = {"GET": "get", "POST": "post", "PUT": "put", "PATCH": "patch", "DELETE": "delete"}
PATH_PARAM_PATTERN = re.compile(r"<(?:[^:]+:)?(\w+)>")


def _to_openapi_path(flask_rule):
    return PATH_PARAM_PATTERN.sub(r"{\1}", flask_rule)


def _path_params(flask_rule):
    return PATH_PARAM_PATTERN.findall(flask_rule)


def _tag_for(flask_rule):
    parts = [p for p in flask_rule.split("/") if p and not p.startswith("<")]
    return parts[1] if len(parts) > 1 else "default"


def _schema_name_resolver(schema):
    """Every resource folder names its schemas Get/Post/Put/DeleteSchema (matching
    the HTTP method), so the default apispec resolver (which keys off the bare
    class name) collides constantly. Disambiguate using the schema's module path
    instead, e.g. app.api.forms.detail.schemas.PutSchema -> 'forms_detail_PutSchema'.
    """
    schema_cls = schema if isinstance(schema, type) else type(schema)
    module_parts = schema_cls.__module__.split(".")
    if "api" in module_parts:
        resource_path = "_".join(module_parts[module_parts.index("api") + 1 : -1])
    else:
        resource_path = schema_cls.__module__
    return f"{resource_path}_{schema_cls.__name__}"


def build_spec(app):
    spec = APISpec(
        title="Form Management API",
        version="1.0.0",
        openapi_version="3.0.3",
        info={"description": "REST API cho hệ thống quản lý form (admin tạo form, nhân viên submit)."},
        plugins=[MarshmallowPlugin(schema_name_resolver=_schema_name_resolver)],
    )
    spec.components.security_scheme("bearerAuth", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"})

    seen_rules = set()
    for rule in app.url_map.iter_rules():
        if rule.rule.startswith("/static") or rule.rule in seen_rules:
            continue

        view_class = getattr(app.view_functions[rule.endpoint], "view_class", None)
        if view_class is None or not issubclass(view_class, Resource):
            continue
        seen_rules.add(rule.rule)

        operations = {}
        for http_method, handler_class in view_class.method_handlers.items():
            path_params = [
                {"name": name, "in": "path", "required": True, "schema": {"type": "string"}}
                for name in _path_params(rule.rule)
            ]

            operation = {
                "tags": [_tag_for(rule.rule)],
                "responses": {"200": {"description": "OK"}},
            }
            if handler_class.auth_required:
                operation["security"] = [{"bearerAuth": []}]
            if handler_class.permission_requirements:
                operation["description"] = "Yêu cầu permission: " + ", ".join(handler_class.permission_requirements)

            schema_class = handler_class.input_schema_class
            if schema_class and http_method in ("GET", "DELETE"):
                operation["parameters"] = path_params + [{"in": "query", "schema": schema_class}]
            elif schema_class:
                operation["parameters"] = path_params
                operation["requestBody"] = {"content": {"application/json": {"schema": schema_class}}}
            else:
                operation["parameters"] = path_params

            operations[HTTP_METHOD_MAP[http_method]] = operation

        spec.path(path=_to_openapi_path(rule.rule), operations=operations)

    return spec.to_dict()


def register_docs(app):
    @app.get("/api/openapi.json")
    def openapi_json():
        return jsonify(build_spec(app))

    @app.get("/api/docs")
    def api_docs():
        return SWAGGER_UI_HTML
