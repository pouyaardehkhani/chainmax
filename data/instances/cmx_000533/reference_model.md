# Bounded integer reference model

Minimize 0 + 5 active:R_W0_M0_standard:0

## Variables

- `active:R_W0_M0_standard:0`: boolean in [0, 1], activation.
- `inventory:M0:P0:0:0`: integer in [0, 6], item.
- `inventory:W0:P0:0:0`: integer in [0, 6], item.
- `inventory:W1:P0:0:0`: integer in [0, 6], item.
- `serve:M0:P0:0:0`: integer in [0, 3], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 4], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 eq 3. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 eq 3. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000003: 1 serve:M0:P0:0:0 eq 3. Source: demands.
- c000004: 1 inventory:W0:P0:0:0 le 3. Source: locations/storage_capacity.
- c000005: 1 ship:R_W0_M0_standard:P0:0:0 le 4. Source: locations/throughput_capacity.
- c000006: 1 inventory:W1:P0:0:0 le 7. Source: locations/storage_capacity.
- c000007: 0 le 0. Source: locations/throughput_capacity.
- c000008: 1 inventory:M0:P0:0:0 le 2. Source: locations/storage_capacity.
- c000009: 0 le 2. Source: locations/throughput_capacity.
- c000010: 1 ship:R_W0_M0_standard:P0:0:0 le 4. Source: routes/capacity.
- c000011: -4 active:R_W0_M0_standard:0 + 1 ship:R_W0_M0_standard:P0:0:0 le 0. Source: routes/activation.
- c000012: -1 active:R_W0_M0_standard:0 + 1 ship:R_W0_M0_standard:P0:0:0 ge 0. Source: routes/minimum_lot.
