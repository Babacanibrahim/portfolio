from flask import (
    render_template, redirect, url_for, request,
    flash, current_app, session
)
from .models import Project, Message
from werkzeug.utils import secure_filename
from .forms import AddProjectForm
from . import db
import os
from functools import wraps

# Login decoratoru
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash("Lütfen giriş yapın.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def register_routes(app):

    @app.route('/')
    def index():
        projects = Project.query.order_by(Project.created_at.desc()).all()
        return render_template('index.html', projects=projects)

    @app.route('/about')
    def about():
        return render_template('about.html')
    
    @app.route("/cv")
    def cv():
        return render_template("cv.html")

    @app.route('/project_detail/<int:id>')
    def project_detail(id):
        project = Project.query.filter_by(id=id).first_or_404()
        return render_template('project_detail.html', project=project)
    
    # İletişim
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')

            if not name or not email or not message:
                flash('Lütfen tüm alanları doldurun.', 'danger')
                return redirect(url_for('contact'))

            new_message = Message(name=name, email=email, content=message)
            db.session.add(new_message)
            db.session.commit()

            flash('Mesajınız başarıyla gönderildi, teşekkürler!', 'success')
            return redirect(url_for('contact'))

        return render_template('contact.html')


    # --- LOGIN ---
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if session.get('admin_logged_in'):
            return redirect(url_for('admin'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if (username == current_app.config['ADMIN_USERNAME'] and
                password == current_app.config['ADMIN_PASSWORD']):
                session['admin_logged_in'] = True
                flash('Başarıyla giriş yapıldı.', 'success')
                return redirect(url_for('admin'))
            else:
                flash('Kullanıcı adı veya şifre hatalı.', 'danger')

        return render_template('login.html')

    # ÇIKIŞ
    @app.route('/logout')
    @login_required
    def logout():
        session.pop('admin_logged_in', None)
        flash('Çıkış yapıldı.', 'info')
        return redirect(url_for('login'))

    # --- ADMIN PANEL ---
    @app.route('/admin')
    @login_required
    def admin():
        projects = Project.query.all()
        return render_template('admin.html', projects=projects)

    # Mesajları görme (okundu işareti buradan kaldırıldı)
    @app.route('/admin/messages')
    @login_required
    def messages():
        messages = Message.query.order_by(Message.created_at.desc()).all()
        for msg in messages:
            msg.is_read = True
        db.session.commit()
        return render_template('messages.html', messages=messages)

    # --- PROJE EKLEME ---
    @app.route('/add_project', methods=['GET', 'POST'])
    @login_required
    def add_project():
        form = AddProjectForm()
        if form.validate_on_submit():
            filename = None
            if form.image.data:
                image_file = form.image.data
                filename = secure_filename(image_file.filename)
                upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
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
            return redirect(url_for('admin'))

        return render_template('add_project.html', form=form)

    # --- PROJE DÜZENLEME ---
    @app.route('/edit_project/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_project(id):
        project = Project.query.filter_by(id=id).first_or_404()
        form = AddProjectForm(obj=project)

        if form.validate_on_submit():
            project.title = form.title.data
            project.description = form.description.data
            project.github_link = form.github_link.data

            if form.image.data:
                image_file = form.image.data
                filename = secure_filename(image_file.filename)
                upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
                image_file.save(upload_path)
                project.image = filename

            db.session.commit()
            flash("Proje başarıyla güncellendi.", "success")
            return redirect(url_for('admin'))

        return render_template('edit_project.html', form=form, project=project)

    # --- PROJE SİLME ---
    @app.route('/delete/<int:id>', methods=['POST'])
    @login_required
    def delete(id):
        project = Project.query.filter_by(id=id).first()
        if project:
            if project.image:
                image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], project.image)
                if os.path.exists(image_path):
                    os.remove(image_path)
            db.session.delete(project)
            db.session.commit()
            flash("Proje başarıyla silindi", "success")
        else:
            flash("Proje bulunamadı", "danger")
        return redirect(url_for('admin'))

    # --- CONTEXT PROCESSOR ---
    @app.context_processor
    def inject_is_admin():
        return dict(is_admin=session.get('admin_logged_in', False))
    
    # Mesaj sayısı bildirimi
    @app.context_processor
    def inject_globals():
        unread_message_count = Message.query.filter_by(is_read=False).count()
        return dict(is_admin=session.get("admin_logged_in", False), unread_message_count=unread_message_count)
