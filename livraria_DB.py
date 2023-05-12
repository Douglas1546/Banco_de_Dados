import mysql.connector
import os

conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '@Refri198',
    database = 'bd_livraria',
)

cursor = conexao.cursor(prepared=True)

#=======================================================================================================#
class CRUD_cliente():
    def __init__(self, nome, cpf, email, telefone):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone

    def cadastrarCliente(): #CREATE
        os.system('cls')
        cliente = CRUD_cliente(input("Digite o nome do cliente: "), input("Digite o CPF do cliente: "), input("Digite o email do cliente: "), input("Digite o telefone do cliente: "))
        print("Cliente [",cliente.nome,"], CPF [", cliente.cpf, "], Email [",cliente.email,"], Telefone [", cliente.telefone, "] Cadastrado")

        sql = f'INSERT INTO clientes (nome_cliente, cpf, email, telefone) VALUES (%s, %s, %s, %s)' # CREATE - Insere elementos na tabela
        valores = (cliente.nome, cliente.cpf, cliente.email, cliente.telefone)
        cursor.execute(sql, valores) # executa o comando sql
        conexao.commit() 

    def exibirClientes():
        os.system('cls')
        sql = f'SELECT * FROM clientes' #READ
        cursor.execute(sql)
        resultado = cursor.fetchall() 
        print("\n================Clientes Registrados================\n")
        for list in resultado:
            print(list)
        print("\n==================================================\n")

    def alterarCadastroCliente():
        print("\n================Alterar cadastro do cliente================\n")
        id = input("Digite o [ID] do cliente que voce deseja alterar:")
        print("\n 1 - Alterar nome do cliente \n 2 - Alterar cpf do cliente \n 3 - Alterar email do cliente \n 4 - Alterar telefone do cliente")
        op = input("\nDigite o numero referente ao que voce deseja alterar no cadastro do cliente: ")
        while True:
            if op == "1":
                atlz_nome = input("Digite o nome atualizado: ")
                sql = f'UPDATE clientes SET nome_cliente = %s WHERE idClientes = %s' #UPDATE
                valores = (atlz_nome, id)
                cursor.execute(sql, valores)
                conexao.commit()
                break
            elif op == "2":
                atlz_cpf = input("Digite o cpf atualizado: ")
                sql = f'UPDATE clientes SET cpf = %s WHERE idClientes = %s' # UPDATE
                valores = (atlz_cpf, id)
                cursor.execute(sql, valores)
                conexao.commit() 
                break
            elif op == "3":
                atlz_email = input("Digite email atualizado: ")
                sql = f'UPDATE clientes SET email = %s WHERE idClientes = %s' # UPDATE
                valores = (atlz_email, id)
                cursor.execute(sql, valores)
                conexao.commit() 
                break
            elif op == "4":
                atlz_tel = input("Digite o telefone atualizado: ")
                sql = f'UPDATE clientes SET telefone = %s WHERE idClientes = %s' # UPDATE
                valores = (atlz_tel, id)
                cursor.execute(sql, valores)
                conexao.commit() 
                break
            
    def deleteCliente():
        print("\n================Remover cadastro do cliente================\n")
        id = input("Digite o [ID] do cliente que voce deseja remover:")
        sql = f'DELETE FROM clientes WHERE idClientes = %s ' # DELETE
        valores = (id,)
        cursor.execute(sql, valores)
        conexao.commit() 
        print(f"\nCliente com ID [{id}] removido com sucesso!")

    def pesquisarCliente():
        print("\n================Pesquisar Cliente================\n")
        op = input("\n 1 - Pesquisar por ID \n 2 - Pesquisar por nome \n\n Digite a opção desejada: ")
        while True:
            if op == '1':
                pesquisar = input("Digite o ID que você deseja pesquisar: ")
                sql = f'SELECT * FROM clientes WHERE idClientes LIKE %s' #READ
                valores = (pesquisar,)
                cursor.execute(sql, valores)
                resultado = cursor.fetchall()
                print("\n================ Cliente encontrado ================\n")
                print("\nID: ",resultado[0][0])
                print("\nNome do cliente: ",resultado[0][1])
                print("\nCPF do cliente: ",resultado[0][2])
                print("\nEmail do cliente: ",resultado[0][3])
                print("\nTelefone do cliente: ",resultado[0][4])
                print("\n==================================================\n")
                break
            elif op == '2':
                pesquisar = input("Digite o nome do cliente que deseja pesquisar: ")
                sql = f'SELECT * FROM clientes WHERE nome_cliente LIKE %s' #READ
                valores = ('%' + pesquisar + '%',) # É necessário adicionar o caractere '%' antes e depois do valor da variável, indicando que podem haver quaisquer caracteres antes e depois da sequência de caracteres buscada.
                cursor.execute(sql, valores)
                resultado = cursor.fetchall() # o cursor.fetchall ja retorna uma lista para a variavel resultado, então não preciso jogar a variavel resultado dentro de uma lista
                for result in resultado:
                    print("\n================ Cliente encontrado ================\n")
                    print("\nID: ",result[0])
                    print("\nNome do cliente: ",result[1])
                    print("\nCPF do cliente: ",result[2])
                    print("\nEmail do cliente: ",result[3])
                    print("\nTelefone do cliente: ",result[4])
                    print("\n==================================================\n")
                break

    def gerarRelatorioClientes():
        os.system('cls')
        print("\n================ Relatório dos clientes ================\n")
        sql = f'SELECT * FROM clientes' #READ
        cursor.execute(sql)
        resultado = cursor.fetchall()

        print("\n-Clientes cadastrados no sistema-\n")
        nome = [coluna[1] for coluna in resultado]
        cpf = [coluna[2] for coluna in resultado] 
        email = [coluna[3] for coluna in resultado] 
        telefone = [coluna[4] for coluna in resultado] 


        dados = list(zip(nome, cpf, email, telefone)) # combina as quatro listas acima em uma lista de tuplas
        for nomes, cpfs, emails, telefones in dados:
            print("Nome:", nomes,"| CPF:", cpfs,"| Email:", emails,"| Telefone:", telefones)
        ##################################################################################################
        qtd_cadastrado = len(resultado)
        print("\nQuantidade de usuarios cadastrados no sistema: ", qtd_cadastrado)
        print("\n==================================================\n")
#====================================================================================================================#
class CRUD_livros():
    def __init__(self, nome_livro, preco, qtd):
        self.nome_livro = nome_livro
        self.preco = preco
        self.qtd = qtd

    def cadastrarLivro(): #CREATE
        os.system('cls')
        livro = CRUD_livros(input("Digite o nome do livro: "), input("Digite o preço: "), input("Digite a quantidade: "))
        print("Livro de nome [",livro.nome_livro,"], preco [", livro.preco, "] e quantidade [",livro.qtd,"] Cadastrado")

        sql = f'INSERT INTO livros (nome_livro, preço, quantidade) VALUES (%s, %s, %s)' # CREATE
        valores = (livro.nome_livro, livro.preco, livro.qtd)
        cursor.execute(sql, valores)
        conexao.commit() 

    def exibirLivros():
        os.system('cls')
        sql = f'SELECT * FROM livros' #READ
        cursor.execute(sql)
        resultado = cursor.fetchall()
        print("\n================ Livros Registrados ================\n")
        for list in resultado:
            print(list)
        print("\n==================================================\n")

    def alterarCadastroLivro():
        print("\n================ Alterar cadastro do Livro ================\n")
        id = input("Digite o [ID] do livro que voce deseja alterar:")
        print("\n 1 - Alterar nome do livro \n 2 - Alterar o valor do livro \n 3 - Alterar a quantidade disponível")
        op = input("\nDigite o numero referente ao que voce deseja alterar no cadastro do livro: ")
        while True:
            if op == "1":
                atlz_nome_livro = input("Digite o nome do livro atualizado: ")
                sql = f'UPDATE livros SET nome_livro = %s WHERE id_livro = %s' #UPDATE
                valores = (atlz_nome_livro, id)
                cursor.execute(sql, valores)
                conexao.commit() 
                break
            elif op == "2":
                atlz_preco = input("Digite o preço atualizado: ")
                sql = f'UPDATE livros SET preço = %s WHERE id_livro = %s'
                valores = (atlz_preco, id)
                cursor.execute(sql, valores)
                conexao.commit() 
                break
            elif op == "3":
                atlz_qtd = input("Digite a quantidade atualizada disponível: ")
                sql = f'UPDATE livros SET quantidade = %s WHERE id_livro = %s' 
                valores = (atlz_qtd, id)
                cursor.execute(sql, valores)
                conexao.commit() 
                break

    def deleteLivro():
        print("\n================ Remover cadastro do cliente ================\n")
        id = input("Digite o [ID] do livro que voce deseja remover:")
        sql = f'DELETE FROM livros WHERE id_livro = %s' # DELETE
        valores = (id,)
        cursor.execute(sql, valores)
        conexao.commit() 
        print(f"\nLivro com ID [{id}] removido com sucesso!")

    def pesquisarLivro():
        print("\n================Pesquisar Livro================\n")
        op = input("\n 1 - Pesquisar por ID \n 2 - Pesquisar por nome \n\n Digite a opção desejada: ")
        while True:
            if op == '1':
                pesquisar = input("Digite o ID do livro que deseja pesquisar: ")
                sql = f'SELECT * FROM livros WHERE id_livro LIKE %s ' #READ
                valores = (pesquisar,) 
                cursor.execute(sql, valores)
                resultado = cursor.fetchall()
                print("\n================ Livro encontrado ================\n")
                print("\nID: ",resultado[0][0])
                print("\nNome do livro: ",resultado[0][1])
                print("\nPreço R$: ",resultado[0][2])
                print("\nQuantidade disponível: ",resultado[0][3])
                print("\n==================================================\n")
                break
            elif op == '2':
                pesquisar = input("Digite o nome do livro que deseja pesquisar: ")
                sql = f'SELECT * FROM livros WHERE nome_livro LIKE %s ' #READ
                valores = ('%' + pesquisar + '%',) 
                cursor.execute(sql, valores)
                resultado = cursor.fetchall()
                for result in resultado:
                    print("\n================ Livro encontrado ================\n")
                    print("\nID: ",result[0])
                    print("\nNome do livro: ",result[1])
                    print(f"\nPreço R$: {round(result[2], 2)}")
                    print("\nQuantidade disponível: ",result[3])
                    print("\n==================================================\n")
                break

    def gerarRelatorioEstoque():
        os.system('cls')
        print("\n================ Relatório do estoque ================\n")
        sql = f'SELECT * FROM livros' #READ
        cursor.execute(sql)
        resultado = cursor.fetchall()

        print("\n-Nome e quantidade de cada livro armazenado no estoque-\n")
        nome = [coluna[1] for coluna in resultado] # pega somente os nomes da coluna 1 e armazena em nomes
        qtd_cada_livro = [coluna[3] for coluna in resultado] # pega os valores da coluna 3 e armazena em qtd_cada_livro
        
        dados = list(zip(nome, qtd_cada_livro)) # combina as duas listas acima em uma lista de tuplas
        for nomes, qtd in dados:
            print("Livro:", nomes,"| Quantidade em estoque:", qtd)
        ##################################################################################################
        print("\n------------------Resumo------------------\n")
        qtd_cadastrado = len(resultado) 
        valor_total = sum(coluna[2] * coluna[3] for coluna in resultado) # pega todos os valores das colunas 2(preço) e 3(quantidade), realiza a multiplicação (preço x quantidade)
                                                                         # e depois soma tudo para obter o valor total do estoque
        total_livros = sum(coluna[3] for coluna in resultado)
        print("Quantidade de livros diferentes cadastrados: ", qtd_cadastrado)
        print("Quantidade total de livros em estoque: ", total_livros)
        print(f'Valor total dos itens armazenados no estoque R$: {round(valor_total, 2)}')
        print("\n==================================================\n")
#====================================================================================================================#

while True:
    print("\n================ Livraria ================\n")
    print("1 -  Cadastrar cliente")
    print("2 -  Alterar cadastro do cliente")
    print("3 -  Pesquisar cliente")
    print("4 -  Remover Cliente")
    print("5 -  Listar todos os clientes cadastrados")

    print("6 -  Cadastrar Livro")
    print("7 -  Alterar cadastro do livro")
    print("8 -  Pesquisar Livro")
    print("9 -  Remover Livro")
    print("10 - Listar todos os Livros cadastrados")

    print("11 - Gerar relatório")

    print("\n0 -  Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        CRUD_cliente.cadastrarCliente() #CREATE
    elif opcao == "2":
        CRUD_cliente.alterarCadastroCliente() #UPDATE
    elif opcao == "3":
        CRUD_cliente.pesquisarCliente()
    elif opcao == "4":
        CRUD_cliente.deleteCliente() # DELETE
    elif opcao == "5":
        CRUD_cliente.exibirClientes() # READ
    elif opcao == "6":
        CRUD_livros.cadastrarLivro()
    elif opcao == "7":
        CRUD_livros.alterarCadastroLivro()
    elif opcao == "8":
        CRUD_livros.pesquisarLivro()
    elif opcao == "9":
        CRUD_livros.deleteLivro()
    elif opcao == "10":
        CRUD_livros.exibirLivros()
    elif opcao == '11':
        os.system('cls')
        while True:
            print("\n 1 - Gerar relatório do estoque \n 2 - Gerar relatório dos clientes")
            op = input("\nEscolha qual relatório você deseja gerar: ")
            if op == "1":
                CRUD_livros.gerarRelatorioEstoque()
                break
            elif op == "2":
                CRUD_cliente.gerarRelatorioClientes()
                break
    elif opcao == "0":
        print("Saindo...")
        break
    else:
        print("Opção inválida. Tente novamente.")

cursor.close()

conexao.close()