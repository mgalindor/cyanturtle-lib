from abc import ABC, abstractmethod
from dataclasses import asdict

from dacite import from_dict

from cyanturtle.common import remove_none_in_dict


class Entity(ABC):

    @classmethod
    def from_dict(cls, data):
        return from_dict(data_class=cls, data=data)

    def to_dict(self):
        # return {key: value for key, value in asdict(self).items() if value}
        return remove_none_in_dict(asdict(self))


class Repository(ABC):

    @abstractmethod
    def create(self, **kwargs) -> str:
        """Overrides to create a record"""
        raise NotImplementedError("Not implemented create")

    @abstractmethod
    def find_by_id(self, id, **kwargs) -> dict:
        """Overrides to find a record by id"""
        raise NotImplementedError("Not implemented findById")

    @abstractmethod
    def update(self, id, **kwargs):
        """Overrides to update a record"""
        raise NotImplementedError("Not implemented update")

    @abstractmethod
    def delete_by_id(self, id, **kwargs):
        """Overrides to delete a record by id"""
        raise NotImplementedError("Not implemented deleteById")
