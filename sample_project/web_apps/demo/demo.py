from typing import Any

from wepps.app import App, ResponseStages, ResponseError
import wepps.stage.stages as stages
from wepps.stage.parameters import (
    Integer,
    PositiveInteger,
    StrictlyPositiveInteger,
    PositiveFloat,
    Float,
    Enumeration,
    FloatList,
    Boolean,
)

import plotly.graph_objects as go

# ===================
# Documentation Stage
# ===================

d1_docs_text = r"""
Test equation with a $\phi \in \mathbb{R}$
$$
\begin{align*}
x^2 + y^2 &= 1 \\\\
y &= \sqrt{1 - x^2}.
\end{align*}
$$
"""

d1_docs = stages.DocsStage(
    "The first documentation stage",
    d1_docs_text,
)

d2_docs = stages.DocsStage(
    "2nd docs stage",
    r"""
Here are information for another part, maybe the second settings stage or the plots.


$$
\alpha + \frac{2\beta}{\gamma}
$$
""",
)

# ==============
# Settings Stage
# ==============

s1_params = [
    Integer(
        "i",
        r"$i$",
        r"Placeholder no latex: $\alpha$",
        r"Hover docs (no latex: $\phi$)",
        False,
    ),
    StrictlyPositiveInteger(
        "phi",
        r"$\phi$",
        "Placeholder: for StrictlyPositiveInteger",
        r"Hover docs",
        False,
    ),
    Enumeration(
        "option",
        "Option",
        "Placeholder: for Enumeration",
        r"Hover docs",
        False,
        ["A", "B", "C"],
        "B",
    ),
    Boolean(
        "b",
        r"$\text{A boolean value}$",
        "Placeholder: for Boolean",
        r"Hover docs",
        False,
        True,
    ),
]
s2_params = [
    PositiveInteger(
        "xi", r"$\xi$", "Placeholder: for PositiveInteger", r"Hover docs", False
    ),
    StrictlyPositiveInteger(
        "Phi",
        r"$\Phi$",
        "Placeholder: for StrictlyPositiveInteger",
        r"Hover docs",
        False,
    ),
    PositiveFloat(
        "alpha",
        r"$\alpha_{\beta - 2}^3$",
        "Placeholder: for PositiveFloat",
        r"Hover docs",
        False,
    ),
    Float("rho", r"$\rho$", "Placeholder: for Float", r"Hover docs", False),
    Enumeration(
        "selection",
        "Selection",
        "Placeholder: for Enumeration",
        r"Hover docs",
        False,
        ["First", "Second", "Third"],
    ),
    FloatList("n", r"$n$", r"Placeholder: for FloatList", r"Hover docs", False),
    Boolean("b", r"$\mathbb{B}$", "Placeholder: for Boolean", r"Hover docs", False),
]

s1_settings = stages.SettingsStage("S1", "Open Stage", s1_params, False)

s2_settings = stages.SettingsStage("S2", "Folded Stage", s2_params, True)

# ===========
# Plots Stage
# ===========

# If the plot stage has a caption but no plot (=None),
# then the caption will be displayed in large as a result
# including multiline equations
p1_plots = stages.PlotsStage(
    "Contour",
    r"""
Test equation with a $\phi \in \mathbb{R}$
$$
\begin{align*}
x^2 + y^2 &= 1 \\\\
y &= \sqrt{1 - x^2}.
\end{align*}
$$
""",
    None,
)

# If both, a plot and a caption are set, then the caption will
# be diplayed as a caption (see at the bottom where `.caption = ...`)

# If only a plot is set without a caption, then only the plot will be displayed

# If both are empty, then 'No plot computed' will be displayed
p2_plots = stages.PlotsStage("Plot 2")

# =============
# Dummy figures
# =============


def dummy_fig_1():
    fig = go.Figure(
        data=go.Contour(
            z=[
                [10, 10.625, 12.5, 15.625, 20],
                [5.625, 6.25, 8.125, 11.25, 15.625],
                [2.5, 3.125, 5.0, 8.125, 12.5],
                [0.625, 1.25, 3.125, 6.25, 10.625],
                [0, 0.625, 2.5, 5.625, 10],
            ],
        )
    )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    return fig.to_json()


# ====================================================
#                     Demo App
# ====================================================


class Demo(App):
    def __init__(self) -> None:
        super().__init__(title="API Demonstration")

    def compute(self, response_data: dict[str, Any] | None) -> ResponseStages:
        # Create a response, where stages will be added to
        r = ResponseStages()

        # If response_data == None, then its the initial request
        if not response_data:
            r.add_docs_stage(d1_docs)
            r.add_docs_stage(d2_docs)
            r.add_settings_stage(s1_settings)
            r.add_plot_stage(p1_plots)
            r.add_plot_stage(p2_plots)
            return r

        # Otherwise, there is data:
        # A dictionary filled with the settings stages id
        # and then the parameters id, e.g.
        # response_data['S1']['i'] <- contains the value of the parameter

        # But as all of those values are currently str, we can convert them
        # Each stage has to be converted individually, as only the stage
        # knows the types corresponding to each parameter in a stateless manner
        S1_data = s1_settings.convert_to_types(response_data["S1"])
        if "S2" in response_data.keys():
            S2_data = s2_settings.convert_to_types(response_data["S2"])
            print(S2_data)

        # Imagine someone filled a field with some unrealistic value,
        # just raise an Exception to display an error message.
        try:
            if S1_data["i"] > 15:
                # This can be raised anywhere in this function to display an error
                raise ResponseError('Test error: "i" is larger than 15.')
        except ResponseError:
            raise
        except Exception as e:
            # Just to be sure, wrap the conversion in a try/except block
            # If i is set as an integer, then it can't be filled with something else.
            # TODO: This conversion might automatically happen in the flask backend.
            raise ResponseError(f"Unknown Error: {str(e)}")

        # === Fill stages with data ===

        # --- Docs
        # If data needs to be changed a copy must be created.
        # Otherwise, the base data will be changed for *all* requests,
        # i.e. also for requests that did not send the correct input values.
        docs_d1 = d1_docs.copy()
        docs_d1.text += f"\n\n*Some added information*"

        r.add_docs_stage(docs_d1)  # Changed data
        r.add_docs_stage(d2_docs)  # Unchanged data

        # --- Settings
        # Create a copy with the values from the response,
        # so that there is no global change of the parameters for another request.
        # Same reasoning as for the docs.
        # !!! Note, that for parameter values to stay the same after computation,
        #     a copy must be made.
        # Example:
        #    i = 0 (default)
        # -> i = 3 (frontend input)
        # -> Computation in this function
        #    No copy               | Copy
        # i = 0 (reset to default) | i = 3 (remains the same)
        s1_settings_edited = s1_settings.copy_from_response(response_data["S1"])
        # Then we can also change parameter values (currently only in list format, might change...)
        s1_settings_edited.parameters[0].value = 5

        r.add_settings_stage(s1_settings_edited)

        # Add another stage, that wasn't there before
        r.add_settings_stage(s2_settings)

        # --- Plots
        # Set the figure data
        plot_p1 = p1_plots.copy()
        plot_p1.plot = dummy_fig_1()
        plot_p1.caption = r"Informative caption $\alpha^4$ with $\phi \in \mathbb{R}$"

        # We can also dynamically change the title
        plot_p2 = p2_plots.copy()
        plot_p2.title += " (new)"
        plot_p2.plot = dummy_fig_1()

        r.add_plot_stage(plot_p1)
        r.add_plot_stage(plot_p2)

        # Then return the stages
        return r
