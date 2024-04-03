from typing import Dict
from RocketSeat.NLW.src.models.settings.connection import db_connection_handler
from RocketSeat.NLW.src.models.entities import Events
from sqlalchemy.exc import IntegrityError, NoResultFound


class EventsRepository:
    def insert_event(self, eventsInfo: Dict) -> Dict:
        with db_connection_handler as database:
            try:
                event = Events(
                    id=eventsInfo.get("uuid"),
                    title=eventsInfo.get("title"),
                    details=eventsInfo.get("details"),
                    slug=eventsInfo.get("slug"),
                    maximum_attendees=eventsInfo.get("maximum_attendees")
                )
                database.session.add(event)
                database.session.commit()

                return eventsInfo
            except IntegrityError:
                raise Exception('Evento já cadastrado!')
            except Exception as exception:
                database.session.rollback()#Deu problema -> Volta pro estado anterior
                raise exception


    def get_event_by_id(self, event_id: str) -> Events: #Query
        with db_connection_handler as database:
            try:
                event = (
                    database.session
                        .query(Events)
                        .filter(Events.id == event_id)
                        .one()
                )
                return event
            except NoResultFound:
                return None #Caso o id não esteja, não faz nada
