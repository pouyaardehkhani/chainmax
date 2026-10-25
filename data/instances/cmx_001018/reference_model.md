# Bounded integer reference model

Minimize 0 + 4 ship:R_W0_M0_standard:P0:0:0 + 4 ship:R_W0_M0_standard:P1:0:0 + 12 ship:R_W1_M0_standard:P0:0:0 + 12 ship:R_W1_M0_standard:P1:0:0 + 4 ship:R_W2_M0_standard:P0:0:0 + 4 ship:R_W2_M0_standard:P1:0:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 14], item.
- `inventory:M0:P1:0:0`: integer in [0, 14], item.
- `inventory:W0:P0:0:0`: integer in [0, 14], item.
- `inventory:W0:P1:0:0`: integer in [0, 14], item.
- `inventory:W1:P0:0:0`: integer in [0, 14], item.
- `inventory:W1:P1:0:0`: integer in [0, 14], item.
- `inventory:W2:P0:0:0`: integer in [0, 14], item.
- `inventory:W2:P1:0:0`: integer in [0, 14], item.
- `serve:M0:P0:0:0`: integer in [0, 3], item.
- `serve:M0:P1:0:0`: integer in [0, 4], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 3], item.
- `ship:R_W0_M0_standard:P1:0:0`: integer in [0, 7], item.
- `ship:R_W1_M0_standard:P0:0:0`: integer in [0, 2], item.
- `ship:R_W1_M0_standard:P1:0:0`: integer in [0, 4], item.
- `ship:R_W2_M0_standard:P0:0:0`: integer in [0, 4], item.
- `ship:R_W2_M0_standard:P1:0:0`: integer in [0, 9], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W0:P1:0:0 + 1 ship:R_W0_M0_standard:P1:0:0 eq 7. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W1:P0:0:0 + 1 ship:R_W1_M0_standard:P0:0:0 eq 1. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:W1:P1:0:0 + 1 ship:R_W1_M0_standard:P1:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000004: 1 inventory:W2:P0:0:0 + 1 ship:R_W2_M0_standard:P0:0:0 eq 6. Source: balance/initial_stock/routes/recipes.
- c000005: 1 inventory:W2:P1:0:0 + 1 ship:R_W2_M0_standard:P1:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000006: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 + -1 ship:R_W1_M0_standard:P0:0:0 + -1 ship:R_W2_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000007: 1 inventory:M0:P1:0:0 + 1 serve:M0:P1:0:0 + -1 ship:R_W0_M0_standard:P1:0:0 + -1 ship:R_W1_M0_standard:P1:0:0 + -1 ship:R_W2_M0_standard:P1:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000008: 1 serve:M0:P0:0:0 eq 3. Source: demands.
- c000009: 1 serve:M0:P1:0:0 eq 4. Source: demands.
- c000010: 2 inventory:W0:P0:0:0 + 1 inventory:W0:P1:0:0 le 5. Source: locations/storage_capacity.
- c000011: 2 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M0_standard:P1:0:0 le 8. Source: locations/throughput_capacity.
- c000012: 2 inventory:W1:P0:0:0 + 1 inventory:W1:P1:0:0 le 2. Source: locations/storage_capacity.
- c000013: 2 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M0_standard:P1:0:0 le 0. Source: locations/throughput_capacity.
- c000014: 2 inventory:W2:P0:0:0 + 1 inventory:W2:P1:0:0 le 9. Source: locations/storage_capacity.
- c000015: 2 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M0_standard:P1:0:0 le 10. Source: locations/throughput_capacity.
- c000016: 2 inventory:M0:P0:0:0 + 1 inventory:M0:P1:0:0 le 2. Source: locations/storage_capacity.
- c000017: 0 le 0. Source: locations/throughput_capacity.
- c000018: 2 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M0_standard:P1:0:0 le 7. Source: routes/capacity.
- c000019: 2 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M0_standard:P1:0:0 le 4. Source: routes/capacity.
- c000020: 2 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M0_standard:P1:0:0 le 9. Source: routes/capacity.
