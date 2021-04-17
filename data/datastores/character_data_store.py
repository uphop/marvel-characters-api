from data.datastores.session_helper import SessionHelper
from data.models.meta import Base
from data.models.character_model import Character
import logging
logger = logging.getLogger(__name__)

class CharacterDataStore:
    def create_character(self, id, name, description, modified, thumbnail_path, thumbnail_extension):
        # insert into data store and commit
        session = SessionHelper().get_session()
        session.add(Character(id=id, name=name, description=description, modified=modified, thumbnail_path=thumbnail_path, thumbnail_extension=thumbnail_extension))
        session.commit()

    def get_characters(self):
        # select all characters
        session = SessionHelper().get_session()
        return session.query(Character.id).all()

    def get_character_by_id(self, id):
        # select character by ID
        session = SessionHelper().get_session()
        return session.query(Character.id, Character.name, Character.description, Character.modified, Character.thumbnail_path, Character.thumbnail_extension).filter(Character.id == id).one_or_none()

    def delete_characters(self):
        # delete records from data store and commit
        session = SessionHelper().get_session()
        session.query(Character).delete()
        session.commit()


