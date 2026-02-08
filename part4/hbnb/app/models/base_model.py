import uuid
from datetime import datetime
from sqlalchemy.orm.attributes import InstrumentedAttribute
from app.extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self.__class__, key):
                attr = getattr(self.__class__, key)
                if isinstance(attr, InstrumentedAttribute):
                    try:
                        setattr(self, key, value)
                    except Exception:
                        continue
                else:
                    setattr(self, key, value)
        self.updated_at = datetime.now()
        self.save()


def to_dict(self):
    dict_representation = {
        column.key: getattr(self, column.key)
        for column in self.__mapper__.columns
    }

    if hasattr(self, "created_at"):
        dict_representation["created_at"] = (
            self.created_at.isoformat() if self.created_at else None
        )
    if hasattr(self, "updated_at"):
        dict_representation["updated_at"] = (
            self.updated_at.isoformat() if self.updated_at else None
        )
    return dict_representation
