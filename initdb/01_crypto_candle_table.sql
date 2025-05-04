CREATE SCHEMA IF NOT EXISTS crypto;

CREATE TABLE crypto.candles (
  id           bigserial primary key,
  symbol       text not null,
  bucket_ts    timestamptz not null,
  open         numeric,
  high         numeric,
  low          numeric,
  close        numeric
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_candles_symbol_bucket
  ON crypto.candles(symbol, bucket_ts);
