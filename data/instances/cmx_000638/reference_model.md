# Bounded integer reference model

Minimize 0 + 4 produce:B_W0:0 + 3 produce:B_W1:0 + 1 produce:B_W2:0 + 2 ship:R_W0_M0_standard:P0:0:0 + 7 ship:R_W1_M0_standard:P0:0:0 + 5 ship:R_W2_M0_standard:P0:0:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 27], item.
- `inventory:M0:RAW:0:0`: integer in [0, 27], item.
- `inventory:W0:P0:0:0`: integer in [0, 27], item.
- `inventory:W0:RAW:0:0`: integer in [0, 27], item.
- `inventory:W1:P0:0:0`: integer in [0, 27], item.
- `inventory:W1:RAW:0:0`: integer in [0, 27], item.
- `inventory:W2:P0:0:0`: integer in [0, 27], item.
- `inventory:W2:RAW:0:0`: integer in [0, 27], item.
- `produce:B_W0:0`: integer in [0, 1], batch.
- `produce:B_W1:0`: integer in [0, 1], batch.
- `produce:B_W2:0`: integer in [0, 6], batch.
- `serve:M0:P0:0:0`: integer in [0, 4], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 6], item.
- `ship:R_W1_M0_standard:P0:0:0`: integer in [0, 7], item.
- `ship:R_W2_M0_standard:P0:0:0`: integer in [0, 7], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + -2 produce:B_W0:0 + 1 ship:R_W0_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W0:RAW:0:0 + 1 produce:B_W0:0 eq 1. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W1:P0:0:0 + -1 produce:B_W1:0 + 1 ship:R_W1_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:W1:RAW:0:0 + 3 produce:B_W1:0 eq 3. Source: balance/initial_stock/routes/recipes.
- c000004: 1 inventory:W2:P0:0:0 + -1 produce:B_W2:0 + 1 ship:R_W2_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000005: 1 inventory:W2:RAW:0:0 + 3 produce:B_W2:0 eq 14. Source: balance/initial_stock/routes/recipes.
- c000006: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 + -1 ship:R_W1_M0_standard:P0:0:0 + -1 ship:R_W2_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000007: 1 inventory:M0:RAW:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000008: 1 serve:M0:P0:0:0 eq 4. Source: demands.
- c000009: 1 inventory:W0:P0:0:0 + 1 inventory:W0:RAW:0:0 le 1. Source: locations/storage_capacity.
- c000010: 1 ship:R_W0_M0_standard:P0:0:0 le 2. Source: locations/throughput_capacity.
- c000011: 1 inventory:W1:P0:0:0 + 1 inventory:W1:RAW:0:0 le 4. Source: locations/storage_capacity.
- c000012: 1 ship:R_W1_M0_standard:P0:0:0 le 2. Source: locations/throughput_capacity.
- c000013: 1 inventory:W2:P0:0:0 + 1 inventory:W2:RAW:0:0 le 6. Source: locations/storage_capacity.
- c000014: 1 ship:R_W2_M0_standard:P0:0:0 le 7. Source: locations/throughput_capacity.
- c000015: 1 inventory:M0:P0:0:0 + 1 inventory:M0:RAW:0:0 le 1. Source: locations/storage_capacity.
- c000016: 0 le 2. Source: locations/throughput_capacity.
- c000017: 1 ship:R_W0_M0_standard:P0:0:0 le 6. Source: routes/capacity.
- c000018: 1 ship:R_W1_M0_standard:P0:0:0 le 7. Source: routes/capacity.
- c000019: 1 ship:R_W2_M0_standard:P0:0:0 le 7. Source: routes/capacity.
