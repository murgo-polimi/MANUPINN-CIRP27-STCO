# Reference dataset of the assembly line (Terkaj et al., CIRP Annals 70, 2021)

The original data of the assembly line studied in W. Terkaj, Q. Qi, M. Urgo et al., "Multi-scale modelling of
manufacturing systems using ontologies and delta-lenses", CIRP Annals 70 (2021) 361-364. The paper evaluates the
methods on these logs as the reference ("REAL") case (Suppl. S5).

- `master_log/07_HFM_log.txt.gz`: the master (high-fidelity) log, 200 parts and 200 components, 5,200 events over about
  2,943 s; file as distributed with the reference dataset (UTF-8 with byte-order mark), gzip-compressed.
- `lfm_logs/07_HFM_<id>_log.txt.gz`: the 511 low-fidelity logs, one per sensor configuration, gzip-compressed;
  `<id>` is the configuration id of `../configurations.csv`. Each is the master log restricted to the sensed interfaces
  of the configuration (checked event by event: 0 mismatches).

Format: as in `tools/FORMATS.md`, with one difference in the low-fidelity logs: the resources are those of the
low-fidelity model. Every resource or cluster of merged resources is named after its first resource with the suffix
`_1` (e.g. `B6_1` = B6 and M7 when B6|M7 is not sensed); the composition of the clusters is the `clusters` column of
`../configurations.csv`.
