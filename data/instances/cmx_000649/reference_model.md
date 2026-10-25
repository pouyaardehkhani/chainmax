# Bounded integer reference model

Minimize 0 + 12 open:W0 + 14 open:W1 + 8 ship:R_W0_M0_standard:P0:0:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 4], item.
- `inventory:W0:P0:0:0`: integer in [0, 4], item.
- `inventory:W1:P0:0:0`: integer in [0, 4], item.
- `open:W0`: boolean in [0, 1], activation.
- `open:W1`: boolean in [0, 1], activation.
- `serve:M0:P0:0:0`: integer in [0, 4], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 4], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 eq 4. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000003: 1 serve:M0:P0:0:0 eq 4. Source: demands.
- c000004: 1 inventory:W0:P0:0:0 le 3. Source: locations/storage_capacity.
- c000005: 1 ship:R_W0_M0_standard:P0:0:0 le 4. Source: locations/throughput_capacity.
- c000006: -4 open:W0 + 1 ship:R_W0_M0_standard:P0:0:0 le 0. Source: locations/opening_cost.
- c000007: 1 inventory:W1:P0:0:0 le 3. Source: locations/storage_capacity.
- c000008: 0 le 0. Source: locations/throughput_capacity.
- c000009: 0 le 0. Source: locations/opening_cost.
- c000010: 1 inventory:M0:P0:0:0 le 0. Source: locations/storage_capacity.
- c000011: 0 le 3. Source: locations/throughput_capacity.
- c000012: 1 ship:R_W0_M0_standard:P0:0:0 le 4. Source: routes/capacity.
