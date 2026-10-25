# Bounded integer reference model

Minimize 0 + 1 ship:R_H0_M0_standard:P0:0:0 + 5 ship:R_W0_H0_standard:P0:0:0 + 6 ship:R_W1_H0_standard:P0:0:0 + 4 ship:R_W2_H0_standard:P0:0:0

## Variables

- `inventory:H0:P0:0:0`: integer in [0, 5], item.
- `inventory:M0:P0:0:0`: integer in [0, 5], item.
- `inventory:W0:P0:0:0`: integer in [0, 5], item.
- `inventory:W1:P0:0:0`: integer in [0, 5], item.
- `inventory:W2:P0:0:0`: integer in [0, 5], item.
- `serve:M0:P0:0:0`: integer in [0, 2], item.
- `ship:R_H0_M0_standard:P0:0:0`: integer in [0, 2], item.
- `ship:R_W0_H0_standard:P0:0:0`: integer in [0, 5], item.
- `ship:R_W1_H0_standard:P0:0:0`: integer in [0, 3], item.
- `ship:R_W2_H0_standard:P0:0:0`: integer in [0, 5], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_H0_standard:P0:0:0 eq 3. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 + 1 ship:R_W1_H0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W2:P0:0:0 + 1 ship:R_W2_H0_standard:P0:0:0 eq 2. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:H0:P0:0:0 + 1 ship:R_H0_M0_standard:P0:0:0 + -1 ship:R_W0_H0_standard:P0:0:0 + -1 ship:R_W1_H0_standard:P0:0:0 + -1 ship:R_W2_H0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000004: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_H0_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000005: 1 serve:M0:P0:0:0 eq 2. Source: demands.
- c000006: 1 inventory:W0:P0:0:0 le 3. Source: locations/storage_capacity.
- c000007: 1 ship:R_W0_H0_standard:P0:0:0 le 6. Source: locations/throughput_capacity.
- c000008: 1 inventory:W1:P0:0:0 le 1. Source: locations/storage_capacity.
- c000009: 1 ship:R_W1_H0_standard:P0:0:0 le 0. Source: locations/throughput_capacity.
- c000010: 1 inventory:W2:P0:0:0 le 5. Source: locations/storage_capacity.
- c000011: 1 ship:R_W2_H0_standard:P0:0:0 le 1. Source: locations/throughput_capacity.
- c000012: 1 inventory:H0:P0:0:0 le 2. Source: locations/storage_capacity.
- c000013: 1 ship:R_H0_M0_standard:P0:0:0 le 4. Source: locations/throughput_capacity.
- c000014: 1 inventory:M0:P0:0:0 le 2. Source: locations/storage_capacity.
- c000015: 0 le 4. Source: locations/throughput_capacity.
- c000016: 1 ship:R_H0_M0_standard:P0:0:0 le 2. Source: routes/capacity.
- c000017: 1 ship:R_W0_H0_standard:P0:0:0 le 5. Source: routes/capacity.
- c000018: 1 ship:R_W1_H0_standard:P0:0:0 le 3. Source: routes/capacity.
- c000019: 1 ship:R_W2_H0_standard:P0:0:0 le 7. Source: routes/capacity.
