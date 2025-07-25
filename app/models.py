from . import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    description = db.Column(db.Text, nullable = False)
    github_link = db.Column(db.String)
    image = db.Column(db.String)