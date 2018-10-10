CREATE TABLE cliente (
	nome varchar(255) NOT NULL,
	senha varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	cpf integer NOT NULL,
	PRIMARY KEY (cpf)
);

CREATE TABLE Mensagem (
	remetente varchar(255) NOT NULL,
	destinatario varchar(255) NOT NULL,
	mensagem text NOT NULL
);





