CREATE SCHEMA IF NOT EXISTS qualidade;

CREATE TABLE IF NOT EXISTS qualidade.metricas_qualidade (
    id BIGSERIAL PRIMARY KEY,
    regra VARCHAR(100) NOT NULL,
    dimensao VARCHAR(50) NOT NULL,
    tabela_avaliada VARCHAR(100) NOT NULL,
    linhas_avaliadas BIGINT NOT NULL,
    linhas_com_falha BIGINT NOT NULL,
    percentual_falhas NUMERIC(8,2) NOT NULL,
    data_execucao TIMESTAMPTZ DEFAULT NOW()
);