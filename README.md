# Data for "Physics-informed event-log reconstruction and parameter identification in partially observed production lines"

Data behind the figures and tables of the manuscript (M. Urgo, W. Terkaj, Q. Qi, A. Nassehi, submitted to CIRP Annals)
and of its Supplementary Material. The repository holds the generated event logs, the reconstructed logs of the decoders
for the configurations discussed in the paper, the per-run, per-configuration result tables and the summary tables.
The simulators, the training code and the trained networks are not part of this release.

Repository: https://github.com/murgo-polimi/MANUPINN-CIRP27-STCO

If you use these data, please cite the paper (see `CITATION.cff`). The reference datasets of the two lines (their
master logs and low-fidelity logs, `*/reference_2021/`) are those of Terkaj et al., CIRP Annals 70 (2021) 361-364; please
cite that paper as well when you use them.

## Layout

```
assembly_line/                 seven-machine assembly line (Section 4 of the paper; Suppl. S2)
  line.md                      machines, standard processing times, maximum buffer capacities, column layout of the logs
  configurations.csv           the 511 sensor configurations (LFMs): sensed interfaces, clusters, hidden events
  test_runs/run_XXX/           100 TEST runs: 07_HFM_log.txt.gz (complete event log, HFM format), params.json (effective
                               capacities, failure and arrival parameters, seed)
  val_runs/run_XXX/            the 50 VAL runs used to select the sensor configurations (Section 4.2): same files
  reconstructions/<method>/    reconstructed logs (HFM format) of the PI-FNO, hybrid, LP-max and LP-true decoders for
                               the configurations discussed in the paper, one file per run and configuration
  metrics/test_run_XXX.csv.gz  per-run, per-configuration, per-method metrics (log errors, KPI values and errors,
                               tolerance checks) on TEST; val_run_XXX.csv.gz the same on the VAL runs
  metrics_full/                the complete evaluation files behind metrics/ (every column of the evaluation, all
                               methods and ablations), test_run_XXX.csv.xz and val_run_XXX.csv.xz
  summary_tables/              the tables behind Table 1, Fig. 3a, Section 4.2 and Suppl. S2 (ablations, sensor spread,
                               VAL selection, run-to-run variability, error quantiles)
  reference_2021/              reference dataset of Terkaj et al. (2021): master_log/07_HFM_log.txt.gz and the 511
                               low-fidelity logs lfm_logs/07_HFM_<id>_log.txt.gz (the REAL case, Suppl. S5)
industrial_case/               drawer-slide line with 26 machines and 21 buffers (Section 5; Suppl. S2-S6)
  line.md                      machines, standard processing times, maximum capacities, interfaces, column layout
  lfm_catalog.csv              the 1536 sensor configurations: 323 given, 1172 random, 41 of the greedy path
                               (bits = sensed interfaces in the order listed in line.md)
  test_runs/run_XXX/           100 TEST runs: 21_HFM_log.txt.gz (complete log, HFM format), truth.json (effective capacities,
                               items per type, seed)
  out_of_range_runs/run_XXX/   30 runs with capacities uniform over 1..c_max (Section 5.3; Suppl. Table S4)
  reconstructions/<method>/    reconstructed logs (HFM format) of the PI-FNO, hybrid, LP-max and LP-true decoders for the
                               three configurations discussed in the paper (G15, G17, G20) on the first 30 TEST runs, one
                               file per run and configuration
  metrics/test_run_XXX.csv.gz  per-run, per-configuration, per-method metrics on TEST; out_of_range_run_XXX.csv.gz the
                               same on the out-of-range runs
  metrics_full/                the complete evaluation files behind metrics/, noise_study/metrics/ and master_log/, in
                               the same sub-folders (metrics/, noise_study/metrics/sigma_<s>/, master_log/), *.csv.xz
  noise_study/                 timestamp-noise experiment (Section 5.5; Suppl. S4): metrics/sigma_<s>/test_run_XXX.csv.gz
                               per noise level, and noisy_logs/sigma_<s>/run_XXX_21_HFM_log.txt.gz (the noisy sensed logs)
  master_log/                  metrics of the methods on the reference master log (Suppl. S5): real.csv.gz
  summary_tables/              the tables behind Table 1, Figs. 3b and 4, Sections 5.3-5.5 and Suppl. S2-S5
  reference_2021/              reference dataset: the 323 given low-fidelity logs lfm_logs/21_HFM_<k>_log.txt.gz and the
                               master log master_log/21_HFM_log.txt.gz rebuilt from them (the REAL case, Suppl. S5)
tools/
  read_logs.py                 reader: HFM log -> table of event times; derive the low-fidelity log of a configuration
  FORMATS.md                   file formats and column definitions
```

## Formats in one paragraph

Event logs are gzip-compressed tab-separated text files (`*.txt.gz`; pandas reads them directly, or use `zcat`/`gunzip`) in the format of the reference dataset (`id  time  property  value1  value2`:
one line per entry or exit of an item into or from a resource). A low-fidelity log is the complete log restricted to the
sensed interfaces of a configuration; `tools/read_logs.py` derives it from the complete log and the configuration
(`configurations.csv` or `lfm_catalog.csv`), so the low-fidelity logs of the simulated runs are not stored one by one
(those of the reference datasets are, in `reference_2021/`, with the resource names of the low-fidelity models). Metrics files have one
row per (run, configuration, method) plus one `truth` row per run with the KPI values of the complete log; column
definitions are in `tools/FORMATS.md`. Summary tables are plain CSV with the same names as in the Supplementary Material
sources.

## Licence

Creative Commons Attribution 4.0 International (CC BY 4.0), see `LICENSE`.
