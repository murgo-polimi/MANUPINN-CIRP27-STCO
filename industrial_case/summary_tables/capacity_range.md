# Capacities uniform over 1..Kmax (30 runs, 238 LFMs; mean buffers out of the paper range per run: 3.3 of 21)

| method | capacity correct | absD_tot | hidden_within_1.0s | share_checks_ok | all_kpis_ok | n_runs |
|---|---|---|---|---|---|---|
| LP-max | 0.389 | 5.061 | 0.761 | 0.818 | 0.000 | 30.000 |
| LP-true (reference) | 1.000 | 0.343 | 0.961 | 0.985 | 0.720 | 30.000 |
| Occupancy -> LP, full range 1..Kmax | 0.705 | 2.769 | 0.870 | 0.964 | 0.469 | 30.000 |
| Occupancy -> LP, paper's range | 0.620 | 3.419 | 0.852 | 0.928 | 0.047 | 30.000 |


## G15

| method | all_kpis_ok | capacity correct |
|---|---|---|
| LP-max | 0.000 | 0.389 |
| LP-true (reference) | 0.867 | 1.000 |
| Occupancy -> LP, full range 1..Kmax | 0.833 | 0.802 |
| Occupancy -> LP, paper's range | 0.067 | 0.689 |


## G17

| method | all_kpis_ok | capacity correct |
|---|---|---|
| LP-max | 0.000 | 0.389 |
| LP-true (reference) | 0.933 | 1.000 |
| Occupancy -> LP, full range 1..Kmax | 0.900 | 0.811 |
| Occupancy -> LP, paper's range | 0.067 | 0.698 |


## G20

| method | all_kpis_ok | capacity correct |
|---|---|---|
| LP-max | 0.000 | 0.389 |
| LP-true (reference) | 0.933 | 1.000 |
| Occupancy -> LP, full range 1..Kmax | 0.933 | 0.821 |
| Occupancy -> LP, paper's range | 0.067 | 0.708 |

