# Bounded integer reference model

Minimize 0 + 4 ship:R_W0_M0_rail:P0:0:0 + 1 ship:R_W1_M0_rail:P0:0:0 + 1 ship:R_W1_M0_road:P0:0:0 + 8 ship:R_W2_M0_road:P0:0:0 + 11 trucks:R_W0_M0_rail:0 + 10 trucks:R_W1_M0_rail:0 + 8 trucks:R_W1_M0_road:0 + 8 trucks:R_W2_M0_road:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 7], item.
- `inventory:W0:P0:0:0`: integer in [0, 7], item.
- `inventory:W1:P0:0:0`: integer in [0, 7], item.
- `inventory:W2:P0:0:0`: integer in [0, 7], item.
- `serve:M0:P0:0:0`: integer in [0, 5], item.
- `ship:R_W0_M0_rail:P0:0:0`: integer in [0, 4], item.
- `ship:R_W1_M0_rail:P0:0:0`: integer in [0, 3], item.
- `ship:R_W1_M0_road:P0:0:0`: integer in [0, 3], item.
- `ship:R_W2_M0_road:P0:0:0`: integer in [0, 5], item.
- `trucks:R_W0_M0_rail:0`: integer in [0, 2], truck.
- `trucks:R_W1_M0_rail:0`: integer in [0, 1], truck.
- `trucks:R_W1_M0_road:0`: integer in [0, 2], truck.
- `trucks:R_W2_M0_road:0`: integer in [0, 1], truck.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_rail:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 + 1 ship:R_W1_M0_rail:P0:0:0 + 1 ship:R_W1_M0_road:P0:0:0 eq 1. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W2:P0:0:0 + 1 ship:R_W2_M0_road:P0:0:0 eq 6. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_rail:P0:0:0 + -1 ship:R_W1_M0_rail:P0:0:0 + -1 ship:R_W1_M0_road:P0:0:0 + -1 ship:R_W2_M0_road:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000004: 1 serve:M0:P0:0:0 eq 5. Source: demands.
- c000005: 1 inventory:W0:P0:0:0 le 2. Source: locations/storage_capacity.
- c000006: 1 ship:R_W0_M0_rail:P0:0:0 le 4. Source: locations/throughput_capacity.
- c000007: 1 inventory:W1:P0:0:0 le 1. Source: locations/storage_capacity.
- c000008: 1 ship:R_W1_M0_rail:P0:0:0 + 1 ship:R_W1_M0_road:P0:0:0 le 1. Source: locations/throughput_capacity.
- c000009: 1 inventory:W2:P0:0:0 le 1. Source: locations/storage_capacity.
- c000010: 1 ship:R_W2_M0_road:P0:0:0 le 8. Source: locations/throughput_capacity.
- c000011: 1 inventory:M0:P0:0:0 le 2. Source: locations/storage_capacity.
- c000012: 0 le 4. Source: locations/throughput_capacity.
- c000013: 1 ship:R_W0_M0_rail:P0:0:0 le 4. Source: routes/capacity.
- c000014: 1 ship:R_W0_M0_rail:P0:0:0 + -2 trucks:R_W0_M0_rail:0 le 0. Source: routes/truck_capacity.
- c000015: 1 ship:R_W1_M0_rail:P0:0:0 le 3. Source: routes/capacity.
- c000016: 1 ship:R_W1_M0_rail:P0:0:0 + -5 trucks:R_W1_M0_rail:0 le 0. Source: routes/truck_capacity.
- c000017: 1 ship:R_W1_M0_road:P0:0:0 le 3. Source: routes/capacity.
- c000018: 1 ship:R_W1_M0_road:P0:0:0 + -2 trucks:R_W1_M0_road:0 le 0. Source: routes/truck_capacity.
- c000019: 1 ship:R_W2_M0_road:P0:0:0 le 5. Source: routes/capacity.
- c000020: 1 ship:R_W2_M0_road:P0:0:0 + -5 trucks:R_W2_M0_road:0 le 0. Source: routes/truck_capacity.
