import importlib
import os
import pkgutil
import json
from inspect import getmembers, isclass
from typing import Any

from flask import (
    Flask,
    jsonify,
    render_template,
    abort,
    request,
    send_from_directory,
    url_for,
)

import wepps
from wepps.app import App, ResponseError

import mistune
import emoji


def import_module(path):
    package = importlib.import_module(path)
    results = {}
    for loader, module_name, _ in pkgutil.walk_packages(package.__path__):
        module = loader.find_module(module_name).load_module(module_name)
        results[module_name] = module
    return results


class Site:
    def __init__(
        self,
        apps_path: str,
        application_root: str = "",
        enforce_dev_mode: bool = False,
        escape_html_in_md: bool = True,
        verbose: bool = False,
    ) -> None:
        self.apps_path = apps_path
        self.application_root = application_root
        self.enforce_dev_mode = enforce_dev_mode
        self.wepps_path = os.path.dirname(wepps.__file__)
        self.render_md = mistune.create_markdown(
            escape=escape_html_in_md,
        )
        self.verbose = verbose

        self.generate_apps()

        # Initialize the index text from the readme once, it doesn't change
        self.title, self.index_text = self.make_index_text("README.md")

        self.initialize_flask_server()

    def make_index_text(self, file: str, folder: str = "") -> tuple[str, str]:
        # Note that this conversion isn't really clean...
        if not os.path.exists(file):
            raise FileNotFoundError(f"{file} file couldn't be found!")

        raw = open(file).read()

        lines = raw.split("\n")
        title = lines[0][2:]  # Remove the hashtag at front

        content = "\n".join(lines[1:])

        # Convert relative links to webapps pages :
        content = content.replace("web_apps/", "")
        content = content.replace("/index.md", "")
        content = content.replace("(./", f"(./{folder}")
        if folder != "":
            content = content.replace(".md)", ")")

        text = emoji.emojize(self.render_md(content))

        return title, text

    def generate_apps(self) -> None:
        modules = import_module(self.apps_path)
        self.apps = {}
        for name, module in modules.items():
            apps = [
                a
                for a in getmembers(module)
                # If its a class, then check if its a subclass, but not the actual App-Class
                if isclass(a[1]) and issubclass(a[1], App) and a[1] != App
            ]
            if len(apps) == 1:
                self.apps[name] = apps[0][1]()  # Create an instance
            elif len(apps) > 1:
                raise RuntimeError(
                    f"In {name} are multiple apps defined! Only define one!"
                )
        if self.verbose:
            print(f"Found apps: {list(self.apps.keys())}")

    def initialize_flask_server(self) -> None:
        STATIC_FOLDER = f"{self.wepps_path}/static"
        self.flask_app = Flask(
            __name__,
            static_folder=STATIC_FOLDER,
            template_folder=f"{self.wepps_path}/templates",
        )

        def url_for_root(route: str, **kwargs) -> str:
            url = url_for(route, **kwargs)
            if self.application_root:
                url = f"{self.application_root}{url}"
            return url

        self.flask_app.jinja_env.globals.update(url_for_root=url_for_root)

        @self.flask_app.route("/")
        def index():
            return render_template("index.html", title=self.title, text=self.index_text)

        @self.flask_app.route("/favicon.ico")
        def favicon():
            return send_from_directory(
                os.path.join(self.flask_app.root_path, "static"),
                "favicon.ico",
                mimetype="image/vnd.microsoft.icon",
            )

        @self.flask_app.route("/assets/<file>")
        def assets(file):
            return send_from_directory(
                os.path.join(self.flask_app.root_path, "static", "assets"),
                file,
            )

        @self.flask_app.route("/doc/images/<file>")
        def doc(file):
            return send_from_directory(
                os.path.join(self.flask_app.root_path, "static", "doc", "images"),
                file,
            )

        # -----------
        # Subdirectory path apps
        # -----------

        @self.flask_app.route("/<app_path>")
        @self.flask_app.route("/<path:app_path>")
        def app_path_route(app_path):
            app_name = app_path.replace("/", ".")
            # First check if the app_path corresponds to an index file
            try:
                index_file_path = os.path.join(self.apps_path, app_path, "index.md")
                title, text = self.make_index_text(
                    index_file_path, folder=app_path + "/"
                )
            except FileNotFoundError:
                pass
            else:
                return render_template("index.html", title=title, text=text)

            # Otherwise check if its an app
            # If the app_name doesn't exist raise a 404
            if app_name not in self.apps.keys():
                abort(404)

            # Get the app title (raises an error if empty)
            app_title = self.apps[app_name].title

            json_file = ""
            css_file = ""
            if not self.enforce_dev_mode and os.path.exists(
                f"{STATIC_FOLDER}/manifest.json"
            ):
                manifest = json.load(open(f"{STATIC_FOLDER}/manifest.json", "r"))
                json_file = os.path.basename(manifest["src/main.tsx"]["file"])
                css_file = os.path.basename(manifest["src/main.css"]["file"])
                if self.verbose:
                    print("Using built js/css files!")

            # Then render the template and inject the corresponding documentation
            return render_template(
                "app.html", title=app_title, json_file=json_file, css_file=css_file
            )

        @self.flask_app.route("/<path:app_path>/compute", methods=["POST"])
        def app_path_compute(app_path):
            app_name = app_path.replace("/", ".")
            # If the app_name doesn't exist raise a 404
            if app_name not in self.apps.keys():
                abort(404)

            # Otherwise get the correct app
            request_json = request.json
            if self.verbose:
                print(request_json)
            request_data = None if not request_json else request_json
            try:
                docs, settings, plots = (
                    self.apps[app_name].compute(request_data).get_stages()
                )
            except ResponseError as e:
                return str(e), 400
            except Exception as e:
                return f"<b>Internal Error</b><br>{str(e)}", 400

            # Serialize them to objects
            docs = [stage.serialize() for stage in docs]
            settings = [stage.serialize() for stage in settings]
            plots = [stage.serialize() for stage in plots]
            return jsonify({"docs": docs, "settings": settings, "plots": plots})

        @self.flask_app.route("/<path:app_path>/documentation", methods=["GET"])
        def app_path_documentation(app_path):
            app_name = app_path.replace("/", ".")
            # If the app_name doesn't exist raise a 404
            if app_name not in self.apps.keys():
                abort(404)

            documentation = (
                "Sorry, but it seems that there is no dedicated documentation."
            )
            if os.path.exists(f"{self.apps_path}/{app_path}.md"):
                documentation = open(f"{self.apps_path}/{app_path}.md").read()
            return jsonify({"text": documentation})

    def wsgi(self) -> Flask:
        return self.flask_app

    def run(self) -> None:
        self.flask_app.run(debug=True, host="0.0.0.0", port=8000)
