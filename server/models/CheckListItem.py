from marshmallow import Schema, fields
from enum import Enum
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

# --- enum values ---
class Status(Enum):
  # when testing in postman, submit status as the listed key, not value. "PACKED", not "packed"
  PACKED = 'packed'
  NOT_PACKED = 'not packed'
  PLANNED = 'planned'

class CheckListItem(db.Model):
  __tablename__ = "checklistitem"

  id = db.Column(db.Integer, primary_key=True)
  item_name = db.Column(db.String, nullable=False)
  status = db.Column(db.Enum(Status), default=Status.NOT_PACKED)

  checklist_id = db.Column(db.Integer(), db.ForeignKey('checklists.id'), nullable=False)

  checklist = db.relationship('CheckList', back_populates='items')

  def __repr__(self):
    return f'Checklist Item {self.id}: {self.item_name}. Status {self.status}'
