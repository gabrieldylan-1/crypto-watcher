CREATE OR REPLACE VIEW v_ohlc_15min AS
SELECT
  symbol,
  date_trunc('hour', bucket_ts) + floor(date_part('minute', bucket_ts)/15)*interval '15 min' as particao_tempo,
  count(*)                           as ticks,
  max(high)                          as high,
  min(low)                           as low,
  avg(close)                         as avg_price
FROM crypto.candles
WHERE bucket_ts >= now() - interval '7 days'
GROUP BY symbol, particao_tempo;
