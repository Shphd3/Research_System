# Amendments

A1: Before any formal DEV/reference/CONF extraction, calibration hook comparison failed because native linear router receives flattened [B*S,1024], while norm2 outputs [B,S,1024]. Correct the audit reshape, retain original code/log/freeze in versions. Exact-equality gate unchanged; no model computation or statistical definition changed.

A2: After numerical completion, portable comparison binding now reads a byte-identical packaged snapshot of the original Qwen table instead of an absolute external path. Original statistical code and its pre-output freeze hash retained; no statistic, weight, threshold or result changed.
