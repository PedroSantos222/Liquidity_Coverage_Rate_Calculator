# Liquidity Stress Testing Model

## Overview

This project implements a simplified liquidity stress testing model in Python. It estimates stressed cash inflows and outflows under different funding scenarios and calculates an illustrative Liquidity Coverage Ratio (LCR)-style measure.

The goal is to demonstrate practical Python skills relevant to liquidity risk and financial risk analysis, including scenario analysis, data validation, aggregation, and automated testing.

## Features

- Three funding scenarios: base, funding stress, and severe.
- Desk-specific stress factors applied to individual transactions.
- Input validation for transaction data, stress factors, and High-Quality Liquid Assets (HQLA).
- Detection of missing fields and duplicate transaction IDs.
- Aggregation of stressed outflows by desk.
- An automated test of the base scenario.

## Methodology

### 1. Apply stress factors

Each transaction amount is multiplied by the stress factor associated with its desk.

**Stressed amount = Original amount × Desk stress factor**

### 2. Calculate recognized inflows

To reflect the simplified 75% inflow cap, recognized inflows are the smaller of total inflows and 75% of total outflows.

**Recognized inflows = min(Total inflows, 0.75 × Total outflows)**

### 3. Calculate net outflows

Recognized inflows are deducted from total outflows.

**Net outflows = Total outflows − Recognized inflows**

### 4. Calculate the LCR-style ratio

The model divides HQLA by net outflows and expresses the result as a percentage.

**LCR-style ratio (%) = (HQLA / Net outflows) × 100**

For example, if HQLA is 135 million and net outflows are 45 million, the resulting ratio is 300%.

All monetary amounts are expressed in millions.

## How to Run

Requires Python 3.

Run the script from a terminal:

```bash
python liquidity_model.py
```

Replace `liquidity_model.py` with the actual name of your Python file if it differs.

The script runs the base-scenario test and prints the results for each funding scenario.

## Limitations

This is an educational model inspired by the LCR framework, not a complete regulatory LCR implementation.

In particular, the model:

- Assumes the supplied HQLA amount is eligible and does not apply regulatory asset haircuts.
- Does not implement HQLA composition requirements or regulatory caps.
- Uses illustrative desk-specific stress factors rather than calibrated estimates.
- Does not apply detailed regulatory inflow and outflow rates.
- Does not model the complete regulatory 30-day liquidity calculation perimeter.

The results should therefore be interpreted as illustrative scenario analysis, not as a regulatory LCR calculation.

