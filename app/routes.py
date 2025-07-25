from flask import render_template, redirect, url_for
from .models import Project


def register_routes(app):

    @app.route("/")
    def index():
        return render_template("index.html")
    
    @app.route("/about")
    def about():
        return render_template("about.html")
    
    @app.route("/project_detail/<int:id>")
    def project_detail(id):
        return render_template("project_detail.html")