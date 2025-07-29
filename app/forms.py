from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, URL, Optional

class AddProjectForm(FlaskForm):
    title = StringField("Proje Başlığı",validators=[DataRequired(message="Proje başlığı gerekli")])
    description = TextAreaField("Proje Açıklaması", validators=[DataRequired()])
    github_link = StringField("GitHub Linki", validators=[Optional(), URL()])
    image = FileField("Proje Görseli", validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Sadece resim dosyaları yüklenebilir!')
    ])
    submit = SubmitField("Kaydet")