import mysql.connector
from flask import Flask, render_template, request, url_for


#=============================================#

app = Flask(__name__)

##############################################################################################################
############################################## ROTAS DO USUARIO ##############################################
##############################################################################################################

@app.route("/")
def login_screen():
    return render_template("tela_login.html")

@app.route('/login_usuario', methods=['POST'])
def login_usuario():
    nome = request.form['nome_cliente']
    senha = request.form['senha_cliente']

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '@Refri198',
        database = 'bd_livraria',
    )
    
    cursor = conexao.cursor(prepared=True)
    sql = f'SELECT * FROM cliente WHERE nome = %s AND cpf = %s '
    valores = (nome, senha)
    cursor.execute(sql, valores)
    resultado = cursor.fetchall() # Ler o banco de dados
    conexao.close()

    if(nome == 'admin' and senha == 'admin'): # Se for o admin logando, mande ele para o painel de admin
        return render_template("homepage_admin.html")
    else:
        if resultado:
        # Login bem sucedido
            return render_template("homepage_cliente.html")
        else:
        # Login mal sucedido
            return render_template("tela_login.html")

    
#==============================================================================#
@app.route("/Cadastre-se.html") #CREATE
def pagina_cadastrarCliente():
    return render_template("Cadastre-se.html")

#envio feito pelo cliente, na pagina de login
@app.route('/submit_cliente', methods=['POST'])
def submit_cliente():
    name = request.form['nome_cliente']
    cpf = request.form['cpf_cliente']
    telefone = request.form['telefone_cliente']
    email = request.form['email_cliente']
    cidade = request.form['cidade_cliente'].lower()

    if cidade == 'sousa':
        desconto = True
    else:
        desconto = False

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '@Refri198',
        database = 'bd_livraria',
    )

    cursor = conexao.cursor(prepared=True)
    sql = f'INSERT INTO cliente (nome, cpf, telefone, email, is_desconto) VALUES (%s, %s, %s, %s, %s)'
    valores = (name, cpf, telefone, email, desconto)
    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

    return login_screen()
#==============================================================================#

############################################################################################################
############################################## ROTAS DO ADMIN ##############################################
############################################################################################################

############################################################################################################
################################################# Clientes #################################################
############################################################################################################

#==============================================================================#
@app.route("/homepage_admin.html")
def home():
    return render_template("homepage_admin.html")
#==============================================================================#


#==============================================================================#
@app.route("/Cadastrar_cliente_admin.html") #CREATE
def pagina_cadastrarCliente_admin():
    return render_template("Pages_admin/Cadastrar_cliente_admin.html")

#envio feito pelo perfil do administrador
@app.route('/submit_admin', methods=['POST'])
def submit_admin():
    name = request.form['nome_cliente']
    cpf = request.form['cpf_cliente']
    telefone = request.form['telefone_cliente']
    email = request.form['email_cliente']
    cidade = request.form['cidade_cliente'].lower()

    if cidade == 'sousa':
        desconto = True
    else:
        desconto = False

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '@Refri198',
        database = 'bd_livraria',
    )
    
    cursor = conexao.cursor(prepared=True)
    sql = f'INSERT INTO cliente (nome, cpf, telefone, email, is_desconto) VALUES (%s, %s, %s, %s, %s)'
    valores = (name, cpf, telefone, email, desconto)
    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

    return render_template("Pages_admin/Cadastrar_cliente_admin.html")
#==============================================================================#

@app.route("/Alterar_cadastro_cliente_admin.html") #UPDATE
def pagina_alterar_cadastro_cliente():
    return render_template("Pages_admin/Alterar_cadastro_cliente_admin.html")

@app.route("/alterar_cliente", methods=['POST']) #UPDATE
def alterar_cadastro_cliente():
    id_usuario = request.form['id']
    nome_atlz = request.form['nome_atlzd']
    cpf_atlz = request.form['cpf_atlzd']
    email_atlz = request.form['email_atlzd']
    telefone_atlz = request.form['telefone_atlzd']
    cidade_atlz = request.form['cidade_atlz'].lower()

    if cidade_atlz == 'sousa':
        desconto_atlz = True
    else:
        desconto_atlz = False


    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '@Refri198',
        database = 'bd_livraria',
    )
    cursor = conexao.cursor(prepared=True)
    comando = f'UPDATE cliente SET nome = %s, cpf = %s, telefone = %s, email = %s, is_desconto = %s WHERE id = %s' #UPDATE
    valores = (nome_atlz, cpf_atlz, telefone_atlz, email_atlz, desconto_atlz, id_usuario)
    cursor.execute(comando, valores)
    conexao.commit() # Edita o banco de dados
    conexao.close()
    
    return pagina_alterar_cadastro_cliente()
#==============================================================================#

@app.route("/Pesquisar_cliente_admin.html")
def pagina_pesquisar_cliente():
    return render_template("Pages_admin/Pesquisar_cliente.html")

@app.route("/pesquisar_cliente", methods=['POST'])
def pesquisar_cliente():
    pesquisar_nome = request.form['nome_cliente']

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '@Refri198',
        database = 'bd_livraria',
    )
    cursor = conexao.cursor(prepared=True)
    comando = f'SELECT * FROM cliente WHERE nome LIKE %s' #READ
    valores = ('%' + pesquisar_nome + '%',)
    cursor.execute(comando, valores)
    resultado = cursor.fetchall() # Ler o banco de dados
    conexao.close()

    return render_template('Pages_admin/Pesquisar_cliente.html', cliente = resultado)
#==============================================================================#

@app.route("/Remover_cliente_admin.html")
def pagina_remover_cliente():
    return render_template("Pages_admin/Remover_cliente.html")

@app.route("/remover_cliente", methods=['POST'])
def remover_cliente():
    id = request.form['id']

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '@Refri198',
        database = 'bd_livraria',
    )
    cursor = conexao.cursor(prepared=True)
    comando = f'DELETE FROM cliente WHERE id = %s' # DELETE
    valores = (id,)
    cursor.execute(comando, valores)
    conexao.commit() # Edita o banco de dados
    conexao.close()
    
    return pagina_remover_cliente()

#==============================================================================#

@app.route("/listar_all_clientes_admin.html")
def pagina_listarAllClientes():
    return render_template("Pages_admin/listar_all_clientes.html")


@app.route("/exibir_clientes") #READ
def exibirClientes():
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '@Refri198',
        database = 'bd_livraria',
    )
    
    cursor = conexao.cursor()
    sql = f'SELECT * FROM cliente' #READ
    cursor.execute(sql)
    resultado = cursor.fetchall() # Ler o banco de dados
    conexao.close()
    
    return render_template('Pages_admin/listar_all_clientes.html', cliente = resultado)
#==============================================================================#

############################################################################################################
################################################## Livros ##################################################
############################################################################################################

#==============================================================================#

@app.route("/Cadastrar_livro_admin.html")
def cadastrar_livro():
    return render_template("Pages_admin/Cadastrar_livro.html")

@app.route('/submit_livro', methods=['POST'])
def submit_livro():
    nome = request.form['nome_livro']
    preco = request.form['preco_livro']
    local  = request.form['local_fabric']
    qtd_livro = request.form['quantidade_livro']
    categoria = request.form['categoria_livro']

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '@Refri198',
        database = 'bd_livraria',
    )
    
    cursor = conexao.cursor(prepared=True)
    sql = f'INSERT INTO livro (id_categoria, nome, preco, local_fabricacao, quantidade_estoq) VALUES (%s, %s, %s, %s, %s)'
    valores = (categoria, nome, preco, local, qtd_livro)
    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

    return cadastrar_livro()

#==============================================================================#

@app.route("/Alterar_cadastro_livro_admin.html") #UPDATE
def pagina_alterar_cadastro_livro():
    return render_template("Pages_admin/Alterar_cadastro_livro_admin.html")

@app.route("/alterar_livro", methods=['POST']) #UPDATE
def alterar_cadastro_livro():
    id_livro = request.form['id']
    nome_atlz = request.form['nome_atlzd']
    preco_atlz = request.form['preco_atlzd']
    local_atlz  = request.form['local_fabric_atlz']
    qtd_atlz = request.form['quantidade_atlzd']
    categoria_atlz = request.form['categoria_livro_atlz']


    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '@Refri198',
        database = 'bd_livraria',
    )
    cursor = conexao.cursor(prepared=True)
    comando = f'UPDATE livro SET id_categoria = %s, nome = %s, preco = %s, local_fabricacao = %s, quantidade_estoq = %s WHERE id = %s' #UPDATE
    valores = (categoria_atlz, nome_atlz, preco_atlz, local_atlz, qtd_atlz, id_livro)
    cursor.execute(comando, valores)
    conexao.commit() # Edita o banco de dados
    conexao.close()
    
    return pagina_alterar_cadastro_livro()

#==============================================================================#

@app.route("/Pesquisar_livro_admin.html")
def pagina_pesquisar_livros():
    return render_template("Pages_admin/Pesquisar_livro.html")

@app.route("/pesquisar_livro", methods=['POST'])
def pesquisar_livros():
    pesquisar_nome = request.form['nome_livro']

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '@Refri198',
        database = 'bd_livraria',
    )
    cursor = conexao.cursor(prepared=True)
    comando = f'SELECT * FROM livro WHERE nome LIKE %s' #READ
    valores = ('%' + pesquisar_nome + '%',)
    cursor.execute(comando, valores)
    resultado = cursor.fetchall() # Ler o banco de dados
    conexao.close()

    return render_template('Pages_admin/Pesquisar_livro.html', livro = resultado)

#==============================================================================#

@app.route("/Remover_livro_admin.html")
def pagina_remover_livro():
    return render_template("Pages_admin/Remover_livro.html")

@app.route("/remover_livro", methods=['POST'])
def remover_livro():
    id = request.form['id']

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '@Refri198',
        database = 'bd_livraria',
    )
    cursor = conexao.cursor(prepared=True)
    comando = f'DELETE FROM livro WHERE id = %s' # DELETE
    valores = (id,)
    cursor.execute(comando, valores)
    conexao.commit() # Edita o banco de dados
    conexao.close()
    
    return pagina_remover_livro()

#==============================================================================#

@app.route("/listar_all_livros_admin.html")
def pagina_listarAllLivros():
    return render_template("Pages_admin/listar_all_livros.html")


@app.route("/exibir_livros") #READ
def exibirLivros():
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '@Refri198',
        database = 'bd_livraria',
    )
    
    cursor = conexao.cursor()
    sql = f'SELECT * FROM livro' #READ
    cursor.execute(sql)
    resultado = cursor.fetchall() # Ler o banco de dados
    conexao.close()
    
    return render_template('Pages_admin/listar_all_livros.html', livro = resultado)
#==============================================================================#

@app.route("/Gerar_relatorio_admin.html")
def pagina_gerarRelatorio():
    return render_template("Pages_admin/Gerar_relatorio.html")


@app.route("/exibir_relatorio") #READ
def exibirRelatorio():
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '@Refri198',
        database = 'bd_livraria',
    )
    
    cursor = conexao.cursor()
    sql_1 = f'SELECT * FROM cliente'
    sql_2 = f'SELECT * FROM livro'
    cursor.execute(sql_1)
    clientes = cursor.fetchall() # Ler o banco de dados

    cursor.execute(sql_2)
    livros = cursor.fetchall()

    conexao.close()

    qtd_clientes = len(clientes) # pega a quantidade de elementos(as pessoas cadastradas) dentro da lista
    qtd_livros_diferente = len(livros)

    valor_total = sum(coluna[3] * coluna[5] for coluna in livros)# pega todos os valores das colunas 2(preço) e 3(quantidade), realiza a multiplicação (preço x quantidade), linha por linha,
                                                                 # e depois soma tudo para ter o valor total do estoque
    valor_total = round(valor_total, 2)

    total_livros = sum(coluna[5] for coluna in livros) # Soma todos os valores da coluna [3]
    


    return render_template('Pages_admin/Gerar_relatorio.html', cliente = clientes, total_clientes = qtd_clientes, livro = livros, total_livros_dif = qtd_livros_diferente, livros_total = total_livros, preco_total = valor_total)


#=======================================================================================================#
if __name__ == "__main__":
    app.run(debug=True)
#=======================================================================================================#