"""Readers for the event logs of the repository (no dependency on the experiment code; needs pandas).

    import read_logs as RL
    ev  = RL.read_log('industrial_case/test_runs/run_000/21_HFM_log.txt.gz')   # one row per event (.gz read directly)
    tab = RL.event_table(ev)                                                   # items x (resource, enter/exit)
    cfg = RL.industrial_interfaces('industrial_case/lfm_catalog.csv', 'G15')   # sensed interfaces of G15
    lfm = RL.low_fidelity_log(ev, cfg)                                         # the low-fidelity log of G15
    lfm.to_csv('G15_run_000.txt', sep='\\t', index=False)

Interfaces are written 'A|B': the exit from A coincides with the entry into B. A low-fidelity log keeps the events at the
sensed interfaces and the line entries and final exits of every item, which are always observed.
"""
import pandas as pd

INDUSTRIAL_INTERFACES = ['B00|M01', 'B01|M02', 'B02|M03', 'B03|M05', 'B04|M06', 'B05|M07', 'B06|M08', 'B07|M09', 'B09|M13',
    'B10|M14', 'B11|M23', 'B12|M15', 'B13|M17', 'B14|M18', 'B15|M21', 'B17|M21', 'B18|M22', 'B19|M23', 'B20|M24', 'B21|M25',
    'B22|M26', 'M01|B01', 'M02|B02', 'M03|M04', 'M04|M19', 'M05|B04', 'M06|B05', 'M07|B06', 'M08|B07', 'M09|M10', 'M10|M11',
    'M11|M12', 'M12|B09', 'M13|B10', 'M14|B11', 'M15|M16', 'M16|B13', 'M17|B14', 'M18|B15', 'M19|M20', 'M20|B17', 'M21|B18',
    'M22|B19', 'M23|B20', 'M24|B21', 'M25|B22']          # order of the bits of lfm_catalog.csv
INDUSTRIAL_ALWAYS = ['B11|M23', 'B15|M21', 'B17|M21', 'B19|M23', 'M21|B18', 'M23|B20']
INDUSTRIAL_ROUTES = {'component02': ['B00', 'M01', 'B01', 'M02', 'B02', 'M03', 'M04', 'M19', 'M20', 'B17', 'M21'],
    'component01': ['B12', 'M15', 'M16', 'B13', 'M17', 'B14', 'M18', 'B15', 'M21', 'B18', 'M22', 'B19', 'M23'],
    'drawerSlide': ['B03', 'M05', 'B04', 'M06', 'B05', 'M07', 'B06', 'M08', 'B07', 'M09', 'M10', 'M11', 'M12', 'B09', 'M13',
                    'B10', 'M14', 'B11', 'M23', 'B20', 'M24', 'B21', 'M25', 'B22', 'M26']}
ASSEMBLY_OPTIONAL = ['B6|M7', 'M6|B6', 'B5|M6', 'M5|B5', 'B4|M5', 'M3|B3', 'M2|M3', 'B1|B2', 'M1|B1']
ASSEMBLY_ALWAYS = ['B2|M4', 'B3|M4', 'M4|B4']
ASSEMBLY_ROUTES = {'Part': ['M1', 'B1', 'B2', 'M4', 'B4', 'M5', 'B5', 'M6', 'B6', 'M7'], 'Component': ['M2', 'M3', 'B3', 'M4']}


def read_log(path):
    """HFM-format log -> DataFrame with columns id, time, event ('enter'/'exit'), resource, item_type, item_no."""
    d = pd.read_csv(path, sep='\t', encoding='utf-8-sig')
    d = d.rename(columns={'value1': 'event', 'value2': 'resource'}).drop(columns=['property'])
    d['item_type'] = d.id.str.split('.').str[0]
    d['item_no'] = d.id.str.split('.').str[1].astype(int)
    return d[['id', 'item_type', 'item_no', 'time', 'event', 'resource']]


def event_table(ev):
    """Events -> table indexed by item id with one column per (resource, event), values = times [s]."""
    return ev.pivot_table(index='id', columns=['resource', 'event'], values='time', aggfunc='first')


def industrial_interfaces(catalog_csv, name):
    """Sensed interfaces of configuration `name` (e.g. 'G15', '21_HFM_0', 'R12') of the industrial case."""
    c = pd.read_csv(catalog_csv, dtype={'bits': str}).set_index('name')
    bits = c.loc[name, 'bits']
    return [i for i, b in zip(INDUSTRIAL_INTERFACES, bits) if b == '1']


def assembly_interfaces(configurations_csv, lfm_id):
    """Sensed interfaces of configuration `lfm_id` (0..510) of the assembly line (the three around M4 included)."""
    c = pd.read_csv(configurations_csv).set_index('id')
    return ASSEMBLY_ALWAYS + [i for i in ASSEMBLY_OPTIONAL if c.loc[lfm_id, f'sensed_{i}']]


def low_fidelity_log(ev, sensed_interfaces, routes=None):
    """Keep the events at the sensed interfaces plus every item's line entry and final exit.
    routes: dict item_type -> ordered resources (default: picked by the item types found in the log)."""
    if routes is None:
        routes = INDUSTRIAL_ROUTES if ev.item_type.isin(INDUSTRIAL_ROUTES).all() else ASSEMBLY_ROUTES
    sensed = set(sensed_interfaces)
    keep = []
    for (t, r, e) in zip(ev.item_type, ev.resource, ev.event):
        route = routes[t]; k = route.index(r) if r in route else -1
        if k < 0:
            keep.append(False); continue
        if e == 'enter':
            keep.append(k == 0 or (k > 0 and f'{route[k-1]}|{r}' in sensed))
        else:
            keep.append(k == len(route) - 1 or (k + 1 < len(route) and f'{r}|{route[k+1]}' in sensed))
    return ev[pd.Series(keep, index=ev.index)].reset_index(drop=True)


def to_hfm(ev, path):
    """Write events back in the HFM format of the repository."""
    out = pd.DataFrame({'id': ev.id, 'time': ev.time.map(lambda x: f'{x:.4f}'), 'property': 'place', 'value1': ev.event, 'value2': ev.resource})
    out.to_csv(path, sep='\t', index=False)
