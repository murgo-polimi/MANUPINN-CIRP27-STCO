# Assembly line (running example; Section 2 and 4 of the paper)

Seven machines and six buffers. Part route M1 → B1 → B2 → M4 → B4 → M5 → B5 → M6 → B6 → M7; component route
M2 → M3 → B3 → M4; M4 assembles one part with one component. Runs of 200 parts and 200 components.

| | M1 | M2 | M3 | M4 | M5 | M6 | M7 |
|---|---|---|---|---|---|---|---|
| standard processing time [s] | 5 | 3 | 3 | 10 | 11 | 12 | 13 |

| | B1 | B2 | B3 | B4 | B5 | B6 |
|---|---|---|---|---|---|---|
| maximum capacity | 5 | 4 | 10 | 7 | 6 | 7 |

Effective capacities of a run: `params.json` (`K_B1` … `K_B6`), sampled as described in Section 3.4 of the paper.

Interfaces: always sensed B2|M4, B3|M4, M4|B4; optional (nine) B6|M7, M6|B6, B5|M6, M5|B5, B4|M5, M3|B3, M2|M3,
B1|B2, M1|B1. `configurations.csv` lists the 511 sensor configurations (all subsets of the optional interfaces) with
their `id` (the LFM id used in the paper and in the file names of `reconstructions/`), `n_sensors` (including the three
always sensed), `clusters` (the unobserved sections), the numbers of partially observed and hidden events and the
`sensed_<interface>` flags.

Logs: `test_runs/run_XXX/07_HFM_log.txt.gz` (complete event log, gzip-compressed) with `params.json`; `val_runs/` the same for the first
50 validation runs. Reconstructions: `reconstructions/<pi_fno|hybrid|lp_max|lp_true>/run_XXX_lfm_<id>.txt.gz`,
complete logs reconstructed from the low-fidelity log of configuration `<id>`, for the configurations discussed in
Section 4.2 and Supplementary Table S2.
