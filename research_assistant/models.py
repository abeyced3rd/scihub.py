from datetime import datetime
from . import db


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(1024), nullable=False)
    extracted_text = db.Column(db.Text)
    source_url = db.Column(db.String(1024))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    chapters = db.relationship('Chapter', backref='material', cascade='all,delete-orphan')


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=True)
    order = db.Column(db.Integer, default=0)
    sections = db.relationship('Section', backref='chapter', cascade='all,delete-orphan')


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
