# Identification variants, TEST (100 runs x 511 LFMs), mean over run x LFM pairs

| method | capacity correct | absD | MAE | within_1.0s | hidden_MAE | machine busy | machine blocked | machine idle | buffer mean occ | buffer full share | WIP sub-portion rel | all KPIs ok | viol_mean | viol_share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LP-max (nominal capacities) | 0.532 | 3.075 | 3.263 | 0.652 | 8.394 | 0.095 | 0.127 | 0.075 | 0.421 | 0.288 | 0.037 | 0.008 | 1.058 | 0.063 |
| Occupancy evidence only -> LP | 0.844 | 2.036 | 2.262 | 0.796 | 5.724 | 0.029 | 0.013 | 0.024 | 0.295 | 0.043 | 0.033 | 0.224 | 0.444 | 0.022 |
| Occupancy + LP-max log -> LP (operator-free hybrid) | 0.844 | 2.225 | 2.518 | 0.793 | 6.368 | 0.029 | 0.012 | 0.024 | 0.339 | 0.040 | 0.036 | 0.210 | 0.553 | 0.025 |
| Occupancy + LP-max log -> LP, iterated once | 0.844 | 2.225 | 2.518 | 0.793 | 6.368 | 0.029 | 0.012 | 0.024 | 0.339 | 0.040 | 0.036 | 0.210 | 0.553 | 0.025 |
| PINN, operator without physics term (lambda=0) | 0.827 | 1.400 | 1.142 | 0.548 | 3.070 | 0.025 | 0.021 | 0.014 | 0.152 | 0.042 | 0.007 | 0.147 | 0.602 | 0.231 |
| Hybrid, operator without physics term (lambda=0) | 0.827 | 1.985 | 2.231 | 0.784 | 5.645 | 0.029 | 0.013 | 0.024 | 0.291 | 0.042 | 0.032 | 0.203 | 0.429 | 0.026 |
| PINN, operator with physics term (lambda=1) | 0.822 | 1.273 | 1.088 | 0.631 | 2.886 | 0.020 | 0.019 | 0.014 | 0.148 | 0.043 | 0.007 | 0.185 | 0.476 | 0.194 |
| Hybrid, operator with physics term (lambda=1) | 0.822 | 1.954 | 2.203 | 0.781 | 5.571 | 0.029 | 0.013 | 0.024 | 0.286 | 0.042 | 0.032 | 0.194 | 0.414 | 0.027 |
| LP-true (reference) | 1.000 | 1.281 | 1.631 | 0.865 | 4.047 | 0.029 | 0.013 | 0.023 | 0.183 | 0.041 | 0.028 | 0.292 | 0.000 | 0.000 |

