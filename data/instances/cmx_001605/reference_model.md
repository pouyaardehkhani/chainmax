# Bounded integer reference model

Minimize 0 + 2 ship:R_H0_M0_standard:P0:0:0 + 8 ship:R_W0_H0_standard:P0:0:0 + 5 ship:R_W1_H0_standard:P0:0:0

## Variables

- `inventory:H0:P0:0:0`: integer in [0, 6], item.
- `inventory:M0:P0:0:0`: integer in [0, 6], item.
- `inventory:W0:P0:0:0`: integer in [0, 6], item.
- `inventory:W1:P0:0:0`: integer in [0, 6], item.
- `serve:M0:P0:0:0`: integer in [0, 2], item.
- `ship:R_H0_M0_standard:P0:0:0`: integer in [0, 4], item.
- `ship:R_W0_H0_standard:P0:0:0`: integer in [0, 6], item.
- `ship:R_W1_H0_standard:P0:0:0`: integer in [0, 5], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_H0_standard:P0:0:0 eq 1. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 + 1 ship:R_W1_H0_standard:P0:0:0 eq 5. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:H0:P0:0:0 + 1 ship:R_H0_M0_standard:P0:0:0 + -1 ship:R_W0_H0_standard:P0:0:0 + -1 ship:R_W1_H0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_H0_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000004: 1 serve:M0:P0:0:0 eq 2. Source: demands.
- c000005: 1 inventory:W0:P0:0:0 le 5. Source: locations/storage_capacity.
- c000006: 1 ship:R_W0_H0_standard:P0:0:0 le 1. Source: locations/throughput_capacity.
- c000007: 1 inventory:W1:P0:0:0 le 5. Source: locations/storage_capacity.
- c000008: 1 ship:R_W1_H0_standard:P0:0:0 le 5. Source: locations/throughput_capacity.
- c000009: 1 inventory:H0:P0:0:0 le 2. Source: locations/storage_capacity.
- c000010: 1 ship:R_H0_M0_standard:P0:0:0 le 5. Source: locations/throughput_capacity.
- c000011: 1 inventory:M0:P0:0:0 le 2. Source: locations/storage_capacity.
- c000012: 0 le 2. Source: locations/throughput_capacity.
- c000013: 1 ship:R_H0_M0_standard:P0:0:0 le 4. Source: routes/capacity.
- c000014: 1 ship:R_W0_H0_standard:P0:0:0 le 7. Source: routes/capacity.
- c000015: 1 ship:R_W1_H0_standard:P0:0:0 le 5. Source: routes/capacity.
