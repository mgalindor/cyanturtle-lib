from abc import ABC

from google.cloud import firestore
from werkzeug.exceptions import NotFound

from cyanturtle.common import ObjectId
from cyanturtle.persistence import Repository as BaseRepository


class Repository(BaseRepository, ABC):

    def __init__(self, collection: str):
        self.__db = firestore.Client()
        self.collection = collection

    def create(self, **kwargs) -> str:
        """ Method to create a document in GCP Firestore

        Args:
            kwargs (dict): Dictionary which is the document body

        Raises:
            Conflict : If document_id is provided and the document already exists.

        Returns:
            (string): Id of the new object
        """
        oid = str(ObjectId())
        self._collection_reference().document(oid).set(kwargs)
        return oid

    def find_by_id(self, id, **kwargs) -> dict:
        """ Method to find a document by id in GCP Firestore

        Args:
            id (string): Id of the document

        Raises:
            NotFound: in case not found the document

        Returns:
            (dict): A dict with the document information
        """
        documentReference = self._collection_reference().document(id)
        documentSnapshot = documentReference.get()
        if not documentSnapshot.exists:
            raise NotFound()
        return documentSnapshot.to_dict()

    def update(self, id, **kwargs):
        """ Method to update a document in GCP Firestore for more information see
        https://cloud.google.com/firestore/docs/manage-data/add-data#update-data

        Args:
            id (string): Id of the dictionary
            kwargs (dict): Dictionary which has the updated values of the document body
            it can be partial or full replacement

        Raises:
            NotFound  : If the document does not exist.

        Returns:
            (string): Id of the new object
        """
        documentReference = self._collection_reference().document(id)
        documentReference.update(kwargs)

    def delete_by_id(self, id, **kwargs):
        """ Method to delete a document in GCP Firestore by id

        Args:
            id (string): Id of the dictionary

        Raises:
            NotFound  : If the document does not exist.

        Returns:
            (string): Id of the new object
        """
        self._collection_reference().document(id).delete()

    def _collection_reference(self):
        return self.__db.collection(self.collection)
