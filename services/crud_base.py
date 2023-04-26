from .base_module import (
    Session, List,Column,
    Any
)

class CrudBase:
    def __init__(self, session:Session) -> None:
        self.__session = session
        
    #crud base models
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
    
    #function crud
    def verify_data(self, data:Any,**kwargs) -> str | object:
        count = 0
        
        for value in kwargs:
            
            if kwargs[value](data) is None and count == 0:
               return f"{data} no esta registrado en el sistema"
            
            if count == 0:
                get_data = kwargs[value](data)
            
            
            if kwargs[value](data) is not None and count !=0:
                return f"{data} ya esta registrado en el sistema o esta registrado con otro rol" 
            
            if len(kwargs) == count+1: 
                return get_data
            
            count+=1
        
            
    #setter        
    
    @property
    def get_session(self):
        return self.__session
    
    