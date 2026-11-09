-- PROJETO INTEGRADO - BANCO DE DADOS
-- Aluno: Thiago Rodrigues; Vinicius Pansonato; Guilherme Ronaldo | Turma: 2 TI B
-- Modelo fisico baseado nos modelos conceitual e logico do projeto.
-- Ambiente: phpMyAdmin / XAMPP;MySQL 8.0.16+.
-- Importar este arquivo uma unica vez em um banco novo.
-- O arquivo cria somente a estrutura, sem dados pessoais ou de exemplo.

SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS projeto_integrado
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE projeto_integrado;

-- 1. Contas individuais: CPF e e-mail sao unicos separadamente.
-- CPF: armazenar apenas os 11 digitos; telefone pode ser nao informado.
CREATE TABLE USUARIO (
    id_usuario INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome_completo VARCHAR(150) NOT NULL,
    cpf CHAR(11) NOT NULL,
    email VARCHAR(191) NOT NULL,
    telefone VARCHAR(20) NULL,
    senha_hash VARCHAR(255) NOT NULL,
    perfil VARCHAR(20) NOT NULL,
    CONSTRAINT pk_usuario PRIMARY KEY (id_usuario),
    CONSTRAINT uq_usuario_cpf UNIQUE (cpf),
    CONSTRAINT uq_usuario_email UNIQUE (email),
    CONSTRAINT ck_usuario_perfil CHECK (
        perfil IN ('CLIENTE', 'FUNCIONARIO', 'GERENTE')
    )
) ENGINE=InnoDB;

-- 2. Cada lista pertence a um usuario; cada usuario tem no maximo uma lista.
CREATE TABLE LISTA_DESEJOS (
    id_lista INT UNSIGNED NOT NULL AUTO_INCREMENT,
    id_usuario INT UNSIGNED NOT NULL,
    CONSTRAINT pk_lista_desejos PRIMARY KEY (id_lista),
    CONSTRAINT uq_lista_usuario UNIQUE (id_usuario),
    CONSTRAINT fk_lista_usuario FOREIGN KEY (id_usuario)
        REFERENCES USUARIO (id_usuario)
        ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB;

-- 3. Informacoes comuns aos produtos de um mesmo modelo.
CREATE TABLE MODELO (
    id_modelo INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    descricao TEXT NULL,
    CONSTRAINT pk_modelo PRIMARY KEY (id_modelo)
) ENGINE=InnoDB;

-- 4. Cor unica dentro do modelo; preco compartilhado por seus tamanhos.
CREATE TABLE COLORACAO (
    id_coloracao INT UNSIGNED NOT NULL AUTO_INCREMENT,
    id_modelo INT UNSIGNED NOT NULL,
    cor VARCHAR(50) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    CONSTRAINT pk_coloracao PRIMARY KEY (id_coloracao),
    CONSTRAINT uq_coloracao_modelo_cor UNIQUE (id_modelo, cor),
    CONSTRAINT ck_coloracao_preco CHECK (preco >= 0),
    CONSTRAINT fk_coloracao_modelo FOREIGN KEY (id_modelo)
        REFERENCES MODELO (id_modelo)
        ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB;

-- 5. Um registro para cada tamanho de cada coloracao.
-- Tamanho textual permite valores como P, M, G, 38 e 40.
-- Estoque zero e permitido: o produto esgotado permanece cadastrado.
CREATE TABLE VARIANTE (
    id_variante INT UNSIGNED NOT NULL AUTO_INCREMENT,
    id_coloracao INT UNSIGNED NOT NULL,
    tamanho VARCHAR(20) NOT NULL,
    quantidade_estoque INT NOT NULL DEFAULT 0,
    CONSTRAINT pk_variante PRIMARY KEY (id_variante),
    CONSTRAINT uq_variante_coloracao_tamanho UNIQUE (id_coloracao, tamanho),
    CONSTRAINT ck_variante_estoque CHECK (quantidade_estoque >= 0),
    CONSTRAINT fk_variante_coloracao FOREIGN KEY (id_coloracao)
        REFERENCES COLORACAO (id_coloracao)
        ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB;

-- 6. As fotos pertencem a coloracao, nao a um tamanho especifico.
CREATE TABLE FOTO (
    id_foto INT UNSIGNED NOT NULL AUTO_INCREMENT,
    id_coloracao INT UNSIGNED NOT NULL,
    url VARCHAR(2048) NOT NULL,
    CONSTRAINT pk_foto PRIMARY KEY (id_foto),
    CONSTRAINT fk_foto_coloracao FOREIGN KEY (id_coloracao)
        REFERENCES COLORACAO (id_coloracao)
        ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB;

-- 7. Resolucao do relacionamento N:N entre listas e variantes.
-- A PK composta impede repetir a mesma variante na mesma lista.
-- Incluir ou remover um item nao altera quantidade_estoque.
CREATE TABLE ITEM_LISTA_DESEJOS (
    id_lista INT UNSIGNED NOT NULL,
    id_variante INT UNSIGNED NOT NULL,
    CONSTRAINT pk_item_lista_desejos PRIMARY KEY (id_lista, id_variante),
    INDEX idx_item_variante (id_variante),
    CONSTRAINT fk_item_lista FOREIGN KEY (id_lista)
        REFERENCES LISTA_DESEJOS (id_lista)
        ON DELETE CASCADE ON UPDATE RESTRICT,
    CONSTRAINT fk_item_variante FOREIGN KEY (id_variante)
        REFERENCES VARIANTE (id_variante)
        ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB;

-- REGRAS QUE ENVOLVEM VARIAS TABELAS
-- FKs garantem que todo filho tenha um pai existente. Nao garantem que
-- todo pai tenha pelo menos um filho. As regras abaixo devem ser cumpridas
-- nas transacoes de cadastro/edicao do futuro backend:
-- a) Cadastrar um CLIENTE e sua LISTA_DESEJOS na mesma transacao; impedir
--    excluir ou transferir sua lista enquanto a conta continuar CLIENTE.
--    Ao mudar um perfil para CLIENTE, garantir que sua lista exista.
-- b) Cadastrar MODELO com pelo menos uma COLORACAO, e cada COLORACAO com
--    pelo menos uma VARIANTE e uma FOTO. Impedir remover o ultimo filho
--    obrigatorio de um pai que continue cadastrado.
-- c) Senhas devem ser convertidas em hash pelo backend, antes do INSERT.
-- d) Permissoes por perfil sao verificadas pelo backend: FUNCIONARIO
--    atualiza estoque/tamanhos; GERENTE tambem cadastra modelos e cores.
-- e) A lista e persistente e permite incluir/remover itens, sem reservas,
--    compras, pagamentos ou entregas. Estoque zero nao exclui a variante.
-- O arquivo nao cria triggers nem presume que CHECK possa consultar
-- outras tabelas. CHECK exige MySQL 8.0.16+.

-- Conferencia opcional depois da importacao:
-- SHOW TABLES;
-- SHOW CREATE TABLE ITEM_LISTA_DESEJOS;
-- SELECT VERSION();
