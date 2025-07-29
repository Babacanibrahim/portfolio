from flask import render_template, redirect, url_for ,request, flash, current_app
from .models import Project
from werkzeug.utils import secure_filename
from .forms import AddProjectForm
from . import db
import os


def register_routes(app):

    @app.route("/")
    def index():
        projects =Project.query.all()
        return render_template("index.html", projects = projects)
    

    @app.route("/about")
    def about():
        return render_template("about.html")
    
    @app.route("/project_detail/<int:id>")
    def project_detail(id):
        project = Project.query.filter_by(id = id).first()

        return render_template("project_detail.html", project = project)
    

    @app.route("/admin", methods = ["GET","POST"])
    def admin():
        form = AddProjectForm()
    
        if request.method == "POST" and form.validate():
            filename = None
            if form.image.data:
                image_file = form.image.data
                filename = secure_filename(image_file.filename)
                upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                image_file.save(upload_path)

            new_project = Project(
                title=form.title.data,
                description=form.description.data,
                github_link=form.github_link.data,
                image=filename,
            )
            db.session.add(new_project)
            db.session.commit()
            flash("Proje başarıyla eklendi.", "success")
            return redirect(url_for("admin"))

        return render_template("admin.html", form=form)
