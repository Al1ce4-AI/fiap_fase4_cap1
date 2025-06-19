
CREATE TABLE "CULTURA" (
	id INTEGER NOT NULL, 
	nome VARCHAR(255) NOT NULL, 
	observacao TEXT(1000), 
	PRIMARY KEY (id), 
	UNIQUE (nome)
)

;


CREATE TABLE "NUTRIENTE" (
	id INTEGER NOT NULL, 
	nome VARCHAR(255) NOT NULL, 
	observacao TEXT(1000), 
	PRIMARY KEY (id), 
	UNIQUE (nome)
)

;


CREATE TABLE "PROPRIEDADE" (
	id INTEGER NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	cnpj VARCHAR(14), 
	cidade VARCHAR(255), 
	PRIMARY KEY (id), 
	UNIQUE (nome)
)

;


CREATE TABLE "TIPO_SENSOR" (
	id INTEGER NOT NULL, 
	nome VARCHAR(255) NOT NULL, 
	tipo VARCHAR(15) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (nome)
)

;


CREATE TABLE "UNIDADE" (
	id INTEGER NOT NULL, 
	nome VARCHAR(50) NOT NULL, 
	multiplicador FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (nome)
)

;


CREATE TABLE "CAMPO" (
	id INTEGER NOT NULL, 
	propriedade_id INTEGER NOT NULL, 
	identificador VARCHAR(100) NOT NULL, 
	area_ha FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(propriedade_id) REFERENCES "PROPRIEDADE" (id), 
	UNIQUE (identificador)
)

;


CREATE TABLE "PLANTIO" (
	id INTEGER NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	campo_id INTEGER NOT NULL, 
	tipo_cultura INTEGER NOT NULL, 
	data_inicio DATETIME NOT NULL, 
	data_fim DATETIME, 
	observacao TEXT(1000), 
	PRIMARY KEY (id), 
	FOREIGN KEY(campo_id) REFERENCES "CAMPO" (id), 
	FOREIGN KEY(tipo_cultura) REFERENCES "CULTURA" (id)
)

;


CREATE TABLE "APLICACAO_NUTRIENTE" (
	id INTEGER NOT NULL, 
	plantio_id INTEGER NOT NULL, 
	nutriente_id INTEGER NOT NULL, 
	unidade_id INTEGER NOT NULL, 
	data_aplicacao DATETIME NOT NULL, 
	quantidade FLOAT NOT NULL, 
	observacao TEXT(1000), 
	PRIMARY KEY (id), 
	FOREIGN KEY(plantio_id) REFERENCES "PLANTIO" (id), 
	FOREIGN KEY(nutriente_id) REFERENCES "NUTRIENTE" (id), 
	FOREIGN KEY(unidade_id) REFERENCES "UNIDADE" (id)
)

;


CREATE TABLE "SENSOR" (
	id INTEGER NOT NULL, 
	cod_serial VARCHAR(255), 
	tipo_sensor_id INTEGER NOT NULL, 
	plantio_id INTEGER, 
	nome VARCHAR(255) NOT NULL, 
	descricao VARCHAR(255), 
	data_instalacao DATETIME, 
	unidade_id INTEGER, 
	latitude FLOAT, 
	longitude FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(tipo_sensor_id) REFERENCES "TIPO_SENSOR" (id), 
	FOREIGN KEY(plantio_id) REFERENCES "PLANTIO" (id), 
	UNIQUE (nome), 
	FOREIGN KEY(unidade_id) REFERENCES "UNIDADE" (id)
)

;


CREATE TABLE "IRRIGACAO" (
	id INTEGER NOT NULL, 
	quantidade_total FLOAT NOT NULL, 
	data_hora DATETIME NOT NULL, 
	observacao TEXT(1000), 
	sensor_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(sensor_id) REFERENCES "SENSOR" (id)
)

;


CREATE TABLE "LEITURA_SENSOR" (
	id INTEGER NOT NULL, 
	sensor_id INTEGER NOT NULL, 
	data_leitura DATETIME NOT NULL, 
	valor FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(sensor_id) REFERENCES "SENSOR" (id)
)

;

