from flask import Flask, render_template,request, jsonify, session, redirect, url_for
from usuario import Usuario
from chat import Chat
from contato import Contato

app = Flask(__name__)

app.secret_key = "batatinhafrita123"


#Rota GET para o index ou cadastro
@app.route("/")
@app.route("/cadastro_via_form")
def pag_cadastro():
    return render_template("cadastro_via_form.html")

#Rota POST para o cadastro, ele pega os dados enviados via formulario
@app.route("/cadastro_via_form", methods=["POST"])
def post_cadastro():
    #Pegando os dados do form
    nome = request.form["nome"]
    telefone = request.form["telefone"]
    senha = request.form["senha"]

    #Instanciando o objeto usuário
    usuario = Usuario()
    
    #Cadastrando e retornando se deu certo ou não
    if usuario.cadastrar(nome, telefone, senha) == True:
        
        session['usuario_logado'] = {"nome":usuario.nome,
                                     "telefone":usuario.telefone}
        
        return "Cadastro efetuado com sucesso!"
    else:
        session.clear()
        
        return "Erro ao cadastrar"
    
    
    
    

#Rota GET para outra página de cadastro, essa realiza o cadastro usando requisição via post
@app.route("/cadastrar_via_ajax")
def pag_cadastro_ajax():
    return render_template("cadastro_via_ajax.html")



 
#Rota POST para o cadastro, ele pega os dados enviados via AJAX
@app.route("/cadastrar_via_ajax", methods=["POST"])
def post_cadastro_ajax():
    #Pegando os dados que foram enviados
    dados = request.get_json()
    
    nome = dados["nome"]
    telefone = dados["telefone"]
    senha = dados["senha"]
    
     #Instanciando o objeto usuário
    usuario = Usuario()
    
    #Cadastrando e retornando se deu certo ou não
    if usuario.cadastrar(nome, telefone, senha) == True:
        return jsonify({'mensagem':'Cadastro OK'}), 200
    else:
        return jsonify({'mensagem':'ERRO'}), 500
    
    
    
    
#Rota GET para mostrar a tela de login
@app.route("/login")
def pag_login():
    return render_template("login.html")



#Rota POST para verificar o usuário
@app.route("/login", methods=["POST"])
def pag_login_post():
    telefone = request.form["telefone"]
    senha = request.form["senha"]
    
    usuario = Usuario()
    
    usuario.logar(telefone,senha)
    
    if usuario.logado == True:
        session['usuario_logado'] = {"nome":usuario.nome,
                                     "telefone":usuario.telefone}
        return redirect("/chat")
    else:
        return redirect("/login")
    

#Rota GET para abrir a tela do chat se o usuário já estiver logado
@app.route("/chat")
def pag_chat():
    if "usuario_logado" in session :
        return render_template("chat.html")
    else:
        return redirect("/cadastro_via_form")



#Rota GET para retornar os usuários cadastrados em formato de JSON
@app.route("/retorna_usuarios")
def retorna_usuarios():
    
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario,telefone_usuario)
    
    contatos = chat.retornar_contatos()
    return jsonify(contatos), 200

@app.route("/get/mensagens/<tel_destinatario>")
def api_get_mensagens(tel_destinatario):
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario,telefone_usuario)

    destinatario = Contato("",tel_destinatario)
    mensagens = chat.verificar_mensagem(0,destinatario)
    return jsonify(mensagens), 200

@app.route("/enviar_mensagem", methods=["POST"])
def enviar_mensagem():
   
    # chamei os dados do ajax
        dados = request.get_json() 
        destinatario = dados["telefone"]
        mensagens = dados["mensagem"]
        # instaciei chat
        nome_usuario = session["usuario_logado"]["nome"]
        telefone_usuario = session["usuario_logado"]["telefone"]
        chat = Chat(nome_usuario,telefone_usuario)


        tel_destinatario = Contato("", destinatario)
        mensagem = chat.enviar_mensagem(mensagens,tel_destinatario)
        return jsonify(mensagem,tel_destinatario), 200
    
        
       

        


app.run(debug=True)

