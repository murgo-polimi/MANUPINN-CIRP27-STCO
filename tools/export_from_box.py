r"""Export of the data repository from the experiment folders on the GPU box (not part of the published repository).

Run from the case folder, with the PhysicsNeMo venv (numpy, pandas; no torch needed):
    cd ~/projects/manuPINN\ CIRP/UseCase07 && python <repo>/tools/export_from_box.py assembly   <repo>
    cd ~/projects/manuPINN\ CIRP/UseCase21 && python <repo>/tools/export_from_box.py industrial <repo>
<repo> is the root of the data repository (its README.md, assembly_line/, industrial_case/ already exist).
Every step is resumable (existing output files are skipped). What is written:

assembly_line/
  test_runs/run_XXX/07_HFM_log.txt, params.json           copied from sims_v2/test
  val_runs/run_XXX/07_HFM_log.txt, params.json            written from sims_val/test (truth.npz) and sims_v2/val/params.csv
  reconstructions/<pi_fno|hybrid|lp_max|lp_true>/run_XXX_lfm_<id>.txt.gz   HFM-format logs for SELECTED_07 (the
      configurations discussed in Section 4.2 and Suppl. Table S2); the hybrid is recomputed with hybrid.hybrid()
  metrics/test_run_XXX.csv.gz, val_run_XXX.csv.gz          compact per-(run, configuration, method) metrics
  metrics_full/ (not committed; for an archive)            the raw evaluation files
  summary_tables/                                          E7 tables (sensor_select_val.*, val_per_cfg.csv)
industrial_case/
  test_runs/run_XXX/21_HFM_log.txt, truth.json             written from sims/test/run_XXX/truth.npz
  out_of_range_runs/run_XXX/21_HFM_log.txt, truth.json     from sims/test_widecap
  reconstructions/<method>/run_XXX_<G15|G17|G20>.txt.gz    first 30 TEST runs; hybrid recomputed with the LP
  metrics/test_run_XXX.csv.gz, out_of_range_run_XXX.csv.gz, noise_study/metrics/sigma_<s>/test_run_XXX.csv.gz,
      master_log/real.csv.gz                               compact metrics
  noise_study/noisy_logs/sigma_<s>/run_XXX_21_HFM_log.txt.gz   the noisy sensed timestamps (all 46 interfaces, from
      the same seeds as the experiment; a configuration's noisy low-fidelity log is its restriction)
  metrics_full/                                            raw evaluation files (not committed)
"""
import os, sys, json, glob, gzip, shutil, numpy as np, pandas as pd

SELECTED_07 = sorted({364, 338, 82, 18, 346, 330, 244, 116, 52, 20, 372, 340, 84, 180, 148, 132, 468, 212, 144})
GREEDY_21 = ['G15', 'G17', 'G20']; N_RECON_21 = 30
METHOD_DIR = {'op': 'pi_fno', 'hyb': 'hybrid', 'lp_max': 'lp_max', 'lp_true': 'lp_true'}


def _skip(path):
    return os.path.exists(path)


def _write_gz_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with gzip.open(path + '.tmp', 'wt') as f:
        f.write(text)
    os.replace(path + '.tmp', path)


def _hfm_text_07(T):
    """T (N,15) -> HFM-format text (same layout as scenario.write_hfm_log)."""
    import scenario as SC
    rows = []
    for k in range(SC.N):
        for r in ['M2', 'M3', 'B3']:
            a, b = SC.RES_BOUNDS[r]; rows.append(f'Component.{k+1}\t{T[k, a]:.4f}\tplace\tenter\t{r}'); rows.append(f'Component.{k+1}\t{T[k, b]:.4f}\tplace\texit\t{r}')
        for r in ['M1', 'B1', 'B2', 'M4', 'B4', 'M5', 'B5', 'M6', 'B6', 'M7']:
            a, b = SC.RES_BOUNDS[r]; rows.append(f'Part.{k+1}\t{T[k, a]:.4f}\tplace\tenter\t{r}'); rows.append(f'Part.{k+1}\t{T[k, b]:.4f}\tplace\texit\t{r}')
    return 'id\ttime\tproperty\tvalue1\tvalue2\n' + '\n'.join(rows) + '\n'


# ====================================================================== assembly line (UseCase07)
def assembly(repo):
    sys.path.insert(0, os.path.join('reconstruction', 'exp')); sys.path.insert(0, 'reconstruction')
    import scenario as SC, analyze as AN
    R = os.path.join(repo, 'assembly_line'); SIMS = SC.SIMS_DIR; OUT = SC.EXP_DIR
    EVAL = os.environ.get('UC07_EVAL', 'eval_v22h')
    # 1. TEST runs
    for r in range(100):
        d = os.path.join(R, 'test_runs', f'run_{r:03d}'); os.makedirs(d, exist_ok=True)
        for f in ('07_HFM_log.txt', 'params.json'):
            if not _skip(os.path.join(d, f)):
                shutil.copy(os.path.join(SIMS, 'test', f'run_{r:03d}', f), os.path.join(d, f))
    print('test runs done', flush=True)
    # 2. VAL runs (50): logs from the extracted subset, parameters from val/params.csv
    P = pd.read_csv(os.path.join(SIMS, 'val', 'params.csv'))
    vs = os.path.join('reconstruction', 'sims_val', 'test')
    for r in range(50):
        d = os.path.join(R, 'val_runs', f'run_{r:03d}'); os.makedirs(d, exist_ok=True)
        if _skip(os.path.join(d, 'params.json')):
            continue
        tr = np.load(os.path.join(vs, f'run_{r:03d}', 'truth.npz'))
        open(os.path.join(d, '07_HFM_log.txt'), 'w').write(_hfm_text_07(tr['T']))
        row = {k: (v.item() if hasattr(v, 'item') else v) for k, v in P.iloc[r].items()}
        row.update(run=f'run_{r:03d}', standard_times=SC.STD, max_capacities=SC.KMAX, note='VAL run (first 50 of the validation set), used to select the sensor configurations')
        json.dump(row, open(os.path.join(d, 'params.json'), 'w'), indent=1, default=str)
    print('val runs done', flush=True)
    # 3. reconstructions for the selected configurations (TEST); hybrid recomputed
    import hybrid as HY
    from multiprocessing import Pool
    tag = os.environ.get('UC07_TAG', 'v2')
    with Pool(int(os.environ.get('NPROC', '16'))) as pool:
        for r in range(100):
            todo = [(m, c) for m in METHOD_DIR for c in SELECTED_07
                    if not _skip(os.path.join(R, 'reconstructions', METHOD_DIR[m], f'run_{r:03d}_lfm_{c:03d}.txt.gz'))]
            if not todo:
                continue
            tr = np.load(os.path.join(SIMS, 'test', f'run_{r:03d}', 'truth.npz')); Tt = tr['T']
            op = np.load(os.path.join(OUT, tag, 'test', f'run_{r:03d}.npz'))['op']
            bl = np.load(os.path.join(OUT, 'baseline', 'test', f'run_{r:03d}.npz'))
            H, _ = HY.hybrid(Tt, op, pool)                                   # (511,N,15), all configurations
            recs = {'op': op, 'hyb': H, 'lp_max': bl['lp_max'], 'lp_true': bl['lp_true']}
            for m, c in todo:
                _write_gz_text(os.path.join(R, 'reconstructions', METHOD_DIR[m], f'run_{r:03d}_lfm_{c:03d}.txt.gz'), _hfm_text_07(recs[m][c]))
            print('reconstructions run', r, flush=True)
    # 4. metrics: compact (committed) and full (archive)
    def compact07(df):
        E = AN.errors(df); A = AN.compact(E)
        A = A.rename(columns={'cfg': 'lfm', 'n': 'n_optional', 'absD': 'absD_tot', 'MAE': 'time_MAE'})
        caps = df[df.method != 'truth'][['run', 'cfg', 'method'] + [f'k_{b}_capacity' for b in SC.BUFFERS]].rename(columns={'cfg': 'lfm'})
        return A.merge(caps, on=['run', 'lfm', 'method'], how='left')
    for src, dst_fmt, n in ((os.path.join(OUT, EVAL), 'test_run_{:03d}', 100), (os.path.join('reconstruction', 'out', 'exp_val', EVAL), 'val_run_{:03d}', 50)):
        for r in range(n):
            f = os.path.join(src, f'test_run_{r:03d}.csv'); name = dst_fmt.format(r)
            full = os.path.join(R, 'metrics_full', name + '.csv.gz'); comp = os.path.join(R, 'metrics', name + '.csv.gz')
            if _skip(comp):
                continue
            df = pd.read_csv(f)
            os.makedirs(os.path.dirname(full), exist_ok=True); df.to_csv(full, index=False, compression='gzip')
            os.makedirs(os.path.dirname(comp), exist_ok=True); compact07(df).to_csv(comp, index=False, compression='gzip')
        print('metrics', dst_fmt, 'done', flush=True)
    # 5. E7 tables
    for f in glob.glob(os.path.join(OUT, 'summary_v22h', 'sensor_select_val.*')) + glob.glob(os.path.join(OUT, 'summary_v22h', 'val_per_cfg.csv')):
        shutil.copy(f, os.path.join(R, 'summary_tables', os.path.basename(f)))
    print('assembly line export finished', flush=True)


# ====================================================================== industrial case (UseCase21)
def industrial(repo):
    sys.path.insert(0, os.path.join('reconstruction', 'exp')); sys.path.insert(0, 'reconstruction')
    import line21 as L, scenario as SC, analyze as AN
    R = os.path.join(repo, 'industrial_case'); SIMS = SC.SIMS_DIR; OUT = SC.EXP_DIR
    EVAL = os.environ.get('UC21_EVAL', 'eval')
    C, masks = SC.masks_from_catalog(); names = list(C.name)

    def write_run(src_dir, dst_dir, note):
        if _skip(os.path.join(dst_dir, 'truth.json')):
            return
        os.makedirs(dst_dir, exist_ok=True)
        tr = np.load(os.path.join(src_dir, 'truth.npz'))
        L.write_hfm_log(os.path.join(dst_dir, '21_HFM_log.txt'), tr['T'], tr['n'], tr['gid'])
        info = {f'K_{b}': int(k) for b, k in zip(SC.BUFFERS, tr['K'])}
        info.update(items_per_type={t: int(v) for t, v in zip(L.TYPES, tr['n'])}, max_capacities=SC.KMAX, standard_times={m: float(L.S[m]) for m in SC.MACHINES}, note=note)
        json.dump(info, open(os.path.join(dst_dir, 'truth.json'), 'w'), indent=1)
    # 1. TEST and out-of-range runs
    for r in range(100):
        write_run(os.path.join(SIMS, 'test', f'run_{r:03d}'), os.path.join(R, 'test_runs', f'run_{r:03d}'), 'TEST run')
    print('test runs done', flush=True)
    for r in range(30):
        write_run(os.path.join(SIMS, 'test_widecap', f'run_{r:03d}'), os.path.join(R, 'out_of_range_runs', f'run_{r:03d}'), 'run with capacities uniform over 1..max (Section 5.3, Suppl. Table S4)')
    print('out-of-range runs done', flush=True)
    # 2. reconstructions for G15, G17, G20 on the first N_RECON_21 TEST runs; hybrid recomputed with the LP
    import evaluate as EV, capacity as CAP
    from multiprocessing import Pool
    tag = os.environ.get('UC21_TAG', 'v1l01')
    idx = {g: names.index(g) for g in GREEDY_21}
    with Pool(int(os.environ.get('NPROC', '16'))) as pool:
        for r in range(N_RECON_21):
            todo = [(m, g) for m in METHOD_DIR for g in GREEDY_21
                    if not _skip(os.path.join(R, 'reconstructions', METHOD_DIR[m], f'run_{r:03d}_{g}.txt.gz'))]
            if not todo:
                continue
            tr = np.load(os.path.join(SIMS, 'test', f'run_{r:03d}', 'truth.npz'))
            Tt = np.where(L.valid_mask(tr['n'], SC.N), tr['T'], np.nan)
            p = np.load(os.path.join(OUT, tag, 'test', f'run_{r:03d}.npz'), allow_pickle=True)
            bl = np.load(os.path.join(OUT, 'baseline', 'test', f'run_{r:03d}.npz'), allow_pickle=True)
            assert list(p['names']) == names == list(bl['names'])
            sel = [idx[g] for g in GREEDY_21]
            op = p['op'][sel].astype(np.float64)
            Kh, _, _ = CAP.identify(op, masks[sel])
            hyb = pool.map(EV._hyb, [(Tt, masks[sel][i], Kh[i]) for i in range(len(sel))])
            recs = {'op': op, 'hyb': np.stack(hyb), 'lp_max': bl['lp_max'][sel], 'lp_true': bl['lp_true'][sel]}
            for m, g in todo:
                i = GREEDY_21.index(g); T = np.asarray(recs[m][i], float)
                tmp = os.path.join(R, 'reconstructions', METHOD_DIR[m], f'run_{r:03d}_{g}.tmp.txt')
                os.makedirs(os.path.dirname(tmp), exist_ok=True)
                L.write_hfm_log(tmp, np.where(np.isnan(T), 0.0, T), tr['n'], tr['gid'])
                _write_gz_text(tmp.replace('.tmp.txt', '.txt.gz'), open(tmp).read()); os.remove(tmp)
            print('reconstructions run', r, flush=True)
    # 3. metrics (compact + full)
    def compact21(df):
        E = AN.errors(df); A = AN.compact(E)
        caps = df[df.method != 'truth'][['run', 'lfm', 'method'] + [f'k_{b}_capacity' for b in SC.BUFFERS if f'k_{b}_capacity' in df.columns]]
        extra = [c for c in ('sigma', 'elastic_clusters', 'obs_rms_err') if c in df.columns]
        if extra:
            caps = caps.join(df.loc[df.method != 'truth', extra])
        return A.merge(caps, on=['run', 'lfm', 'method'], how='left')
    def export_metrics(src_glob, dst_dir, rename=lambda b: b):
        for f in sorted(glob.glob(src_glob)):
            name = rename(os.path.basename(f).replace('.csv.gz', '').replace('.csv', ''))
            comp = os.path.join(dst_dir, name + '.csv.gz'); full = os.path.join(R, 'metrics_full', os.path.relpath(comp, R))
            if _skip(comp):
                continue
            df = pd.read_csv(f)
            os.makedirs(os.path.dirname(full), exist_ok=True); df.to_csv(full, index=False, compression='gzip')
            os.makedirs(os.path.dirname(comp), exist_ok=True); compact21(df).to_csv(comp, index=False, compression='gzip')
        print('metrics', dst_dir, 'done', flush=True)
    export_metrics(os.path.join(OUT, EVAL, 'test_run_*.csv.gz'), os.path.join(R, 'metrics'))
    export_metrics(os.path.join(OUT, 'eval_widecap', 'test_run_*.csv.gz'), os.path.join(R, 'metrics'), lambda b: b.replace('test_run', 'out_of_range_run'))
    for sd in sorted(glob.glob(os.path.join(OUT, 'eval_noise_tol', 'sigma_*'))):
        export_metrics(os.path.join(sd, 'test_run_*.csv.gz'), os.path.join(R, 'noise_study', 'metrics', os.path.basename(sd)))
    export_metrics(os.path.join(OUT, EVAL, 'real.csv.gz'), os.path.join(R, 'master_log'))
    # 4. noisy logs: regenerate the noisy sensed timestamps with the seeds of the experiment (all interfaces sensed)
    import noise_sensitivity as NS
    for si, sigma in enumerate(NS.SIGMAS):
        if sigma == 0:
            continue
        for r in range(30):
            dst = os.path.join(R, 'noise_study', 'noisy_logs', f'sigma_{sigma:g}', f'run_{r:03d}_21_HFM_log.txt.gz')
            if _skip(dst):
                continue
            tr = np.load(os.path.join(SIMS, 'test', f'run_{r:03d}', 'truth.npz'))
            Tt = np.where(L.valid_mask(tr['n'], SC.N), tr['T'], np.nan)
            Tn = NS.add_noise(Tt, sigma, np.random.default_rng(10000 * si + r))
            tmp = dst.replace('.txt.gz', '.tmp.txt'); os.makedirs(os.path.dirname(tmp), exist_ok=True)
            L.write_hfm_log(tmp, np.where(np.isnan(Tn), 0.0, Tn), tr['n'], tr['gid'])
            _write_gz_text(dst, open(tmp).read()); os.remove(tmp)
        print('noisy logs sigma', sigma, 'done', flush=True)
    print('industrial case export finished', flush=True)


if __name__ == '__main__':
    {'assembly': assembly, 'industrial': industrial}[sys.argv[1]](os.path.abspath(sys.argv[2]))
