# Bounded integer reference model

Minimize 0 + 12 ship:R_W0_M0_road:P0:0:0 + 9 ship:R_W1_M0_rail:P0:0:0 + 8 ship:R_W1_M0_road:P0:0:0 + 7 trucks:R_W0_M0_road:0 + 3 trucks:R_W1_M0_rail:0 + 6 trucks:R_W1_M0_road:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 5], item.
- `inventory:W0:P0:0:0`: integer in [0, 5], item.
- `inventory:W1:P0:0:0`: integer in [0, 5], item.
- `serve:M0:P0:0:0`: integer in [0, 4], item.
- `ship:R_W0_M0_road:P0:0:0`: integer in [0, 5], item.
- `ship:R_W1_M0_rail:P0:0:0`: integer in [0, 2], item.
- `ship:R_W1_M0_road:P0:0:0`: integer in [0, 5], item.
- `trucks:R_W0_M0_road:0`: integer in [0, 2], truck.
- `trucks:R_W1_M0_rail:0`: integer in [0, 1], truck.
- `trucks:R_W1_M0_road:0`: integer in [0, 2], truck.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_road:P0:0:0 eq 1. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 + 1 ship:R_W1_M0_rail:P0:0:0 + 1 ship:R_W1_M0_road:P0:0:0 eq 4. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_road:P0:0:0 + -1 ship:R_W1_M0_rail:P0:0:0 + -1 ship:R_W1_M0_road:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000003: 1 serve:M0:P0:0:0 eq 4. Source: demands.
- c000004: 1 inventory:W0:P0:0:0 le 3. Source: locations/storage_capacity.
- c000005: 1 ship:R_W0_M0_road:P0:0:0 le 3. Source: locations/throughput_capacity.
- c000006: 1 inventory:W1:P0:0:0 le 0. Source: locations/storage_capacity.
- c000007: 1 ship:R_W1_M0_rail:P0:0:0 + 1 ship:R_W1_M0_road:P0:0:0 le 5. Source: locations/throughput_capacity.
- c000008: 1 inventory:M0:P0:0:0 le 1. Source: locations/storage_capacity.
- c000009: 0 le 1. Source: locations/throughput_capacity.
- c000010: 1 ship:R_W0_M0_road:P0:0:0 le 5. Source: routes/capacity.
- c000011: 1 ship:R_W0_M0_road:P0:0:0 + -4 trucks:R_W0_M0_road:0 le 0. Source: routes/truck_capacity.
- c000012: 1 ship:R_W1_M0_rail:P0:0:0 le 2. Source: routes/capacity.
- c000013: 1 ship:R_W1_M0_rail:P0:0:0 + -2 trucks:R_W1_M0_rail:0 le 0. Source: routes/truck_capacity.
- c000014: 1 ship:R_W1_M0_road:P0:0:0 le 5. Source: routes/capacity.
- c000015: 1 ship:R_W1_M0_road:P0:0:0 + -3 trucks:R_W1_M0_road:0 le 0. Source: routes/truck_capacity.
