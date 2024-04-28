from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class HostelsForm(FlaskForm):
    #мне лень тут расписывать. Сделайте ппжпж
    Websites = StringField('Сайты', validators=[DataRequired()])
    Title = StringField('Заголовок', validators=[DataRequired()])
    Description = StringField('Описание', validators=[DataRequired()])
    Cell_phones = StringField('Сотовые телефоны', validators=[DataRequired()])
    Landline_phones = StringField('Городские телефоны', validators=[DataRequired()])
    Email = StringField('Электронная почта', validators=[DataRequired()])
    Region = StringField('Регион', validators=[DataRequired()])
    Locality = StringField('Локация', validators=[DataRequired()])
    VK = StringField('VK', validators=[DataRequired()])
    Instagram = StringField('Instagram', validators=[DataRequired()])
    Facebook = StringField('Facebook', validators=[DataRequired()])
    WhatsApp = StringField('WhatsApp', validators=[DataRequired()])
    Viber = StringField('Viber', validators=[DataRequired()])
    YouTube = StringField('YouTube', validators=[DataRequired()])
    Telegram = StringField('Telegram', validators=[DataRequired()])
    Twitter = StringField('Twitter', validators=[DataRequired()])
    submit = SubmitField('Применить')