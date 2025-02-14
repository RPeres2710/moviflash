from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField
from wtforms.validators import DataRequired
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuração do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'rperes0510@gmail.com'  # Coloque seu e-mail
app.config['MAIL_PASSWORD'] = 'dfxg luwh jeig yjxa'  # Senha do seu app
app.config['MAIL_DEFAULT_SENDER'] = 'r.peres@movisafe-americalatina.com'  # E-mail de envio

mail = Mail(app)

# Definindo a chave secreta para proteger o formulário
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

# Criando o formulário de cadastro
class MoviflashForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    localidade = StringField('Localidade', validators=[DataRequired()])
    data = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    link = StringField('Link do Moviflash', validators=[DataRequired()])
    destinatarios = StringField('Destinatários (separados por vírgula)', validators=[DataRequired()])
    enviado = BooleanField('Enviado')

# Lista para armazenar os moviflash cadastrados
moviflash_list = []

# Função para enviar o e-mail
def send_email(link, destinatarios):
    try:
        # Destinatários podem ser passados em formato de lista
        recipients = [email.strip() for email in destinatarios.split(',')]  # Split e limpar e-mails
        msg = Message('Relatório Moviflash', recipients=recipients)
        msg.body = f"Prezados, segue o report de segurança para o seu conhecimento. Att.\n\nLink do Moviflash: {link}"
        mail.send(msg)
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MoviflashForm()

    if form.validate_on_submit():
        # Coletando dados do formulário
        moviflash = {
            'nome': form.nome.data,
            'localidade': form.localidade.data,
            'data': form.data.data,
            'link': form.link.data,
            'destinatarios': form.destinatarios.data,
            'enviado': form.enviado.data
        }
        # Adicionando na lista de moviflash
        moviflash_list.append(moviflash)
        return redirect(url_for('index'))  # Redireciona para a página principal
    
    return render_template('index.html', form=form, moviflash_list=moviflash_list)

@app.route('/enviar/<int:moviflash_id>', methods=['POST'])
def enviar_email(moviflash_id):
    moviflash = moviflash_list[moviflash_id]
    link = moviflash['link']
    destinatarios = moviflash['destinatarios']
    
    # Enviar o e-mail
    send_email(link, destinatarios)
    
    # Alterar o ícone para carta aberta
    moviflash['enviado'] = True
    
    return redirect(url_for('index'))

@app.route('/excluir/<int:moviflash_id>', methods=['POST'])
def excluir(moviflash_id):
    # Excluir o item da lista
    moviflash_list.pop(moviflash_id)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


