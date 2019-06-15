from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, Float,
                        String, MetaData, ForeignKey,
                        DateTime, UniqueConstraint)
from marshmallow import Schema, fields, ValidationError, post_load


Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    cpf = Column(Integer)
    name = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    debt = relationship('Debt', back_populates='person')

    __table_args__ = (UniqueConstraint('cpf'),
                     )

    def __repr__(self):
        return f'<Person(cpf={self.cpf})>'

    @property
    def as_json(self):
        return person_schema.dump(self).data

    @property
    def event_name(self):
        return 'person.new'


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class PersonSchema(Schema):
    id = fields.Int(dump_only=True)
    cpf = fields.Int(required=True)
    name = fields.Str(required=True)
    address = fields.Str()
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_person(self, data, **kwargs):
        return Person(**data)


person_schema = PersonSchema()


# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class Debt(Base):
    __tablename__ = 'debt'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    value = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    person = relationship('Person', back_populates='debt')

    def __repr__(self):
        return f'<Debt(cpf={self.person.cpf},value={self.value})>'

    @property
    def as_json(self):
        return debt_schema.dump(self).data

    @property
    def event_name(self):
        return 'debt.new'


class DebtSchema(Schema):
    id = fields.Int(dump_only=True)
    person_id = fields.Int(dump_only=True)
    value = fields.Float(required=True)
    created_at = fields.DateTime(dump_only=True)

    person = fields.Nested(PersonSchema, validate=must_not_be_blank)

    @post_load
    def make_debt(self, data, **kwargs):
        return Debt(**data)


debt_schema = DebtSchema(strict=True)
