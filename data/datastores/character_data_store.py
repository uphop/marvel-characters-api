from data.datastores.session_helper import SessionHelper
from data.models.meta import Base
from data.models.character_model import Character
import logging
logger = logging.getLogger(__name__)

class CharacterDataStore:
    def create_character(self, id, name, description, modified, thumbnail_path, thumbnail_extension):
        # insert into data store and commit
        session = SessionHelper().get_session()
        try:
            session.add(Character(id=id, name=name, description=description, modified=modified, thumbnail_path=thumbnail_path, thumbnail_extension=thumbnail_extension))
            session.commit()
        except:
            session.rollback()

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
        try:
            session.query(Character).delete()
            session.commit()
        except:
            session.rollback()

    def get_character_last_modified(self):
        # select character by ID
        session = SessionHelper().get_session()
        return session.query(Character.modified).order_by(Character.modified.desc()).limit(1).one_or_none()

    def update_character(self, id, name, description, modified, thumbnail_path, thumbnail_extension):
        # update record in data store and commit
        session = SessionHelper().get_session()
        try:
            character = session.query(Character).filter(Character.id == id).one_or_none()
            character.name = name
            character.description = description
            character.modified = modified
            character.thumbnail_path = thumbnail_path
            character.thumbnail_extension = thumbnail_extension
            session.commit()
        except:
            session.rollback()




