# DAX Measures — India CPI & Inflation Analysis Dashboard

This document contains the DAX measures used in the project.

**Assumed table name:** `Table1`

> If your Power BI table has a different name, replace `Table1` with your actual table name.

---

## 1. Latest Combined CPI

Returns the Combined CPI for the latest month available.

```DAX
Latest Combined CPI =
CALCULATE(
    AVERAGE(Table1[combined_cpi]),
    LASTDATE(Table1[month])
)
```

**Expected result:** 107.94 for July 2026.

---

## 2. Average Combined CPI

Calculates the average Combined CPI across the available observations.

```DAX
Average Combined CPI =
AVERAGE(Table1[combined_cpi])
```

---

## 3. Latest Combined Inflation

Returns Combined inflation for the latest available month.

```DAX
Latest Combined Inflation =
CALCULATE(
    AVERAGE(Table1[combined_inflation]),
    LASTDATE(Table1[month])
)
```

**Expected result:** 4.45% for July 2026.

---

## 4. CPI Growth %

Calculates percentage growth between the first and latest Combined CPI observations.

```DAX
CPI Growth % =
VAR FirstCPI =
    CALCULATE(
        AVERAGE(Table1[combined_cpi]),
        FIRSTDATE(Table1[month])
    )
VAR LastCPI =
    CALCULATE(
        AVERAGE(Table1[combined_cpi]),
        LASTDATE(Table1[month])
    )
RETURN
    DIVIDE(LastCPI - FirstCPI, FirstCPI) * 100
```

**Expected result:** approximately 6.17%.

---

## 5. Maximum Monthly CPI Increase

Finds the largest positive month-over-month Combined CPI percentage change.

```DAX
Maximum Monthly CPI Increase =
MAX(Table1[Combined_CPI_MoM_Pct])
```

**Expected result:** 1.03%, occurring in June 2026.

---

## 6. Minimum Monthly CPI Change

Finds the smallest month-over-month Combined CPI percentage change.

```DAX
Minimum Monthly CPI Change =
MIN(Table1[Combined_CPI_MoM_Pct])
```

**Expected result:** approximately -0.34%, occurring in February 2025.

---

## 7. Latest Rural–Urban Inflation Gap

Calculates the rural minus urban inflation rate for the latest available month.

```DAX
Latest Rural Urban Inflation Gap =
CALCULATE(
    AVERAGE(Table1[rural_inflation]),
    LASTDATE(Table1[month])
)
-
CALCULATE(
    AVERAGE(Table1[urban_inflation]),
    LASTDATE(Table1[month])
)
```

**Expected result:** 0.88 percentage points for July 2026.

---

## 8. CPI Increase in Points

Calculates the absolute Combined CPI increase between the first and latest observations.

```DAX
CPI Increase in Points =
CALCULATE(
    AVERAGE(Table1[combined_cpi]),
    LASTDATE(Table1[month])
)
-
CALCULATE(
    AVERAGE(Table1[combined_cpi]),
    FIRSTDATE(Table1[month])
)
```

**Expected result:** 6.27 points.

Calculation:

```text
107.94 - 101.67 = 6.27
```

This is an index-point change, not a percentage change.

---

# Calculated Columns

These are calculated columns rather than measures.

## 9. Rural–Urban CPI Gap

```text
Rural CPI - Urban CPI
```

Interpretation:

- Positive → rural CPI is higher
- Negative → urban CPI is higher
- Zero → equal CPI

## 10. Combined CPI Month-over-Month Change

```text
Current Combined CPI - Previous Month Combined CPI
```

Measures the absolute monthly CPI movement.

## 11. Combined CPI Month-over-Month Percentage

```text
(Current Combined CPI - Previous Combined CPI)
/ Previous Combined CPI * 100
```

Expresses the monthly CPI movement as a percentage.

---

# DAX Concepts Used

## `CALCULATE()`

Changes the filter context under which an expression is evaluated.

## `AVERAGE()`

Returns the arithmetic mean of a numeric column.

## `MAX()`

Returns the largest value.

## `MIN()`

Returns the smallest value.

## `FIRSTDATE()`

Returns the first date in the current filter context.

## `LASTDATE()`

Returns the last date in the current filter context.

## `DIVIDE()`

Performs division with safer handling of divide-by-zero situations.

## `VAR`

Creates reusable variables that make complex DAX easier to read and maintain.

---

# Measure vs Calculated Column

### Calculated Column

Calculated row by row and stored in the model.

Used here for:
- Rural–Urban CPI Gap
- Combined CPI MoM Change
- Combined CPI MoM %

### Measure

Calculated dynamically based on filter context.

Used here for:
- Latest CPI
- Average CPI
- Latest inflation
- CPI growth
- Maximum monthly increase
- Minimum monthly change
- Latest rural–urban inflation gap

---

# Validation Values

Use these values to check the Power BI calculations:

| Metric | Expected |
|---|---:|
| First Combined CPI | 101.67 |
| Latest Combined CPI | 107.94 |
| CPI Increase | 6.27 points |
| CPI Growth | ~6.17% |
| Latest Combined Inflation | 4.45% |
| Highest Monthly CPI Increase | 1.03% |
| Lowest Monthly CPI Change | -0.34% |
| Latest Rural Inflation | 4.84% |
| Latest Urban Inflation | 3.96% |
| Latest Rural–Urban Inflation Gap | 0.88 percentage points |

---

# Important Notes

1. The project contains 19 monthly observations from January 2025 through July 2026.
2. Inflation values are blank for the provided 2025 observations and were not converted to zero.
3. July 2026 values are provisional.
4. The `month` field should be correctly recognized as a date/date-compatible field for `FIRSTDATE()` and `LASTDATE()` to behave as intended.
5. For a larger production Power BI model, create a dedicated Date table and establish a relationship to the data table before implementing advanced time-intelligence calculations.
