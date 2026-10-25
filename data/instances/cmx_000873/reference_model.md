# Bounded integer reference model

Minimize 0 + 2 dispose:M0:P0:0:0 + 2 dispose:M0:P0:0:1 + 2 dispose:M0:P0:1:0 + 2 dispose:M0:P0:1:1 + 2 dispose:W0:P0:0:0 + 2 dispose:W0:P0:0:1 + 2 dispose:W0:P0:1:0 + 2 dispose:W0:P0:1:1 + 2 dispose:W1:P0:0:0 + 2 dispose:W1:P0:0:1 + 2 dispose:W1:P0:1:0 + 2 dispose:W1:P0:1:1 + 3 ship:R_W0_M0_standard:P0:0:0 + 3 ship:R_W0_M0_standard:P0:0:1 + 3 ship:R_W0_M0_standard:P0:1:0 + 3 ship:R_W0_M0_standard:P0:1:1 + 8 ship:R_W1_M0_standard:P0:0:0 + 8 ship:R_W1_M0_standard:P0:0:1 + 8 ship:R_W1_M0_standard:P0:1:0 + 8 ship:R_W1_M0_standard:P0:1:1

## Variables

- `dispose:M0:P0:0:0`: integer in [0, 6], item.
- `dispose:M0:P0:0:1`: integer in [0, 6], item.
- `dispose:M0:P0:1:0`: integer in [0, 6], item.
- `dispose:M0:P0:1:1`: integer in [0, 6], item.
- `dispose:W0:P0:0:0`: integer in [0, 6], item.
- `dispose:W0:P0:0:1`: integer in [0, 6], item.
- `dispose:W0:P0:1:0`: integer in [0, 6], item.
- `dispose:W0:P0:1:1`: integer in [0, 6], item.
- `dispose:W1:P0:0:0`: integer in [0, 6], item.
- `dispose:W1:P0:0:1`: integer in [0, 6], item.
- `dispose:W1:P0:1:0`: integer in [0, 6], item.
- `dispose:W1:P0:1:1`: integer in [0, 6], item.
- `inventory:M0:P0:0:0`: integer in [0, 6], item.
- `inventory:M0:P0:0:1`: integer in [0, 0], item.
- `inventory:M0:P0:1:0`: integer in [0, 6], item.
- `inventory:M0:P0:1:1`: integer in [0, 0], item.
- `inventory:W0:P0:0:0`: integer in [0, 6], item.
- `inventory:W0:P0:0:1`: integer in [0, 0], item.
- `inventory:W0:P0:1:0`: integer in [0, 6], item.
- `inventory:W0:P0:1:1`: integer in [0, 0], item.
- `inventory:W1:P0:0:0`: integer in [0, 6], item.
- `inventory:W1:P0:0:1`: integer in [0, 0], item.
- `inventory:W1:P0:1:0`: integer in [0, 6], item.
- `inventory:W1:P0:1:1`: integer in [0, 0], item.
- `serve:M0:P0:1:0`: integer in [0, 2], item.
- `serve:M0:P0:1:1`: integer in [0, 2], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 6], item.
- `ship:R_W0_M0_standard:P0:0:1`: integer in [0, 6], item.
- `ship:R_W0_M0_standard:P0:1:0`: integer in [0, 6], item.
- `ship:R_W0_M0_standard:P0:1:1`: integer in [0, 6], item.
- `ship:R_W1_M0_standard:P0:0:0`: integer in [0, 2], item.
- `ship:R_W1_M0_standard:P0:0:1`: integer in [0, 2], item.
- `ship:R_W1_M0_standard:P0:1:0`: integer in [0, 2], item.
- `ship:R_W1_M0_standard:P0:1:1`: integer in [0, 2], item.

## Hard constraints

- c000000: 1 dispose:W0:P0:0:0 + 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 eq 3. Source: balance/initial_stock/routes/recipes.
- c000001: 1 dispose:W0:P0:0:1 + 1 inventory:W0:P0:0:1 + 1 ship:R_W0_M0_standard:P0:0:1 eq 0. Source: balance/initial_stock/routes/recipes.
- c000002: 1 dispose:W0:P0:1:0 + 1 inventory:W0:P0:1:0 + 1 ship:R_W0_M0_standard:P0:1:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000003: 1 dispose:W0:P0:1:1 + -1 inventory:W0:P0:0:0 + 1 inventory:W0:P0:1:1 + 1 ship:R_W0_M0_standard:P0:1:1 eq 0. Source: balance/initial_stock/routes/recipes.
- c000004: 1 dispose:W1:P0:0:0 + 1 inventory:W1:P0:0:0 + 1 ship:R_W1_M0_standard:P0:0:0 eq 3. Source: balance/initial_stock/routes/recipes.
- c000005: 1 dispose:W1:P0:0:1 + 1 inventory:W1:P0:0:1 + 1 ship:R_W1_M0_standard:P0:0:1 eq 0. Source: balance/initial_stock/routes/recipes.
- c000006: 1 dispose:W1:P0:1:0 + 1 inventory:W1:P0:1:0 + 1 ship:R_W1_M0_standard:P0:1:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000007: 1 dispose:W1:P0:1:1 + -1 inventory:W1:P0:0:0 + 1 inventory:W1:P0:1:1 + 1 ship:R_W1_M0_standard:P0:1:1 eq 0. Source: balance/initial_stock/routes/recipes.
- c000008: 1 dispose:M0:P0:0:0 + 1 inventory:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 + -1 ship:R_W1_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000009: 1 dispose:M0:P0:0:1 + 1 inventory:M0:P0:0:1 + -1 ship:R_W0_M0_standard:P0:0:1 + -1 ship:R_W1_M0_standard:P0:0:1 eq 0. Source: balance/initial_stock/routes/recipes.
- c000010: 1 dispose:M0:P0:1:0 + 1 inventory:M0:P0:1:0 + 1 serve:M0:P0:1:0 + -1 ship:R_W0_M0_standard:P0:1:0 + -1 ship:R_W1_M0_standard:P0:1:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000011: 1 dispose:M0:P0:1:1 + -1 inventory:M0:P0:0:0 + 1 inventory:M0:P0:1:1 + 1 serve:M0:P0:1:1 + -1 ship:R_W0_M0_standard:P0:1:1 + -1 ship:R_W1_M0_standard:P0:1:1 eq 0. Source: balance/initial_stock/routes/recipes.
- c000012: 1 serve:M0:P0:1:0 + 1 serve:M0:P0:1:1 eq 2. Source: demands.
- c000013: 1 inventory:W0:P0:0:0 + 1 inventory:W0:P0:0:1 le 6. Source: locations/storage_capacity.
- c000014: 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:1 le 1. Source: locations/throughput_capacity.
- c000015: 1 inventory:W0:P0:1:0 + 1 inventory:W0:P0:1:1 le 6. Source: locations/storage_capacity.
- c000016: 1 ship:R_W0_M0_standard:P0:1:0 + 1 ship:R_W0_M0_standard:P0:1:1 le 1. Source: locations/throughput_capacity.
- c000017: 1 inventory:W1:P0:0:0 + 1 inventory:W1:P0:0:1 le 3. Source: locations/storage_capacity.
- c000018: 1 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M0_standard:P0:0:1 le 4. Source: locations/throughput_capacity.
- c000019: 1 inventory:W1:P0:1:0 + 1 inventory:W1:P0:1:1 le 3. Source: locations/storage_capacity.
- c000020: 1 ship:R_W1_M0_standard:P0:1:0 + 1 ship:R_W1_M0_standard:P0:1:1 le 4. Source: locations/throughput_capacity.
- c000021: 1 inventory:M0:P0:0:0 + 1 inventory:M0:P0:0:1 le 0. Source: locations/storage_capacity.
- c000022: 0 le 1. Source: locations/throughput_capacity.
- c000023: 1 inventory:M0:P0:1:0 + 1 inventory:M0:P0:1:1 le 0. Source: locations/storage_capacity.
- c000024: 0 le 1. Source: locations/throughput_capacity.
- c000025: 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:1 le 6. Source: routes/capacity.
- c000026: 1 ship:R_W0_M0_standard:P0:1:0 + 1 ship:R_W0_M0_standard:P0:1:1 le 6. Source: routes/capacity.
- c000027: 1 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M0_standard:P0:0:1 le 2. Source: routes/capacity.
- c000028: 1 ship:R_W1_M0_standard:P0:1:0 + 1 ship:R_W1_M0_standard:P0:1:1 le 2. Source: routes/capacity.
