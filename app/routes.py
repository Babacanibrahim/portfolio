from flask import render_template, redirect, url_for, request, flash, current_app, Response
from .models import Project
from werkzeug.utils import secure_filename
from .forms import AddProjectForm
from . import db
import os
from functools import wraps

#ADMİN GİRİŞİ
def check_auth(username, password):
    return username == current_app.config["ADMIN_USERNAME"] and password == current_app.config["ADMIN_PASSWORD"]

def authenticate():
    return Response(
        'Erişim için giriş yapmalısınız.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

#DECORATORS
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

#ROUTES
def register_routes(app):

    @app.route("/")
    def index():
        projects = Project.query.order_by(Project.created_at.desc()).all()
        return render_template("index.html", projects=projects)

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/project_detail/<int:id>")
    def project_detail(id):
        project = Project.query.filter_by(id=id).first()
        return render_template("project_detail.html", project=project)

    # PROJE DÜZENLEME
    @app.route("/edit_project/<int:id>", methods=["GET", "POST"])
    @requires_auth
    def edit_project(id):
        project = Project.query.filter_by(id=id).first_or_404()
        form = AddProjectForm()

        if request.method == "POST" and form.validate():
            project.title = form.title.data
            project.description = form.description.data
            project.github_link = form.github_link.data

            # Resim güncelleme
            if form.image.data:
                image_file = form.image.data
                filename = secure_filename(image_file.filename)
                upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                image_file.save(upload_path)
                project.image = filename

            db.session.commit()
            flash("Proje başarıyla güncellendi.", "success")
            return redirect(url_for("admin"))

        else:
            # Formu mevcut proje verileriyle doldur
            form.title.data = project.title
            form.description.data = project.description
            form.github_link.data = project.github_link

        return render_template("edit_project.html", form=form, project = project)
    
    # PROJE EKLEME
    @app.route("/add_project", methods=["GET", "POST"])
    @requires_auth
    def add_project():
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
            return redirect(url_for("add_project"))

        return render_template("add_project.html", form=form)
    

    #ADMİN SAYFASI
    @app.route("/admin", methods = ["GET","POST"])
    def admin ():
        projects = Project.query.all()

        return render_template("admin.html", projects = projects)
    
    # Proje Silme
    @app.route("/delete/<int:id>", methods =["POST"])
    @requires_auth
    def delete(id):
        project = Project.query.filter_by(id = id).first()
        if project:
            if project.image:
                image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], project.image)
                if os.path.exists(image_path):
                    os.remove(image_path)
            db.session.delete(project)
            db.session.commit()
            flash("Proje başarıyla silindi","success")
        else:
            flash("Proje bulunamadı", "danger")
        return redirect(url_for("admin"))
    
    #CONTEXT PROCESSOR
    @app.context_processor
    def inject_is_admin():
        auth = request.authorization
        if auth and auth.username == current_app.config["ADMIN_USERNAME"] and auth.password == current_app.config["ADMIN_PASSWORD"]:
            return dict(is_admin=True)
        return dict(is_admin=False)