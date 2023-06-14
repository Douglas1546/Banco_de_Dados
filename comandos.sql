CREATE TABLE cliente (
    id  INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(255) NOT NULL,
    telefone VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    is_desconto BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE pagamento (
    id  INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE vendedor (
    id  INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(255) NOT NULL,
    telefone VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE categoria (
    id  INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE livro (
    id  INT NOT NULL AUTO_INCREMENT,
    id_categoria INT NOT NULL,
    nome VARCHAR(255) NOT NULL,
    preco FLOAT NOT NULL,
    local_fabricacao VARCHAR(255) NOT NULL,
    quantidade_estoq INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_categoria) REFERENCES categoria(id)
);

CREATE TABLE compra (
    id  INT NOT NULL AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    id_vendedor INT NOT NULL,
    id_pagamento INT NOT NULL,
    data_compra DATE NOT NULL,
    status_compra BOOLEAN NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id),
    FOREIGN KEY (id_pagamento) REFERENCES pagamento(id),
    FOREIGN KEY (id_vendedor) REFERENCES vendedor(id)
);

CREATE TABLE item (
    id  INT NOT NULL AUTO_INCREMENT,
    id_compra INT NOT NULL,
    id_livro INT NOT NULL,
    quantidade INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_compra) REFERENCES compra(id),
    FOREIGN KEY (id_livro) REFERENCES livro(id)
);

INSERT INTO cliente ( nome, cpf, telefone, email, is_desconto) VALUES ("Yasmin", "12855502736", "84999649841", "yasmin.medeirosapp@gmail.com",FALSE);
INSERT INTO cliente ( nome, cpf, telefone, email, is_desconto) VALUES ("Ingrid", "12855695736", "84995699841", "ingrid@gmail.com", FALSE);
INSERT INTO cliente ( nome, cpf, telefone, email, is_desconto) VALUES ("Douglas", "12855695846", "84995699556", "douglas@gmail.com", TRUE);
INSERT INTO vendedor ( nome, cpf, telefone, email) VALUES ("Yasmin", "12855502736", "84999649841", "yasmin.medeirosapp@gmail.com");
INSERT INTO vendedor ( nome, cpf, telefone, email) VALUES ("Ingrid", "12855695736", "84995699841", "ingrid@gmail.com");
INSERT INTO vendedor ( nome, cpf, telefone, email) VALUES ("Douglas", "12855695846", "84995699556", "douglas@gmail.com");
INSERT INTO pagamento (nome) VALUES ("Pix");
INSERT INTO pagamento (nome) VALUES ("Berries");
INSERT INTO pagamento (nome) VALUES ("Cartão");
INSERT INTO pagamento (nome) VALUES ("Boletos");
INSERT INTO categoria (nome) VALUES ("Fantasia");
INSERT INTO categoria (nome) VALUES ("Ficção Científica");
INSERT INTO categoria (nome) VALUES ("Educação");
INSERT INTO livro (nome, preco, local_fabricacao, id_categoria, quantidade_estoq) VALUES ("A escola do bem e do mal", 35.5, "Mari", 1 ,10);
INSERT INTO livro (nome, preco, local_fabricacao, id_categoria, quantidade_estoq) VALUES ("Harry Potter", 35.5, "João Pessoa", 1, 4);
INSERT INTO livro (nome, preco, local_fabricacao, id_categoria, quantidade_estoq) VALUES ("Paulo Freire", 35.5, "Caicó", 3, 9);
INSERT INTO livro (nome, preco, local_fabricacao, id_categoria, quantidade_estoq) VALUES ("Planeta dos Macacos", 35.5, "Sousa", 2, 20);

CREATE PROCEDURE realizar_compra (IN cliente_in INT, IN pagamento_in INT, IN vendedor_in INT, IN livro_in INT, IN qtd_in INT, IN dt_compra_in DATE)
BEGIN
	DECLARE capacidade INT DEFAULT 0;
	SELECT quantidade_estoq INTO capacidade FROM livro WHERE livro.id=livro_in;
	IF capacidade<qtd_in THEN
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Tem menos livros no estoque que o requisitado';
	ELSE
	    INSERT INTO compra (id_cliente,id_vendedor, id_pagamento, status_compra, data_compra) VALUES (cliente_in, vendedor_in, pagamento_in, TRUE, dt_compra_in);
	    INSERT INTO item (id_compra, id_livro, quantidade) VALUES ((SELECT MAX(id) FROM compra), livro_in, qtd_in);
	    UPDATE livro SET quantidade_estoq = (quantidade_estoq - qtd_in) WHERE id = livro_in;
	 END IF;
END;
CALL realizar_compra (2,1,2,3,2,DATE("2023-06-10"));

CREATE PROCEDURE relatorio_de_vendas_mensal (IN vendedor_in INT, IN data_inicio_in DATE, IN data_final_in DATE)
BEGIN
    SELECT vendedor.id, vendedor.nome, COUNT(compra.id) as quantidade_de_vendas, SUM(item.quantidade) as quantidade_de_livros_vendidos,  
    SUM(item.quantidade*livro.preco*IF(cliente.is_desconto is true, 0.8, 1)) as valor_das_vendas FROM 
    vendedor JOIN compra ON vendedor.id = compra.id_vendedor 
    JOIN item ON compra.id = item.id_compra JOIN livro ON item.id_livro = livro.id JOIN cliente ON cliente.id = compra.id_cliente WHERE 
    compra.data_compra BETWEEN data_inicio_in AND data_final_in AND vendedor.id = vendedor_in   GROUP BY vendedor.id, vendedor.nome ; 
END ;

CALL relatorio_de_vendas_mensal(2, DATE("2023-06-5"), DATE("2023-06-15")); 

CREATE VIEW view_livro_menos_5 AS SELECT Livro.id as id_livro, Livro.nome as nome_livro, Categoria.id as id_categoria, Categoria.nome as nome_categoria, 
    Livro.quantidade_estoq, Livro.local_fabricacao
    FROM Livro JOIN Categoria ON Livro.id_categoria = Categoria.id WHERE Livro.quantidade_estoq < 5;


CREATE PROCEDURE historico_de_compras (IN cliente_in INT)
BEGIN
    SELECT cliente.id, compra.data_compra, livro.nome, item.quantidade, ROUND(SUM(item.quantidade*livro.preco*IF(cliente.is_desconto, 0.8, 1)),2) 
	FROM cliente JOIN compra ON compra.id_cliente = cliente.id  
	JOIN item ON item.id_compra = compra.id 
	JOIN livro ON item.id_livro = livro.id 
	JOIN categoria  ON categoria.id = livro.id_categoria
	WHERE cliente.id= cliente_in
	GROUP BY cliente.id, compra.data_compra, livro.nome,item.quantidade  ORDER BY cliente.id, compra.data_compra, livro.nome, item.quantidade ;  
END ;


