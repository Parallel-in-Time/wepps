from typing import Any
from enum import Enum

class WebType(Enum):
    Integer = "Integer"
    PositiveInteger = "PositiveInteger"
    StrictlyPositiveInteger = "StrictlyPositiveInteger"
    PositiveFloat = "PositiveFloat"
    Float = "Float"
    Enumeration = "Enumeration"
    FloatList = "FloatList"
    Boolean = "Boolean"


class Parameter:
    ids: list[str] = []  # Keep track of all ids to check for uniqueness.

    def __init__(
        self,
        unique_id: str,
        name: str,
        placeholder: str,
        doc: str,
        type: WebType,
        optional: bool,
        choices: list[str] | None,
        value: int | float | list[float] | str | None,
    ) -> None:
        """Create a new parameter.

        Args:
            unique_id (str): A unique and slugified id.
            name (str): The name of this parameter that will be displayed. Might be LaTeX Math (r'`\lam`').
            placeholder (str): The placeholder inside the parameter field.
            doc (str): The doc-string on hover.
            type (WebType): The type of this parameter.
            optional (bool): If the parameter is optional.
            choices (list[str] | None): Only if the WebType == Enumeration otherwise None.
            value (int | float | list[float] | str | None): If there exists a default value, then this value value should be set.
        """
        self.id: str = unique_id
        self.name: str = name
        self.placeholder: str = placeholder
        self.doc: str = doc
        self.type: WebType = type
        self.optional: bool = optional
        self.choices: list[
            str
        ] | None = choices  # None if this is not an enumeration type
        self.value: int | float | list[
            float
        ] | str | None = value  # None if no default value exists

    def serialize(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "placeholder": self.placeholder,
            "doc": self.doc,
            "type": self.type.value,
            "optional": self.optional,
            "choices": self.choices,
            "value": self.value,
        }

    def convert(self, value: str) -> Any:
        """Converts the value to the python type of this parameter.

        Args:
            value (str): The input value from the frontend as a string.

        Raises:
            NotImplementedError: If subclass doesn't implement it.

        Returns:
            Any: The python type of this parameter.
        """

        raise NotImplementedError("Conversion function not implemented!")


class Integer(Parameter):
    def __init__(
        self,
        unique_id: str,
        name: str,
        placeholder: str,
        doc: str,
        optional: bool,
        value: int | None = None,
    ) -> None:
        super().__init__(
            unique_id, name, placeholder, doc, WebType.Integer, optional, None, value
        )

    def convert(self, value: str) -> Any:
        return int(value)


class PositiveInteger(Parameter):
    def __init__(
        self,
        unique_id: str,
        name: str,
        placeholder: str,
        doc: str,
        optional: bool,
        value: int | None = None,
    ) -> None:
        super().__init__(
            unique_id,
            name,
            placeholder,
            doc,
            WebType.PositiveInteger,
            optional,
            None,
            value,
        )

    def convert(self, value: str) -> Any:
        return int(value)


class StrictlyPositiveInteger(Parameter):
    def __init__(
        self,
        unique_id: str,
        name: str,
        placeholder: str,
        doc: str,
        optional: bool,
        value: int | None = None,
    ) -> None:
        super().__init__(
            unique_id,
            name,
            placeholder,
            doc,
            WebType.StrictlyPositiveInteger,
            optional,
            None,
            value,
        )

    def convert(self, value: str) -> Any:
        return int(value)


class PositiveFloat(Parameter):
    def __init__(
        self,
        unique_id: str,
        name: str,
        placeholder: str,
        doc: str,
        optional: bool,
        value: float | None = None,
    ) -> None:
        super().__init__(
            unique_id,
            name,
            placeholder,
            doc,
            WebType.PositiveFloat,
            optional,
            None,
            value,
        )

    def convert(self, value: str) -> Any:
        return float(value)


class Float(Parameter):
    def __init__(
        self,
        unique_id: str,
        name: str,
        placeholder: str,
        doc: str,
        optional: bool,
        value: float | None = None,
    ) -> None:
        super().__init__(
            unique_id, name, placeholder, doc, WebType.Float, optional, None, value
        )

    def convert(self, value: str) -> Any:
        return float(value)


class Enumeration(Parameter):
    def __init__(
        self,
        unique_id: str,
        name: str,
        placeholder: str,
        doc: str,
        optional: bool,
        choices: list[str],
        value: str | None = None,
    ) -> None:
        super().__init__(
            unique_id,
            name,
            placeholder,
            doc,
            WebType.Enumeration,
            optional,
            choices,
            value,
        )

    def convert(self, value: str) -> Any:
        return value


class FloatList(Parameter):
    def __init__(
        self,
        unique_id: str,
        name: str,
        placeholder: str,
        doc: str,
        optional: bool,
        value: list[float] | None = None,
    ) -> None:
        super().__init__(
            unique_id, name, placeholder, doc, WebType.FloatList, optional, None, value
        )

    def convert(self, value: str) -> Any:
        return [float(v) for v in value.split(",") if v != ""]


class Boolean(Parameter):
    def __init__(
        self,
        unique_id: str,
        name: str,
        placeholder: str,
        doc: str,
        optional: bool,
        value: bool | None = None,
    ) -> None:
        super().__init__(
            unique_id, name, placeholder, doc, WebType.Boolean, optional, None, value
        )

    def convert(self, value: str) -> Any:
        return bool(value)
