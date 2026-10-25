# Bounded integer reference model

Minimize 0 + 7 produce:B_W0:0 + 6 produce:B_W1:0 + 2 ship:R_W0_M0_standard:P0:0:0 + 8 ship:R_W1_M0_standard:P0:0:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 12], item.
- `inventory:M0:RAW:0:0`: integer in [0, 12], item.
- `inventory:W0:P0:0:0`: integer in [0, 12], item.
- `inventory:W0:RAW:0:0`: integer in [0, 12], item.
- `inventory:W1:P0:0:0`: integer in [0, 12], item.
- `inventory:W1:RAW:0:0`: integer in [0, 12], item.
- `produce:B_W0:0`: integer in [0, 1], batch.
- `produce:B_W1:0`: integer in [0, 3], batch.
- `serve:M0:P0:0:0`: integer in [0, 4], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 3], item.
- `ship:R_W1_M0_standard:P0:0:0`: integer in [0, 8], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + -1 produce:B_W0:0 + 1 ship:R_W0_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W0:RAW:0:0 + 3 produce:B_W0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W1:P0:0:0 + -2 produce:B_W1:0 + 1 ship:R_W1_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:W1:RAW:0:0 + 1 produce:B_W1:0 eq 5. Source: balance/initial_stock/routes/recipes.
- c000004: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 + -1 ship:R_W1_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000005: 1 inventory:M0:RAW:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000006: 1 serve:M0:P0:0:0 eq 4. Source: demands.
- c000007: 1 inventory:W0:P0:0:0 + 1 inventory:W0:RAW:0:0 le 2. Source: locations/storage_capacity.
- c000008: 1 ship:R_W0_M0_standard:P0:0:0 le 2. Source: locations/throughput_capacity.
- c000009: 1 inventory:W1:P0:0:0 + 1 inventory:W1:RAW:0:0 le 3. Source: locations/storage_capacity.
- c000010: 1 ship:R_W1_M0_standard:P0:0:0 le 6. Source: locations/throughput_capacity.
- c000011: 1 inventory:M0:P0:0:0 + 1 inventory:M0:RAW:0:0 le 3. Source: locations/storage_capacity.
- c000012: 0 le 4. Source: locations/throughput_capacity.
- c000013: 1 ship:R_W0_M0_standard:P0:0:0 le 3. Source: routes/capacity.
- c000014: 1 ship:R_W1_M0_standard:P0:0:0 le 8. Source: routes/capacity.
