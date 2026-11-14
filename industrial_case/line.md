# Industrial case (Section 5 of the paper)

Drawer-slide production line of Terkaj et al. (2021): 26 machines, 21 buffers, three item types.
Routes (resources in order):

- component02: B00 M01 B01 M02 B02 M03 M04 M19 M20 B17 M21 (assembled onto component01 at M21)
- component01: B12 M15 M16 B13 M17 B14 M18 B15 M21 B18 M22 B19 M23 (assembled onto the slide at M23)
- drawerSlide: B03 M05 B04 M06 B05 M07 B06 M08 B07 M09 M10 M11 M12 B09 M13 B10 M14 B11 M23 B20 M24 B21 M25 B22 M26

Standard processing times [s]: M03, M09, M11, M18, M19 5.14; M01, M02, M05, M06, M07, M08, M12, M13, M16, M21, M22,
M23, M24 10.28; M10, M14, M17, M20, M25, M26 15.42; M04, M15 20.56.
Maximum capacities: B00, B03, B12 20; B15 40; B11, B14, B17, B22 3; all other buffers 2.
Runs of 400 items per type; the first 1000 items by arrival form the log (as in the master log). Effective capacities,
items per type and seed of a run: `truth.json`.

Interfaces (46), in the order of the `bits` column of `lfm_catalog.csv`:
B00|M01, B01|M02, B02|M03, B03|M05, B04|M06, B05|M07, B06|M08, B07|M09, B09|M13, B10|M14, B11|M23, B12|M15, B13|M17,
B14|M18, B15|M21, B17|M21, B18|M22, B19|M23, B20|M24, B21|M25, B22|M26, M01|B01, M02|B02, M03|M04, M04|M19, M05|B04,
M06|B05, M07|B06, M08|B07, M09|M10, M10|M11, M11|M12, M12|B09, M13|B10, M14|B11, M15|M16, M16|B13, M17|B14, M18|B15,
M19|M20, M20|B17, M21|B18, M22|B19, M23|B20, M24|B21, M25|B22.
Always sensed: B11|M23, B15|M21, B17|M21, B19|M23, M21|B18, M23|B20; the other 40 are optional.

`lfm_catalog.csv`: the 1536 evaluated configurations — `21_HFM_<k>` the 323 given configurations of the reference
dataset, `R<k>` the 1172 random ones stratified by sensor count, `G00` … `G40` the greedy sensor-removal path selected
on validation runs (`G15`, `G17`, `G20` are the configurations discussed in the paper; G15 is drawn in Fig. 4).

Logs: `test_runs/run_XXX/21_HFM_log.txt.gz` (100 TEST runs, gzip-compressed), `out_of_range_runs/run_XXX/` (30 runs with every capacity
uniform over 1 … maximum, Section 5.3). Reconstructions: `reconstructions/<method>/run_XXX_<G15|G17|G20>.txt.gz` for
the first 30 TEST runs. Noise study: `noise_study/noisy_logs/sigma_<s>/run_XXX_21_HFM_log.txt.gz` are the TEST logs
with Gaussian timestamp noise of standard deviation `<s>` s on every interface (the noisy low-fidelity log of a
configuration is the restriction to its sensed interfaces); `noise_study/metrics/sigma_<s>/` the corresponding metrics.
