# Reference dataset of the industrial case

The given low-fidelity logs of the drawer-slide line, used in the paper as the reference ("REAL") case of the
industrial line (Suppl. S5), and the master log rebuilt from them.

- `lfm_logs/21_HFM_<k>_log.txt.gz`: the 323 given low-fidelity logs, gzip-compressed; `21_HFM_<k>` is the `name` of the
  configuration in `../lfm_catalog.csv` (`source = given`), whose `bits` give the sensed interfaces.
  Each log holds the first 1,000 items by arrival (340 component02, 308 component01, 352 drawerSlide).
- `master_log/21_HFM_log.txt.gz`: the master (high-fidelity) log, 32,440 events over 14,303.76 s, gzip-compressed. It is not part of the
  given dataset: it was **rebuilt** for this study as the union of the 35 low-fidelity logs that merge a single step
  (every interface is sensed in at least one of them), and it reproduces every given low-fidelity log by projection.

Format: as in `tools/FORMATS.md`, with one difference in the low-fidelity logs: the resources are those of the
low-fidelity model. Every resource or cluster of merged resources is named after its first resource with the suffix
`_1` (e.g. `B09_1` covers B09 and the resources merged with it when the following interfaces are not sensed).
