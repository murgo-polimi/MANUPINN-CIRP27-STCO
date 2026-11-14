# Filling the data repository from the GPU box (instructions for the experiment chat)

Written 14 Nov 2026 by the paper-writing chat. The skeleton of the repository (README, LICENSE, CITATION, FORMATS,
line descriptions, configuration catalogues, summary tables, `tools/`) is in the Mac project folder
`~/devprojects/MANUPINN CIRP/data_repository/`. The logs, reconstructions and per-run metrics live on the GPU box
and are exported by `tools/export_from_box.py`. **Nothing in the experiment folders is modified.**

1. Copy the repository skeleton to the box, e.g. `~/projects/data_repository/` (rsync the folder from the Mac).
2. From each case folder, with the PhysicsNeMo venv (torch is not needed):
   ```
   cd ~/projects/manuPINN\ CIRP/UseCase07 && NPROC=16 python ~/projects/data_repository/tools/export_from_box.py assembly   ~/projects/data_repository
   cd ~/projects/manuPINN\ CIRP/UseCase21 && NPROC=16 python ~/projects/data_repository/tools/export_from_box.py industrial ~/projects/data_repository
   ```
   Both are resumable. Environment variables if the layout differs from the defaults: `UC07_EVAL` (default
   `eval_v22h`), `UC07_TAG` (`v2`), `UC21_EVAL` (`eval`), `UC21_TAG` (`v1l01`). The hybrid reconstructions are
   recomputed with the LP (assembly line: all 511 configurations per run, ~seconds; industrial case: G15/G17/G20 on
   30 runs). Expected time: well under an hour per case.
3. Report sizes: `du -sh */test_runs */val_runs */out_of_range_runs */reconstructions */metrics */metrics_full
   industrial_case/noise_study`, the number of files, and any step that failed (do not patch around a failure; report
   the traceback). `metrics_full/` is excluded from git (`.gitignore`) and is meant for a separate archive (Zenodo) if
   the authors decide to publish the raw evaluation files.
4. Copy the filled repository back to the Mac folder (`rsync -a --exclude metrics_full`), and the E7 tables
   (`sensor_select_val.csv/.md`, `val_per_cfg.csv`) that the script places in `assembly_line/summary_tables/`.
5. Write a short note `claude/data_repository_export.md` in the project: what was exported, sizes, deviations.

The paper chat will then review the README against the content, and the authors create the GitHub repository
(licence template: Creative Commons Attribution 4.0) and push.
