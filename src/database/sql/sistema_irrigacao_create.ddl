-- Gerado por Oracle SQL Developer Data Modeler 24.3.1.351.0831
--   em:        2025-05-15 03:19:19 BRT
--   site:      Oracle Database 11g
--   tipo:      Oracle Database 11g



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE CULTURA 
    ( 
     ID_CULTURA         INTEGER  NOT NULL , 
     NOME_CULTURA       VARCHAR2 (255)  NOT NULL , 
     OBSERVACAO_CULTURA VARCHAR2 (255) 
    ) 
;

ALTER TABLE CULTURA 
    ADD CONSTRAINT CULTURA_PK PRIMARY KEY ( ID_CULTURA ) ;

CREATE TABLE IRRIGACAO 
    ( 
     ID_IRRIGACAO       INTEGER  NOT NULL , 
     QUANTIDADE_TOTAL   FLOAT  NOT NULL , 
     DATA_HORA          DATE  NOT NULL , 
     OBSERVACAO         VARCHAR2 (255) , 
     SENSOR_ID_SENSOR   INTEGER  NOT NULL , 
     CULTURA_ID_CULTURA INTEGER  NOT NULL 
    ) 
;

COMMENT ON COLUMN IRRIGACAO.QUANTIDADE_TOTAL IS 'Quantidade de irrigação aplicada' 
;

COMMENT ON COLUMN IRRIGACAO.DATA_HORA IS 'Data e hora do inicio da irrigação' 
;

COMMENT ON COLUMN IRRIGACAO.OBSERVACAO IS 'Observações sobre a irrigação' 
;

ALTER TABLE IRRIGACAO 
    ADD CONSTRAINT IRRIGACAO_PK PRIMARY KEY ( ID_IRRIGACAO, CULTURA_ID_CULTURA ) ;

CREATE TABLE SENSOR 
    ( 
     ID_SENSOR                  INTEGER  NOT NULL , 
     NOME_SENSOR                VARCHAR2 (255)  NOT NULL , 
     DESCRICAO                  VARCHAR2 (255) , 
     DATA_INSTALACAO            DATE , 
     LATITUDE                   FLOAT , 
     LONGITUDE                  FLOAT , 
     TIPO_SENSOR_ID_TIPO_SENSOR INTEGER  NOT NULL 
    ) 
;

ALTER TABLE SENSOR 
    ADD CONSTRAINT SENSOR_PK PRIMARY KEY ( ID_SENSOR ) ;

CREATE TABLE TIPO_SENSOR 
    ( 
     ID_TIPO_SENSOR INTEGER  NOT NULL , 
     NOME_SENSOR    VARCHAR2 (255)  NOT NULL 
    ) 
;

ALTER TABLE TIPO_SENSOR 
    ADD CONSTRAINT TIPO_SENSOR_PK PRIMARY KEY ( ID_TIPO_SENSOR ) ;

ALTER TABLE IRRIGACAO 
    ADD CONSTRAINT IRRIGACAO_CULTURA_FK FOREIGN KEY 
    ( 
     CULTURA_ID_CULTURA
    ) 
    REFERENCES CULTURA 
    ( 
     ID_CULTURA
    ) 
;

ALTER TABLE IRRIGACAO 
    ADD CONSTRAINT IRRIGACAO_SENSOR_FK FOREIGN KEY 
    ( 
     SENSOR_ID_SENSOR
    ) 
    REFERENCES SENSOR 
    ( 
     ID_SENSOR
    ) 
;

ALTER TABLE SENSOR 
    ADD CONSTRAINT SENSOR_TIPO_SENSOR_FK FOREIGN KEY 
    ( 
     TIPO_SENSOR_ID_TIPO_SENSOR
    ) 
    REFERENCES TIPO_SENSOR 
    ( 
     ID_TIPO_SENSOR
    ) 
;



-- Relatório do Resumo do Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                             4
-- CREATE INDEX                             0
-- ALTER TABLE                              7
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
