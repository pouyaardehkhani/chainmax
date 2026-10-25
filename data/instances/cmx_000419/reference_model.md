# Bounded integer reference model

Minimize 0 + 10 ship:R_W0_M0_standard:P0:0:0 + 10 ship:R_W0_M0_standard:P1:0:0 + 5 ship:R_W1_M0_standard:P0:0:0 + 5 ship:R_W1_M0_standard:P1:0:0 + 5 ship:R_W1_M1_standard:P0:0:0 + 5 ship:R_W1_M1_standard:P1:0:0 + 4 ship:R_W2_M1_standard:P0:0:0 + 4 ship:R_W2_M1_standard:P1:0:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 21], item.
- `inventory:M0:P1:0:0`: integer in [0, 21], item.
- `inventory:M1:P0:0:0`: integer in [0, 21], item.
- `inventory:M1:P1:0:0`: integer in [0, 21], item.
- `inventory:W0:P0:0:0`: integer in [0, 21], item.
- `inventory:W0:P1:0:0`: integer in [0, 21], item.
- `inventory:W1:P0:0:0`: integer in [0, 21], item.
- `inventory:W1:P1:0:0`: integer in [0, 21], item.
- `inventory:W2:P0:0:0`: integer in [0, 21], item.
- `inventory:W2:P1:0:0`: integer in [0, 21], item.
- `serve:M0:P0:0:0`: integer in [0, 5], item.
- `serve:M0:P1:0:0`: integer in [0, 3], item.
- `serve:M1:P0:0:0`: integer in [0, 5], item.
- `serve:M1:P1:0:0`: integer in [0, 2], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 13], item.
- `ship:R_W0_M0_standard:P1:0:0`: integer in [0, 13], item.
- `ship:R_W1_M0_standard:P0:0:0`: integer in [0, 5], item.
- `ship:R_W1_M0_standard:P1:0:0`: integer in [0, 5], item.
- `ship:R_W1_M1_standard:P0:0:0`: integer in [0, 10], item.
- `ship:R_W1_M1_standard:P1:0:0`: integer in [0, 10], item.
- `ship:R_W2_M0_standard:P0:0:0`: integer in [0, 8], item.
- `ship:R_W2_M0_standard:P1:0:0`: integer in [0, 8], item.
- `ship:R_W2_M1_standard:P0:0:0`: integer in [0, 2], item.
- `ship:R_W2_M1_standard:P1:0:0`: integer in [0, 2], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 eq 1. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W0:P1:0:0 + 1 ship:R_W0_M0_standard:P1:0:0 eq 2. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W1:P0:0:0 + 1 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M1_standard:P0:0:0 eq 5. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:W1:P1:0:0 + 1 ship:R_W1_M0_standard:P1:0:0 + 1 ship:R_W1_M1_standard:P1:0:0 eq 2. Source: balance/initial_stock/routes/recipes.
- c000004: 1 inventory:W2:P0:0:0 + 1 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M1_standard:P0:0:0 eq 6. Source: balance/initial_stock/routes/recipes.
- c000005: 1 inventory:W2:P1:0:0 + 1 ship:R_W2_M0_standard:P1:0:0 + 1 ship:R_W2_M1_standard:P1:0:0 eq 5. Source: balance/initial_stock/routes/recipes.
- c000006: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 + -1 ship:R_W1_M0_standard:P0:0:0 + -1 ship:R_W2_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000007: 1 inventory:M0:P1:0:0 + 1 serve:M0:P1:0:0 + -1 ship:R_W0_M0_standard:P1:0:0 + -1 ship:R_W1_M0_standard:P1:0:0 + -1 ship:R_W2_M0_standard:P1:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000008: 1 inventory:M1:P0:0:0 + 1 serve:M1:P0:0:0 + -1 ship:R_W1_M1_standard:P0:0:0 + -1 ship:R_W2_M1_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000009: 1 inventory:M1:P1:0:0 + 1 serve:M1:P1:0:0 + -1 ship:R_W1_M1_standard:P1:0:0 + -1 ship:R_W2_M1_standard:P1:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000010: 1 serve:M0:P0:0:0 eq 5. Source: demands.
- c000011: 1 serve:M0:P1:0:0 eq 3. Source: demands.
- c000012: 1 serve:M1:P0:0:0 eq 5. Source: demands.
- c000013: 1 serve:M1:P1:0:0 eq 2. Source: demands.
- c000014: 1 inventory:W0:P0:0:0 + 1 inventory:W0:P1:0:0 le 5. Source: locations/storage_capacity.
- c000015: 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M0_standard:P1:0:0 le 0. Source: locations/throughput_capacity.
- c000016: 1 inventory:W1:P0:0:0 + 1 inventory:W1:P1:0:0 le 0. Source: locations/storage_capacity.
- c000017: 1 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M0_standard:P1:0:0 + 1 ship:R_W1_M1_standard:P0:0:0 + 1 ship:R_W1_M1_standard:P1:0:0 le 10. Source: locations/throughput_capacity.
- c000018: 1 inventory:W2:P0:0:0 + 1 inventory:W2:P1:0:0 le 6. Source: locations/storage_capacity.
- c000019: 1 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M0_standard:P1:0:0 + 1 ship:R_W2_M1_standard:P0:0:0 + 1 ship:R_W2_M1_standard:P1:0:0 le 10. Source: locations/throughput_capacity.
- c000020: 1 inventory:M0:P0:0:0 + 1 inventory:M0:P1:0:0 le 3. Source: locations/storage_capacity.
- c000021: 0 le 2. Source: locations/throughput_capacity.
- c000022: 1 inventory:M1:P0:0:0 + 1 inventory:M1:P1:0:0 le 2. Source: locations/storage_capacity.
- c000023: 0 le 2. Source: locations/throughput_capacity.
- c000024: 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M0_standard:P1:0:0 le 13. Source: routes/capacity.
- c000025: 1 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M0_standard:P1:0:0 le 5. Source: routes/capacity.
- c000026: 1 ship:R_W1_M1_standard:P0:0:0 + 1 ship:R_W1_M1_standard:P1:0:0 le 10. Source: routes/capacity.
- c000027: 1 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M0_standard:P1:0:0 le 8. Source: routes/capacity.
- c000028: 1 ship:R_W2_M1_standard:P0:0:0 + 1 ship:R_W2_M1_standard:P1:0:0 le 2. Source: routes/capacity.
