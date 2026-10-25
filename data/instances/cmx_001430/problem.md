Prepare an integer operating plan for minimum lots and sourcing rules. All available resources and required deliveries are specified below; choose the least-cost feasible plan.

Plan periods 0 through 0. Quantities are items, currency is cents, capacities use volume units, and time is in periods.

## Business rules

1. Choose nonnegative integer shipments, ending inventories, demand fulfillment by age, production batches, and truck counts; activation decisions are Boolean. All have the finite bounds in the reference decision-domain convention.
2. Meet every listed demand exactly at its node and period. No shortages, substitution, purchases, or routes beyond those listed are allowed. Unused stock may remain within storage limits; terminal stock is allowed with no salvage value.
3. Initial stock is available at the beginning of period 0. Within each period, arriving shipments and raw inputs are available before production, demand fulfillment, onward shipment, disposal, and ending-inventory measurement. Zero-lead routes form an acyclic network; goods may pass through its successive nodes within a period. Production outputs are immediately available; recipes consume only raw inputs.
4. A departure in period t with lead L arrives in t+L. Departures arriving outside the horizon are forbidden. Route capacity and truck capacity limit total dispatched volume per route per period. Product volume converts item quantities to volume units. Product lists specify mode eligibility.
5. Node throughput limits outgoing shipment volume per period. Node storage limits end-of-period stock volume shared across products and ages. Opening a warehouse is required for dispatch and charged once for the entire horizon; closed locations may retain initial stock.
6. Route activation is per dispatch period: it is one exactly when positive quantity is dispatched. Active routes require at least max(1, minimum_lot) items in total, summed across eligible products and ages. Fixed costs apply once per active route-period. A maximum supplier count limits active incoming routes at each market per period; in this corpus those routes have distinct suppliers. A dependency [A,B] means route A active implies route B active in the same period.
7. Truck costs supplement per-item shipping costs. Integer truck counts provide truck_capacity times trucks volume; max_trucks is the upper bound. No tours or return journeys are modeled.
8. For a shelf life S, usable ages are 0 through S-1. Initial ages are explicit. Storage and transit each advance age by elapsed periods. Arrival at age S is forbidden. Stock at age S-1 must be used, shipped with an admissible arrival, or disposed of before period end, including the terminal period. Disposal is available only for perishable products and charged per item. Nonperishable products use age 0 throughout.
9. A recipe's integer input quantities are consumed per batch; output_quantity items appear per batch. Recipe capacity is batches per period. Production is bounded and charged per batch.
10. Minimize the nonnegative integer total cost in cents: shipping per item, production per batch, holding per item of ending inventory in every period including the last, disposal per item, route activations, warehouse openings, truck counts, and the objective constant. Zero coefficients mean no charge.
11. A safe quantity bound for each inventory/disposal decision is the maximum of 1 and total initial items plus the sum of every recipe's capacity times output_quantity times number of periods. Shipment bounds are additionally capped by route volume capacity divided by product volume. Fulfillment-by-age bounds equal the listed demand. Expiring ending inventory has bound zero.

## Complete input tables

The following JSON tables are part of the problem statement. Identifiers denote entities; every numerical parameter uses the units specified above. Missing routes are unavailable. The narrative_template field only selects wording.

```json
{
  "demands": [
    {
      "node": "M0",
      "period": 0,
      "product": "P0",
      "quantity": 2
    }
  ],
  "family": "F08",
  "features": [
    "transport",
    "bounded_inventory",
    "exact_demand",
    "minimum_lots_and_sourcing"
  ],
  "initial_stock": [
    {
      "age": 0,
      "node": "W0",
      "product": "P0",
      "quantity": 3
    },
    {
      "age": 0,
      "node": "W1",
      "product": "P0",
      "quantity": 4
    }
  ],
  "locations": [
    {
      "id": "W0",
      "opening_cost": 0,
      "role": "warehouse",
      "storage_capacity": 4,
      "throughput_capacity": 0
    },
    {
      "id": "W1",
      "opening_cost": 0,
      "role": "warehouse",
      "storage_capacity": 2,
      "throughput_capacity": 4
    },
    {
      "id": "W2",
      "opening_cost": 0,
      "role": "warehouse",
      "storage_capacity": 0,
      "throughput_capacity": 0
    },
    {
      "id": "M0",
      "opening_cost": 0,
      "role": "market",
      "storage_capacity": 1,
      "throughput_capacity": 2
    }
  ],
  "narrative_template": 2,
  "objective_constant": 0,
  "periods": 1,
  "products": [
    {
      "disposal_cost": 0,
      "holding_cost": 0,
      "id": "P0",
      "shelf_life": null,
      "volume": 1
    }
  ],
  "recipes": [],
  "routes": [
    {
      "capacity": 6,
      "destination": "M0",
      "fixed_cost": 2,
      "id": "R_W0_M0_standard",
      "lead_time": 0,
      "max_trucks": 0,
      "minimum_lot": 2,
      "mode": "standard",
      "products": [
        "P0"
      ],
      "source": "W0",
      "truck_capacity": 0,
      "truck_cost": 0,
      "unit_cost": 2
    },
    {
      "capacity": 2,
      "destination": "M0",
      "fixed_cost": 17,
      "id": "R_W1_M0_standard",
      "lead_time": 0,
      "max_trucks": 0,
      "minimum_lot": 1,
      "mode": "standard",
      "products": [
        "P0"
      ],
      "source": "W1",
      "truck_capacity": 0,
      "truck_cost": 0,
      "unit_cost": 1
    }
  ],
  "schema_version": "1.0.0",
  "sourcing": {
    "dependencies": [],
    "max_active_suppliers": 1
  },
  "structural_level": "L2",
  "units": {
    "capacity": "volume_unit",
    "currency": "cent",
    "production": "batch",
    "quantity": "item",
    "time": "period",
    "truck": "truck"
  }
}
```
