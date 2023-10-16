from copy import deepcopy
from typing import Any

from wepps.stage.parameters import Parameter


class DocsStage:
    def __init__(
        self,
        title: str,
        text: str,
    ) -> None:
        self.title: str = title
        self.text: str = text

    def copy(self):
        """Returns a new DocsStage but as a copy.

        Returns:
            DocsStage. A new docs stage.
        """
        return DocsStage(
            self.title,
            self.text,
        )

    def serialize(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "text": self.text,
        }


class SettingsStage:
    def __init__(
        self,
        unique_name: str,
        title: str,
        parameters: list[Parameter],
        folded: bool,
    ) -> None:
        self.unique_name: str = unique_name
        self.title: str = title
        self.parameters: list[Parameter] = parameters
        self.folded: bool = folded

    def copy_from_response(self, response_data: dict[str, Any]):
        """Returns a new SettingsStage with updated parameter values.
        Used because of the stateless nature of the server.

        Args:
            response_data (dict[str, Any]): The response directly fed in from the frontend.

        Raises:
            KeyError: If there is no 'settings' key in the response_data

        Returns:
            SettingsStage: A new SettingsStage.
        """

        # Copy all parameters and set new default values
        parameters = deepcopy(self.parameters)
        for parameter in self.parameters:
            try:
                # Might raise another KeyError
                parameter.optional = response_data[parameter.id]
            except KeyError:  # If its from another
                raise KeyError(f'"{parameter.id}" not in response settings data!')

        return SettingsStage(self.unique_name, self.title, parameters, self.folded)

    def convert_to_types(self, response_data: dict[str, Any]) -> dict[str, Any]:
        result = {}
        for parameter in self.parameters:
            try:
                result[parameter.id] = parameter.convert(response_data[parameter.id])
            except KeyError:  # If for some reason this parameter doesn't exist
                print(
                    f"The parameter {parameter.id} doesn't exist. This might be a development problem."
                )
            except ValueError:  # If for some reason the conversion doesn't work
                print(
                    f"The parameter {parameter.id} = {response_data[parameter.id]} couldn't be converted. This might be a development problem."
                )
        return result

    def serialize(
        self,
    ) -> dict[str, Any]:  # Returns a dictionary to be sent to the frontend
        return {
            "id": self.unique_name,
            "title": self.title,
            "parameters": [parameter.serialize() for parameter in self.parameters],
            "folded": self.folded,
        }


class PlotsStage:
    def __init__(
        self,
        title: str,
        caption: str = "",
        plot: Any | None = None,
    ) -> None:
        self.title: str = title
        self.caption: str = caption
        self.plot: Any | None = plot

    def copy(self):
        """Returns a new PlotsStage but as a copy.

        Returns:
            PlotsStage. A new plots stage.
        """
        return PlotsStage(
            self.title,
            self.caption,
            self.plot,
        )

    def serialize(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "caption": self.caption,
            "plot": self.plot,
        }
