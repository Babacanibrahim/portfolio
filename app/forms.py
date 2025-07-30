from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms.validators import DataRequired

class AddProjectForm(FlaskForm):
    title = StringField('Başlık', validators=[DataRequired()])
    description = TextAreaField('Açıklama', validators=[DataRequired()])
    github_link = StringField('GitHub Linki')
    image = FileField('Kapak Fotoğrafı', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Sadece resim dosyaları!')])
    gallery = MultipleFileField('Galeri Fotoğrafları', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Sadece resim dosyaları!')])
    submit = SubmitField('Kaydet')
