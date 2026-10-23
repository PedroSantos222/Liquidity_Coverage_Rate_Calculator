# Liquidity Stress Testing Model

## Overview

A small Python project that estimates stressed liquidity outflows and a simplified Liquidity Coverage Ratio (LCR)-style measure under different funding scenarios.

The model aggregates inflows and outflows by transaction, applies desk-specific stress factors, limits recognized inflows to 75% of total outflows, and calculates the resulting liquidity ratio.

## Features

- Multiple funding stress scenarios: base, funding stress, and severe.
- Input validation for transaction data, stress factors, and HQLA.
- Duplicate transaction ID detection.
- Aggregation of stressed outflows by desk.
- A basic automated test for the base scenario.

## Methodology

For each transaction, the amount is multiplied by its desk's scenario stress factor.

### 1. Recognized inflows

Recognized inflows are capped at 75% of total outflows:

$$
\text{Recognized Inflows}
=
\min\left(
\text{Total Inflows},
0.75 \times \text{Total Outflows}
\right)
$$

### 2. Net outflows

$$
\text{Net Outflows}
=
\text{Total Outflows}
-
\text{Recognized Inflows}
$$

### 3. Simplified LCR-style ratio

$$
\text{LCR-style Ratio}
=
\frac{\text{HQLA}}{\text{Net Outflows}}
\times 100\%
$$

Here, HQLA stands for *High-Quality Liquid Assets*. All monetary amounts are expressed in millions.

## Limitations

This is an educational, illustrative model, not a complete regulatory LCR implementation. It assumes the supplied HQLA amount is eligible and does not implement all regulatory rules, including asset haircuts, HQLA composition and caps, detailed regulatory inflow/outflow rates, and the full 30-day calculation perimeter.

The stress factors are illustrative assumptions, not calibrated estimates.
