# Bounded integer reference model

Minimize 0 + 5 ship:R_W0_M0_standard:P0:0:0 + 2 ship:R_W0_M1_standard:P0:0:0 + 3 ship:R_W1_M0_standard:P0:0:0 + 7 ship:R_W1_M1_standard:P0:0:0 + 8 ship:R_W2_M1_standard:P0:0:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 12], item.
- `inventory:M1:P0:0:0`: integer in [0, 12], item.
- `inventory:W0:P0:0:0`: integer in [0, 12], item.
- `inventory:W1:P0:0:0`: integer in [0, 12], item.
- `inventory:W2:P0:0:0`: integer in [0, 12], item.
- `serve:M0:P0:0:0`: integer in [0, 4], item.
- `serve:M1:P0:0:0`: integer in [0, 5], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 7], item.
- `ship:R_W0_M1_standard:P0:0:0`: integer in [0, 4], item.
- `ship:R_W1_M0_standard:P0:0:0`: integer in [0, 6], item.
- `ship:R_W1_M1_standard:P0:0:0`: integer in [0, 6], item.
- `ship:R_W2_M1_standard:P0:0:0`: integer in [0, 7], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M1_standard:P0:0:0 eq 1. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 + 1 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M1_standard:P0:0:0 eq 4. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W2:P0:0:0 + 1 ship:R_W2_M1_standard:P0:0:0 eq 7. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 + -1 ship:R_W1_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000004: 1 inventory:M1:P0:0:0 + 1 serve:M1:P0:0:0 + -1 ship:R_W0_M1_standard:P0:0:0 + -1 ship:R_W1_M1_standard:P0:0:0 + -1 ship:R_W2_M1_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000005: 1 serve:M0:P0:0:0 eq 4. Source: demands.
- c000006: 1 serve:M1:P0:0:0 eq 5. Source: demands.
- c000007: 1 inventory:W0:P0:0:0 le 1. Source: locations/storage_capacity.
- c000008: 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M1_standard:P0:0:0 le 2. Source: locations/throughput_capacity.
- c000009: 1 inventory:W1:P0:0:0 le 0. Source: locations/storage_capacity.
- c000010: 1 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M1_standard:P0:0:0 le 6. Source: locations/throughput_capacity.
- c000011: 1 inventory:W2:P0:0:0 le 2. Source: locations/storage_capacity.
- c000012: 1 ship:R_W2_M1_standard:P0:0:0 le 8. Source: locations/throughput_capacity.
- c000013: 1 inventory:M0:P0:0:0 le 3. Source: locations/storage_capacity.
- c000014: 0 le 2. Source: locations/throughput_capacity.
- c000015: 1 inventory:M1:P0:0:0 le 3. Source: locations/storage_capacity.
- c000016: 0 le 3. Source: locations/throughput_capacity.
- c000017: 1 ship:R_W0_M0_standard:P0:0:0 le 7. Source: routes/capacity.
- c000018: 1 ship:R_W0_M1_standard:P0:0:0 le 4. Source: routes/capacity.
- c000019: 1 ship:R_W1_M0_standard:P0:0:0 le 6. Source: routes/capacity.
- c000020: 1 ship:R_W1_M1_standard:P0:0:0 le 6. Source: routes/capacity.
- c000021: 1 ship:R_W2_M1_standard:P0:0:0 le 7. Source: routes/capacity.
