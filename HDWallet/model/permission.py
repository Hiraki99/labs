import sys
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from app import app
db = SQLAlchemy(app)


class Permission(db.Model):
    __tablename__ = 'Permission'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.String(125), db.ForeignKey('Role.id'))
    permission = db.Column(db.String(125), nullable=False,
                           default='guest')
    permissionID = db.Column(db.String(250), unique=True,  nullable=False)
    createAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updateAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, role_id, permission):
        self.role_id = role_id
        self.permission = permission
        self.permissionID = "%s-%s" % (role_id, permission)
        self.updateAt = datetime.utcnow()

    def __repr__(self):
        return '<Permission %r>' % self.permissionID
