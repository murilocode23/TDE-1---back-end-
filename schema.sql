CREATE TABLE usuario (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    senha VARCHAR(255) NOT NULL
);

CREATE TABLE curso (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(400) NOT NULL,
    formato_aula VARCHAR(30) NOT NULL
);

CREATE TABLE disciplina (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    carga_horaria INTEGER NOT NULL,
    turno VARCHAR(50),
    curso_id INTEGER NOT NULL,
    FOREIGN KEY (curso_id) REFERENCES curso(id)
);

CREATE TABLE questao (
    id INTEGER PRIMARY KEY,
    descricao TEXT,
    tipo VARCHAR(100),
    nivel_dificuldade TEXT,
    disciplina_id INTEGER NOT NULL,
    FOREIGN KEY (disciplina_id) REFERENCES disciplina(id)
);

CREATE TABLE opcao_questao (
    id INTEGER PRIMARY KEY,
    descricao TEXT,
    correta BOOLEAN,
    questao_id INTEGER NOT NULL,
    FOREIGN KEY (questao_id) REFERENCES questao(id)
);

CREATE TABLE avaliacao (
    id INTEGER PRIMARY KEY,
    curso_id INTEGER NOT NULL,
    disciplina_id INTEGER NOT NULL,
    semestre TEXT,
    docente VARCHAR(100) NOT NULL,
    data_avaliacao DATE,
    data_elaboracao DATE,
    tipo TEXT,
    valor_avaliacao INTEGER NOT NULL,
    quantidade_questoes_multipla_escolha INTEGER NOT NULL,
    quantidade_questoes_abertas INTEGER NOT NULL,
    FOREIGN KEY (curso_id) REFERENCES curso(id),
    FOREIGN KEY (disciplina_id) REFERENCES disciplina(id)
);

CREATE TABLE avaliacao_questao (
    id INTEGER PRIMARY KEY,
    avaliacao_id INTEGER NOT NULL,
    questao_id INTEGER NOT NULL,
    valor_questao INTEGER NOT NULL,
    FOREIGN KEY (avaliacao_id) REFERENCES avaliacao(id),
    FOREIGN KEY (questao_id) REFERENCES questao(id)
);

CREATE TABLE template (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(100),
    nome_arquivo VARCHAR(255)
);

CREATE TABLE usuario_curso (
    usuario_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    PRIMARY KEY (usuario_id, curso_id),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (curso_id) REFERENCES curso(id)
);

CREATE TABLE usuario_disciplina (
    usuario_id INTEGER NOT NULL,
    disciplina_id INTEGER NOT NULL,
    PRIMARY KEY (usuario_id, disciplina_id),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (disciplina_id) REFERENCES disciplina(id)
);



-- OBS: as senhas abaixo estão com HASH bcrypt (não em texto puro), gerado a
-- partir das senhas originais: admin@exemplo.com=123456, autor1@exemplo.com=654321, autor2@exemplo.com=213246
INSERT INTO usuario (id, email, nome, tipo, senha) VALUES
(1, 'admin@exemplo.com', 'Administrador', 'admin', '$2b$12$EgQJ.rSQtJ5CSjiXo8ZIPOdxilIxuZgxic.OqEQRfpMabfZL03Cl2'),
(2, 'autor1@exemplo.com', 'Maria Silva', 'autor', '$2b$12$wvNG9r05sicvc4ZbrNPi.eBrbNyufMieRUo8/ryIIztXOGcQm7U9q'),
(3, 'autor2@exemplo.com', 'João Santos', 'autor', '$2b$12$oBCm7gs2fif3XVl0gbmM4uyea7AqYmi3QoZiyU25AISmpS.xskUvC');



INSERT INTO curso (id, nome, descricao, formato_aula) VALUES
(1, 'Análise e Desenvolvimento de Sistemas',
 'Curso voltado para desenvolvimento de sistemas e tecnologias da informação.',
 'presencial'),
(2, 'Engenharia de Software',
 'O curso é voltado para a criação, desenvolvimento, manutenção, teste e gestão de sistemas e aplicativos computacionais',
 'semi-presencial'),
 
(3,'Análise e Desenvolvimento de Sistemas',
 'É uma graduação tecnológica voltada para a criação, teste e manutenção de softwares e sistemas computacionais',
 'EAD');

INSERT INTO disciplina (id, nome, descricao, carga_horaria, turno, curso_id) VALUES
(1, 'Programação Backend',
 'Desenvolvimento de aplicações no lado do servidor.',
 80, 'Noturno', 1),

(2, 'Banco de Dados',
 'Conceitos de bancos de dados relacionais e SQL.',
 60, 'Noturno', 1),

(3, 'Engenharia de Software',
 'Estudo dos processos e técnicas de desenvolvimento de software.',
 60, 'Vespertino', 2);


INSERT INTO questao (id, descricao, tipo, nivel_dificuldade, disciplina_id) VALUES
(1, 'O que é uma chave primária em um banco de dados?',
 'aberta', 'fácil', 2),

(2, 'Qual comando SQL é utilizado para criar uma tabela?',
 'múltipla escolha', 'fácil', 2),

(3, 'Qual tecnologia pode ser utilizada para desenvolver uma API?',
 'múltipla escolha', 'média', 1);


INSERT INTO opcao_questao (id, descricao, correta, questao_id)
VALUES
(1, 'CREATE TABLE', TRUE, 2),
(2, 'DELETE TABLE', FALSE, 2),
(3, 'REMOVE TABLE', FALSE, 2),
(4, 'CREATE API', FALSE, 2),

(5, 'Flask', TRUE, 3),
(6, 'HTML', FALSE, 3),
(7, 'CSS', FALSE, 3),
(8, 'JPEG', FALSE, 3);



INSERT INTO avaliacao (id, curso_id, disciplina_id, semestre, docente, data_avaliacao, data_elaboracao, tipo,valor_avaliacao,
    quantidade_questoes_multipla_escolha, quantidade_questoes_abertas) VALUES
(1, 1, 2, '2026.2', 'Carlos Oliveira',
 '2026-10-15',
 '2026-09-20',
 'AV1',
 10,
 1,
 1),

(2, 1, 1, '2026.2', 'Ana Souza',
 '2026-10-20',
 '2026-09-22',
 'AV1',
 10,
 1,
 0);


INSERT INTO avaliacao_questao ( id, avaliacao_id, questao_id, valor_questao) VALUES
(1, 1, 1, 5),
(2, 1, 2, 5),
(3, 2, 3, 10);


INSERT INTO template (id, nome, nome_arquivo)
VALUES
(1, 'Modelo padrão de avaliação', 'modelo_avaliacao.docx'),
(2, 'Modelo de avaliação acadêmica', 'modelo_academico.docx');


INSERT INTO usuario_curso (usuario_id, curso_id)
VALUES
(2, 1),
(3, 1),
(3, 2);

INSERT INTO usuario_disciplina (usuario_id, disciplina_id)
VALUES
(2, 1),
(2, 2),
(3, 3);
