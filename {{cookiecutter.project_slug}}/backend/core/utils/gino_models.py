# -*- coding: utf-8 -*-
"""Gino models extra utils."""

from inspect import iscoroutinefunction


class JsonApiGinoModel:
    """Gino db Model extra utilities."""

    __attrs_to_skip = frozenset(("attributes", "id", "data", "type"))
    __crud_base_methods = frozenset(("update", "query", "create", "select", "delete"))

    @property
    def attributes(self):
        """Object attributes for pydantic models.

        JSON:API 1.0 specification says that we must provide
        `attributes` key with all object attributes excluding id.
        """
        result_dict = dict()
        for attr in dir(self):
            # exclude `private` attr
            if attr.startswith("_"):
                continue

            # exclude bounded GINO CRUD methods
            if attr in self.__crud_base_methods:
                continue

            # exclude `query` attr
            if attr.endswith("_query"):
                continue

            # exclude reserved attr
            if attr in self.__attrs_to_skip:
                continue

            # exclude callable methods
            if hasattr(self.__class__, attr) and callable(
                getattr(self.__class__, attr)
            ):  # noqa
                continue

            # get attr value
            attr_value = getattr(self, attr)

            # skip awaitable coroutines
            if iscoroutinefunction(attr_value):
                continue

            result_dict[attr] = attr_value

        return result_dict

    @property
    def type(self):  # noqa: A003
        """JSON:API spec type should be a db model name."""
        return self.__tablename__

    @property
    def data(self):
        """Object data for pydantic models.

        JSON:API 1.0 specification says that we must provide
        `data` key with `id`, `type` and `attributes`.
        """
        return {"id": self.id, "type": self.type, "attributes": self.attributes}
