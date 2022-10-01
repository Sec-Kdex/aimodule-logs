from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import text, func, update
from sqlalchemy.orm import Session, load_only, Load
from ..aurora.aurora_model import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get_one(self, db: Session, code: Optional[Any] = None, where_clause: Optional[str] = None, column_load: Optional[List] = None) -> Optional[ModelType]:
        if code == None and where_clause == None:
            return None
        if where_clause == None:
            where_clause = f""" code='{code}' """
        if column_load == None:
            return db.query(self.model).filter(text(where_clause)).first()
        else:
            return db.query(self.model).options(load_only(*column_load)).filter(text(where_clause)).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 30
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def get_all(
        self,
        db: Session, 
        *, 
        where_clause: Optional[str] ="", 
        skip: Optional[int] = 0,
        limit: Optional[int] = 30,
        sorting_method: Optional[str] = "",
        column_load: Optional[List] = None
    ) -> List[ModelType]:
            if column_load == None:
                return db.query(self.model).filter(text(where_clause)).order_by(text(sorting_method)).offset(skip).limit(limit).all()
            else:
                return db.query(self.model).options(load_only(*column_load)).filter(text(where_clause)).order_by(text(sorting_method)).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:

            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def filter_update(
        self,
        db: Session,
        *,
        where_clause: str,
        update_values: dict
    ) -> ModelType:
        db.query(self.model).filter(text(where_clause)).update(update_values, synchronize_session='fetch')
        db.commit()
        return  

    def remove(
        self, 
        db: Session, 
        *, 
        code: Optional[str] = None,
        where_clause: Optional[str] = None
    ) -> ModelType:
        if code != None:
            obj = db.query(self.model).get(code)
            db.delete(obj)
            db.commit()
            return obj
        elif where_clause != None:
            db.query(self.model).filter(text(where_clause)).delete(synchronize_session=False)
            db.commit()
            db.commit()
        else:
            return
    
    def bulk_update(
        self, 
        db: Session,
        *,
        update_vals: List
    ) -> any:
        obj = db.bulk_update_mappings(self.model, update_vals)
        db.commit()
        return obj

    def get_all_with_single_join(
        self, 
        db: Session, 
        *, 
        where_clause: Optional[str] ="", 
        join_model: ModelType,
        column_load_1: Optional[List] = None,
        column_load_2: Optional[List] = None,
        sorting_method: Optional[str] = "",
        skip: Optional[int] = 0,
        limit: Optional[int] = 30
    ) -> any:
        if column_load_1 is not None and column_load_2 is not None:
            return db.query(self.model, join_model).options(Load(self.model).load_only(*column_load_1),Load(join_model).load_only(*column_load_2)).join(join_model).filter(text(where_clause)).offset(skip).limit(limit).all()
        elif column_load_1 is not None:
            return db.query(self.model, join_model).options(Load(self.model).load_only(*column_load_1)).join(join_model).filter(text(where_clause)).offset(skip).limit(limit).all()
        elif column_load_2 is not None:
            return db.query(self.model, join_model).options(Load(join_model).load_only(*column_load_2)).join(join_model).filter(text(where_clause)).offset(skip).limit(limit).all()
        else:
            return db.query(self.model, join_model).join(join_model).filter(text(where_clause)).offset(skip).limit(limit).all()
        
    
    def get_all_with_multiple_join(
        self, 
        db: Session, 
        *, 
        where_clause: Optional[str] = "", 
        join_model_1: ModelType,
        join_model_2: ModelType,
        join_model_3: Optional[ModelType] = None
    ) -> any:
        if join_model_3 == None:
            return db.query(self.model, join_model_1, join_model_2).select_from(self.model).join(join_model_1).join(join_model_2).filter(text(where_clause)).all()
        else:
            return db.query(self.model, join_model_1, join_model_2, join_model_3).select_from(self.model).join(join_model_1).join(join_model_2).join(join_model_3).filter(text(where_clause)).all()

    
    def call_postgres_function(
        self, 
        db: Session, 
        *, 
        query: str
    ) -> any:
        result = db.execute(text(query)).all()
        db.commit()
        return result