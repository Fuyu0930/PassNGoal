from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    #text = TextAreaField('Text', validators=[DataRequired()])
    text = CKEditorField('Text', validators=[DataRequired()])
    submit = SubmitField('Post')