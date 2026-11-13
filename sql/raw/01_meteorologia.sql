
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.meteorologia_horaria (
    id_meteorologia BIGSERIAL PRIMARY KEY,
    cod_usina VARCHAR(20) NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    temperatura_2m NUMERIC(10, 2),
    precipitacao NUMERIC(10, 2),
    velocidade_vento_10m NUMERIC(10, 2),
    radiacao_solar NUMERIC(12, 2),
    latitude NUMERIC(10, 6),
    longitude NUMERIC(10, 6),
    fonte VARCHAR(100) NOT NULL DEFAULT 'Open-Meteo',
    data_extracao TIMESTAMPTZ NOT NULL,
    CONSTRAINT uq_meteorologia_usina_hora
        UNIQUE (cod_usina, data_hora)
);

CREATE INDEX IF NOT EXISTS idx_meteorologia_data
ON raw.meteorologia_horaria (data_hora);

CREATE INDEX IF NOT EXISTS idx_meteorologia_usina
ON raw.meteorologia_horaria (cod_usina);
