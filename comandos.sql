CREATE TABLE Cliente (
    id  INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(255) NOT NULL,
    telefone VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    is_desconto BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Pagamento (
    id  INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Vendedor (
    id  INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(255) NOT NULL,
    telefone VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Categoria (
    id  INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Livro (
    id  INT NOT NULL AUTO_INCREMENT,
    id_categoria INT NOT NULL,
    nome VARCHAR(255) NOT NULL,
    preco FLOAT NOT NULL,
    local_fabricacao VARCHAR(255) NOT NULL,
    quantidade_estoq INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id)
);

CREATE TABLE Compra (
    id  INT NOT NULL AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    id_vendedor INT NOT NULL,
    id_pagamento INT NOT NULL,
    data_compra DATE NOT NULL,
    status_compra BOOLEAN NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id),
    FOREIGN KEY (id_pagamento) REFERENCES Pagamento(id),
    FOREIGN KEY (id_vendedor) REFERENCES Vendedor(id)
);

CREATE TABLE Item (
    id  INT NOT NULL AUTO_INCREMENT,
    id_compra INT NOT NULL,
    id_livro INT NOT NULL,
    quantidade INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_compra) REFERENCES Compra(id),
    FOREIGN KEY (id_livro) REFERENCES Livro(id)
);

Criação de Elementos Básicos
INSERT INTO Cliente ( nome, cpf, telefone, email, is_desconto) VALUES ("Yasmin", "12855502736", "84999649841", "yasmin.medeirosapp@gmail.com",FALSE);
INSERT INTO Cliente ( nome, cpf, telefone, email, is_desconto) VALUES ("Ingrid", "12855695736", "84995699841", "ingrid@gmail.com", FALSE);
INSERT INTO Cliente ( nome, cpf, telefone, email, is_desconto) VALUES ("Douglas", "12855695846", "84995699556", "douglas@gmail.com", TRUE);
INSERT INTO Vendedor ( nome, cpf, telefone, email) VALUES ("Yasmin", "12855502736", "84999649841", "yasmin.medeirosapp@gmail.com");
INSERT INTO Vendedor ( nome, cpf, telefone, email) VALUES ("Ingrid", "12855695736", "84995699841", "ingrid@gmail.com");
INSERT INTO Vendedor ( nome, cpf, telefone, email) VALUES ("Douglas", "12855695846", "84995699556", "douglas@gmail.com");
INSERT INTO Pagamento (nome) VALUES ("Pix");
INSERT INTO Pagamento (nome) VALUES ("Berries");
INSERT INTO Pagamento (nome) VALUES ("Cartão");
INSERT INTO Pagamento (nome) VALUES ("Boletos");
INSERT INTO Categoria (nome) VALUES ("Fantasia");
INSERT INTO Categoria (nome) VALUES ("Ficção Científica");
INSERT INTO Categoria (nome) VALUES ("Educação");
INSERT INTO Livro (nome, preco, local_fabricacao, id_categoria, quantidade_estoq) VALUES ("A escola do bem e do mal", 35.5, "Mari", 1 ,10);
INSERT INTO Livro (nome, preco, local_fabricacao, id_categoria, quantidade_estoq) VALUES ("Harry Potter", 35.5, "João Pessoa", 1, 4);
INSERT INTO Livro (nome, preco, local_fabricacao, id_categoria, quantidade_estoq) VALUES ("Paulo Freire", 35.5, "Caicó", 3, 9);
INSERT INTO Livro (nome, preco, local_fabricacao, id_categoria, quantidade_estoq) VALUES ("Planeta dos Macacos", 35.5, "Sousa", 2, 20);
Criar constraints de Fk

View -> Produtos que possuem menos que 5 unidades disponíveis.

CREATE PROCEDURE realizar_compra (IN cliente INT, IN pagamento INT, IN vendedor INT, IN livro INT, IN qtd INT, IN dt_compra DATE)
BEGIN
	DECLARE capacidade INT DEFAULT 0;
	SELECT quantidade_estoq INTO capacidade FROM Livro WHERE Livro.id=livro;
	IF capacidade<qtd THEN
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Tem menos livros no estoque que o requisitado';
	ELSE
	    INSERT INTO Compra (id_cliente,id_vendedor, id_pagamento, status_compra, data_compra) VALUES (cliente, vendedor, pagamento, TRUE, dt_compra);
	    INSERT INTO Item (id_compra, id_livro, quantidade) VALUES ((SELECT MAX(id) FROM Compra), livro, qtd);
	    UPDATE Livro SET quantidade_estoq = (quantidade_estoq - qtd) WHERE id = livro;
	 END IF;
END;
CALL realizar_compra (2,1,2,3,2,DATE("2023-06-10"));

CREATE PROCEDURE relatorio_de_vendas_mensal (IN vendedor INT, IN data_inicio DATE, IN data_final DATE)
BEGIN
    SELECT Vendedor.id, Vendedor.nome, COUNT(Compra.id) as quantidade_de_vendas, SUM(Item.quantidade) as quantidade_de_livros_vendidos,  
    SUM(Item.quantidade*Livro.preco) as valor_das_vendas FROM 
    Vendedor JOIN Compra ON Vendedor.id = Compra.id_vendedor 
    JOIN Item ON Compra.id = Item.id_compra JOIN Livro ON Item.id_livro = Livro.id WHERE 
    Compra.data_compra BETWEEN data_inicio AND data_final AND Vendedor.id = vendedor GROUP BY Vendedor.id, Vendedor.nome ; 
END ;

CALL relatorio_de_vendas_mensal(2, DATE("2023-06-5"), DATE("2023-06-15")); 

CREATE VIEW view_livro_menos_5 AS SELECT Livro.id as id_livro, Livro.nome as nome_livro, Categoria.id as id_categoria, Categoria.nome as nome_categoria, 
    Livro.quantidade_estoq, Livro.local_fabricacao
    FROM Livro JOIN Categoria ON Livro.id_categoria = Categoria.id WHERE Livro.quantidade_estoq < 5;





