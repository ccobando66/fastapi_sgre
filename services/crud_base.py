from .base_module import (
    Session, List,Column,
    Any
)

class CrudBase:
    def __init__(self, session:Session) -> None:
        self.__session = session
    
    def save_model_on_db(self,model) -> None:
        self.__session.add(model)
        self.__session.commit()
        self.__session.refresh(model)
    
    def get_model(self, model:object, column:Column, value:Any) -> object:
        return self.__session.query(model
                                    ).filter(column == value
                                    ).first()
    
    def get_many_models(self, model:object, skip:int, limit: int ) -> List[object]:
        return self.__session.query(model
                                    ).offset(skip
                                    ).limit(limit
                                    ).all()
                                    
    def create_model(self,model: object, schema:dict) -> None:
        model_db = model(**schema)
        self.save_model_on_db(model_db)
        
    def update_model(self,
                     model:object,
                     column:Column,
                     value:Any,
                     schema: dict
                     ) -> None:
        
        return self.__session.query(model
                                    ).filter(column == value
                                    ).update(schema)
    
    def delete_model(self,model:object) -> None:
        self.__session.delete(model)
        self.__session.commit()
    
    
    @property
    def get_session(self):
        return self.__session
    
    