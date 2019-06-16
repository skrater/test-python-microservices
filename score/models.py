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
    address = Column(String)
    date_of_birth = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    debt = relationship('Debt', back_populates='person')
    asset = relationship('Asset', back_populates='person')
    score = relationship('Score', back_populates='person')
    income = relationship('Income', back_populates='person')

    __table_args__ = (UniqueConstraint('cpf'),
                     )

    def __repr__(self):
        return f'<Person(cpf={self.cpf})>'

    @property
    def as_json(self):
        return person_schema.dump(self).data

    @property
    def event_name(self):
        return None


class PersonSchema(Schema):
    id = fields.Int(dump_only=True)
    cpf = fields.Int(required=True)
    address = fields.Str()
    date_of_birth = fields.DateTime(required=True)
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_person(self, data, **kwargs):
        return Person(**data)


person_schema = PersonSchema(strict=True)


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
        return None


class DebtSchema(Schema):
    id = fields.Int(dump_only=True)
    person_id = fields.Int(dump_only=True)
    value = fields.Float(required=True)
    created_at = fields.DateTime(dump_only=True)

    person = fields.Nested(PersonSchema, dump_only=True)

    @post_load
    def make_debt(self, data, **kwargs):
        return Debt(**data)


debt_schema = DebtSchema(strict=True)


class Score(Base):
    __tablename__ = 'score'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    person = relationship('Person', back_populates='score')

    def __repr__(self):
        return f'<Score(score={self.score})>'

    @property
    def as_json(self):
        return score_schema.dump(self).data

    @property
    def event_name(self):
        return 'score'


class ScoreSchema(Schema):
    id = fields.Int(dump_only=True)
    person_id = fields.Int(dump_only=True)
    score = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)

    person = fields.Nested(PersonSchema, dump_only=True)

    @post_load
    def make_score(self, data, **kwargs):
        return Score(**data)


score_schema = ScoreSchema(strict=True)


class Asset(Base):
    __tablename__ = 'asset'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    type = Column(String)
    value = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    person = relationship('Person', back_populates='asset')

    def __repr__(self):
        return f'<Asset(type={self.type},value={self.value})>'

    @property
    def as_json(self):
        return asset_schema.dump(self).data

    @property
    def event_name(self):
        return 'asset'


class AssetSchema(Schema):
    id = fields.Int(dump_only=True)
    person_id = fields.Int(dump_only=True)
    type = fields.String(required=True)
    value = fields.Float(required=True)
    created_at = fields.DateTime(dump_only=True)

    person = fields.Nested(PersonSchema, dump_only=True)

    @post_load
    def make_asset(self, data, **kwargs):
        return Asset(**data)


asset_schema = AssetSchema(strict=True)


class Income(Base):
    __tablename__ = 'income'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    type = Column(String)
    value = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    person = relationship('Person', back_populates='income')

    def __repr__(self):
        return f'<Income(type={self.type},value={self.value})>'

    @property
    def as_json(self):
        return income_schema.dump(self).data

    @property
    def event_name(self):
        return 'income'


class IncomeSchema(Schema):
    id = fields.Int(dump_only=True)
    person_id = fields.Int(dump_only=True)
    type = fields.String(required=True)
    value = fields.Float(required=True)
    created_at = fields.DateTime(dump_only=True)

    person = fields.Nested(PersonSchema, dump_only=True)

    @post_load
    def make_income(self, data, **kwargs):
        return Income(**data)


income_schema = IncomeSchema(strict=True)
