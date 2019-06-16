from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, Float,
                        String, MetaData, ForeignKey,
                        DateTime)
from marshmallow import Schema, fields, post_load


Base = declarative_base()


class Score(Base):
    __tablename__ = 'score'

    id = Column(Integer, primary_key=True)
    cpf = Column(Integer)
    type = Column(String)
    value = Column(Float)
    score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

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
    cpf = fields.Int(required=True)
    type = fields.String(required=True)
    value = fields.Float(required=True)
    score = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_score(self, data, **kwargs):
        return Score(**data)


score_schema = ScoreSchema(strict=True)
