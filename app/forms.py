from http.client import PRECONDITION_FAILED
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, FileField, SelectField
from wtforms.validators import DataRequired
from json import load

with open('./JSONFiles/mercadinho.json','r') as f:
    mercadinho = load(f)
    escolha = []
for tipo in mercadinho['mercado']:
    escolha.append(tipo['tipo'])

class CadastroProduto(FlaskForm):
    tipo = SelectField('Tipo', validators=[DataRequired()], default = "", choices=escolha)
    nome = StringField('Nome', validators=[DataRequired()])
    preco = StringField('Preco', validators=[DataRequired()])
    descricao = StringField('Descricao', validators=[DataRequired()])
    quantidade = FloatField('Quantidade', validators=[DataRequired()])
    imagem  =FileField('imagem', validators=[DataRequired()])
    submit = SubmitField('Manda ae paizao')