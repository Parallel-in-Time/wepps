# Wepps

A web app framework to connect python projects to a simple but interactive frontend.

## Usage

The framework is build upon the idea of having different web apps inside a folder that can be addressed from the index page.

So, install the library using

```sh
pip install wepps
```

and copy the sample project from [here](https://github.com/Parallel-in-Time/wepps/tree/main/sample_project).

If you want to start from scratch, create a python file that looks something like

```python
from wepps import Site

if __name__ == "__main__":
    site = Site(apps_path="web_apps")
    site.run()
```

The `apps_path` is the name of the directory next to the python file.
Also, next to the python file should be a `README.md` which will be used as the index page.
Note that the path links inside there should be connected to the web apps structure, so if you have a subdirectory such as `web_apps/complex/index.md`, then use `[complex](/complex)` in markdown or `[app](/interesting/thing)` for `web_apps/interesting/thing.py`.

Inside of the `apps_path`, here `web_apps` should be an empty `__init__.py` to make it a python module and some directories which serve as topic directories for the web apps inside of it.
In each of these directories should also be the obligatory `__init__.py` as well as an `index.md` file that displays information about the spefic topic.
Each web app has a python and a markdown file with the same name; the markdown file serves as the documentation text for the specific web app.

One example `web_apps` structure might look like this:

```
├── main.py
├── README.md
└── web_apps
   ├── __init__.py
   └── demo
      ├── __init__.py
      ├── demo.md
      ├── demo.py
      └── index.md
```

The individual web apps (such as `demo.py`) should always have the basic following structure

```python
from wepps.app import App, ResponseStages
import wepps.stage.stages as stages
from wepps.stage.parameters import PositiveInteger


d1_docs = stages.DocsStage("Title", "Some markdown/LaTeX documentation.")
s1_params = [PositiveInteger("xi", r"$\xi$", "Placeholdertext", r"Hover docs", False)]
s1_settings = stages.SettingsStage("unique_id", "Title", s1_params, False)
p1_plots = stages.PlotsStage("Title", "Some descriptive text.", None)

class Demo(App):
    def __init__(self) -> None:
        super().__init__(title="API Demonstration")

    def compute(self, response_data):
        r = ResponseStages()
        r.add_docs_stage(d1_docs)
        r.add_settings_stage(s1_settings)
        r.add_plot_stage(p1_plots)
        return r
```

All classes that inherit from the `wepps.app.App` will be displayed as individual web apps and linked at their folder position.
So if the folder structure is `web_apps/first/computation.py`, the url of this app will be `/first/computation`.

For detailed information on what you can do and how you can react to changes, please have a look at [this example](https://github.com/Parallel-in-Time/wepps/blob/main/sample_project/web_apps/demo/demo.py).

## Frontend Development

The frontend is built using Typescript and uses vite as a build tool.
The backend uses by default the latest build of vite, i.e., the single Javascript file, if the `enforce_dev_mode` flag in `web.py` isn't set explicitly to `True` such as `Site(..., enforce_dev_mode=True)`.
To use the latest Typescript files (if anything was changed and wasn't build yet), one has to set the flag to `True` and start the vite development server.

For this cd into the `src/frontend` folder and enter

```sh
yarn
yarn dev
```

and start the backend from another project with the `enforce_dev_mode=True` flag .
For this, the `sample_project` is probably a good start and can be altered to check the improvements etc.

### Building

The project can be built inside the `wepps/frontend` folder with

```sh
yarn
yarn build
```

The files created this way will automatically be picked up by the frontend from the created `src/wepps/static/manifest.json` and are used by default.
Currently, the build process doesn't delete old js files, so from time to time the files that aren't explicitly in the `manifest.json` file can be safely deleted.
