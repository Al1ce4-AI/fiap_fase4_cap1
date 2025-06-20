
CREATE TABLE "CULTURA" (
	id INTEGER NOT NULL, 
	nome VARCHAR2(255 CHAR) NOT NULL, 
	observacao CLOB, 
	PRIMARY KEY (id), 
	UNIQUE (nome)
)

;


CREATE TABLE "NUTRIENTE" (
	id INTEGER NOT NULL, 
	nome VARCHAR2(255 CHAR) NOT NULL, 
	observacao CLOB, 
	PRIMARY KEY (id), 
	UNIQUE (nome)
)

;


CREATE TABLE "PROPRIEDADE" (
	id INTEGER NOT NULL, 
	nome VARCHAR2(100 CHAR) NOT NULL, 
	cnpj VARCHAR2(14 CHAR), 
	cidade VARCHAR2(255 CHAR), 
	PRIMARY KEY (id), 
	UNIQUE (nome)
)

;


CREATE TABLE "TIPO_SENSOR" (
	id INTEGER NOT NULL, 
	nome VARCHAR2(255 CHAR) NOT NULL, 
	tipo VARCHAR(15 CHAR) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (nome)
)

;


CREATE TABLE "UNIDADE" (
	id INTEGER NOT NULL, 
	nome VARCHAR2(50 CHAR) NOT NULL, 
	multiplicador FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (nome)
)

;


CREATE TABLE "CAMPO" (
	id INTEGER NOT NULL, 
	propriedade_id INTEGER NOT NULL, 
	identificador VARCHAR2(100 CHAR) NOT NULL, 
	area_ha FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(propriedade_id) REFERENCES "PROPRIEDADE" (id), 
	UNIQUE (identificador)
)

;


CREATE TABLE "PLANTIO" (
	id INTEGER NOT NULL, 
	nome VARCHAR2(100 CHAR) NOT NULL, 
	campo_id INTEGER NOT NULL, 
	tipo_cultura INTEGER NOT NULL, 
	data_inicio DATE NOT NULL, 
	data_fim DATE, 
	observacao CLOB, 
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
	data_aplicacao DATE NOT NULL, 
	quantidade FLOAT NOT NULL, 
	observacao CLOB, 
	PRIMARY KEY (id), 
	FOREIGN KEY(plantio_id) REFERENCES "PLANTIO" (id), 
	FOREIGN KEY(nutriente_id) REFERENCES "NUTRIENTE" (id), 
	FOREIGN KEY(unidade_id) REFERENCES "UNIDADE" (id)
)

;


CREATE TABLE "SENSOR" (
	id INTEGER NOT NULL, 
	cod_serial VARCHAR2(255 CHAR), 
	tipo_sensor_id INTEGER NOT NULL, 
	plantio_id INTEGER, 
	nome VARCHAR2(255 CHAR) NOT NULL, 
	descricao VARCHAR2(255 CHAR), 
	data_instalacao DATE, 
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
	data_hora DATE NOT NULL, 
	observacao CLOB, 
	sensor_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(sensor_id) REFERENCES "SENSOR" (id)
)

;


CREATE TABLE "LEITURA_SENSOR" (
	id INTEGER NOT NULL, 
	sensor_id INTEGER NOT NULL, 
	data_leitura DATE NOT NULL, 
	valor FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(sensor_id) REFERENCES "SENSOR" (id)
)

;

