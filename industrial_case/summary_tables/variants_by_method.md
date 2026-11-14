# Identification variants, TEST (100 runs x 1536 LFMs), mean over run x LFM pairs

| method | capacity correct | absD_tot | time_MAE | hidden_within_1.0s | hidden_MAE | machine busy | machine blocked | machine idle | buffer mean occ | buffer full share | WIP sub-portion rel | share_checks_ok | all_kpis_ok | viol_mean | viol_share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LP-max (nominal capacities) | 0.520 | 3.634 | 6.276 | 0.752 | 11.856 | 0.064 | 0.087 | 0.029 | 0.133 | 0.153 | 0.031 | 0.852 | 0.000 | 1.365 | 0.034 |
| Occupancy evidence only -> LP | 0.768 | 1.816 | 3.488 | 0.866 | 5.981 | 0.005 | 0.006 | 0.007 | 0.071 | 0.008 | 0.015 | 0.964 | 0.418 | 0.509 | 0.012 |
| Occupancy + LP-max log -> LP (operator-free hybrid) | 0.767 | 2.120 | 4.293 | 0.851 | 7.205 | 0.005 | 0.006 | 0.007 | 0.089 | 0.007 | 0.018 | 0.962 | 0.406 | 0.671 | 0.016 |
| Occupancy + LP-max log -> LP, iterated once | 0.767 | 2.120 | 4.293 | 0.851 | 7.205 | 0.005 | 0.006 | 0.007 | 0.089 | 0.007 | 0.018 | 0.962 | 0.406 | 0.671 | 0.016 |
| PINN, operator without physics term (lambda=0) | 0.776 | 3.553 | 3.365 | 0.412 | 7.260 | 0.033 | 0.038 | 0.018 | 0.072 | 0.038 | 0.010 | 0.869 | 0.053 | 1.425 | 0.211 |
| Hybrid, operator without physics term (lambda=0) | 0.776 | 1.684 | 2.943 | 0.873 | 5.191 | 0.005 | 0.006 | 0.006 | 0.067 | 0.008 | 0.015 | 0.965 | 0.415 | 0.472 | 0.012 |
| PINN, operator with physics term (lambda=0.1) | 0.767 | 3.548 | 3.635 | 0.409 | 7.521 | 0.027 | 0.047 | 0.028 | 0.083 | 0.031 | 0.015 | 0.859 | 0.077 | 1.276 | 0.186 |
| Hybrid, operator with physics term (lambda=0.1) | 0.767 | 1.871 | 3.239 | 0.865 | 5.658 | 0.005 | 0.006 | 0.006 | 0.075 | 0.008 | 0.015 | 0.963 | 0.402 | 0.557 | 0.014 |
| LP-true (reference) | 1.000 | 0.597 | 1.281 | 0.945 | 2.135 | 0.005 | 0.005 | 0.006 | 0.019 | 0.006 | 0.011 | 0.976 | 0.603 | 0.000 | 0.000 |

