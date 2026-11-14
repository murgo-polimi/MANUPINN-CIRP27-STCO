# File formats

## Event logs (`*_HFM_log.txt`)

Tab-separated text, header `id	time	property	value1	value2`, one line per event:

| column | content |
|---|---|
| id | item: `Part.<k>` / `Component.<k>` (assembly line); `component02.<g>`, `component01.<g>`, `drawerSlide.<g>` (industrial case; `<g>` is the global item id by arrival, as in the reference dataset) |
| time | event time [s] from the start of the run, four decimals |
| property | always `place` |
| value1 | `enter` or `exit` |
| value2 | resource (machine `M*` or buffer `B*`) |

A complete (high-fidelity) log has every entry and exit of every item. A low-fidelity log of a sensor configuration
keeps only the events at sensed interfaces: an interface `A|B` is the exit from `A`, which coincides with the entry into
`B`. `tools/read_logs.py` reads a log into a table (items × resources, entry and exit times) and derives the
low-fidelity log of a configuration. Reconstructed logs have the same format and contain every event: the events at
sensed interfaces equal the observed ones, the others are the decoder's estimates.

### Assembly line (`assembly_line/`)

Part route M1 → B1 → B2 → M4 → B4 → M5 → B5 → M6 → B6 → M7; component route M2 → M3 → B3 → M4 (assembly at M4).
Standard processing times [s]: M1 5, M2 3, M3 3, M4 10, M5 11, M6 12, M7 13. Maximum buffer capacities: B1 5, B2 4,
B3 10, B4 7, B5 6, B6 7. Runs of 200 parts and 200 components. The nine optional interfaces are B6|M7, M6|B6, B5|M6,
M5|B5, B4|M5, M3|B3, M2|M3, B1|B2, M1|B1; the three interfaces around M4 (B2|M4, B3|M4, M4|B4) are always sensed.
`configurations.csv` lists the 511 configurations: `id` (the LFM id used in the paper), `mask` (bit mask), `n_sensors`
(including the three always sensed), the clusters of the configuration, the numbers of partially observed and hidden
events, the `sensed_<interface>` flags and the baseline (LP-max) statistics of the earlier study.

`params.json` of a run gives the effective capacities (`K_B1` … `K_B6`), the failure and disturbance parameters, the
arrival parameters and the seed; `val_runs/` holds the first 50 runs of the validation set in the same form.

### Industrial case (`industrial_case/`)

Three item types with their routes (component02, component01, drawerSlide; assembly of component02 at M21 and of
component01 at M23) over 26 machines and 21 buffers, 46 interfaces; the six interfaces around the assembly machines
(B11|M23, B15|M21, B17|M21, B19|M23, M21|B18, M23|B20) are always sensed and the other 40 are optional. Standard
processing times [s]: M03, M09, M11, M18, M19 5.14; M01, M02, M05-M08, M12, M13, M16, M21-M24 10.28; M10, M14, M17, M20,
M25, M26 15.42; M04, M15 20.56. Maximum capacities: B00, B03, B12 20; B15 40; B11, B14, B17, B22 3; the others 2.
Runs of 400 items per type, of which the first 1000 items by arrival form the log (as in the master log).
`lfm_catalog.csv`: `name` (G00-G40 for the greedy path, `21_HFM_<k>` for the 323 given configurations, `R<k>` for
the random ones), `source`, `bits` (46 characters, one per interface in the order of `line.md`), `n_sensors`,
`n_optional`, and the LP-max log error of the earlier study where available.

`truth.json` of a run gives the effective capacities (`K_<buffer>`), the number of items of each type and the seed.

## Metrics files (`metrics/*.csv.gz`, `noise_study/metrics/*/*.csv.gz`, `master_log/real.csv.gz`)

One row per (run, configuration, method), plus one row per run with `method = truth` holding the KPI values of the
complete log (`k_*` columns). Methods: `op` (PI-FNO log read with the identified capacities; `op_K` in the assembly-line
files), `hyb` (hybrid: identified capacities → LP), `lp_max` (LP with maximum capacities), `lp_true` (LP with the true
capacities), and the ablations `op_Klog` (capacities from the reconstructed log only) and, in the assembly-line files,
`op` with capacities at the maximum. In the noise files `hyb_tol`, `occ_tol_lp` and `op_tol` are the variants with the
noise-tolerant saturation rule (Section 3.2) and `sigma` the noise level. Main columns:

| column | content |
|---|---|
| `absD_tot` | occupancy-based log error of Terkaj et al. (2021), summed over resources |
| `time_MAE`, `time_maxabs` | timestamp error over all events [s] |
| `hidden_within_1.0s`, `hidden_MAE` | share of hidden events within ±1 s and their mean absolute error [s] |
| `k_<machine>_util`, `_extra_share`, `_blocked_share`, `_idle_share` | machine KPIs of the reconstructed log |
| `k_<buffer>_mean_occ`, `_full_share`, `_capacity` | buffer KPIs and the capacity used to read them |
| `k_WIP_<portion>`, `k_time_<portion>_mean` | WIP and mean residence time of the line portions |
| `cap_feasible_<buffer>`, `cap_tie_<buffer>`, `cap_saturated_<buffer>` | diagnostics of the identification |
| `share_checks_ok`, `all_kpis_ok` (industrial case) | share of KPI checks within tolerance and the all-checks flag |
| `elastic_clusters` (noise files) | clusters decoded with the elastic relaxation of the LP |

The tolerances (0.05 for machine shares and buffer full fractions, 0.5 parts for mean buffer occupancy, 10 % for WIP
and 5 % for residence times of the portions) are those of Section 3.4 of the paper; for the assembly line the checks
are evaluated from the `k_*` columns of the method and truth rows. Summary tables are documented by their headers and by
the Supplementary Material sources they correspond to (noted in `summary_tables/*.md`).
