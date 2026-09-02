# Change Set — Local variable clarity

## Acceptance criterion

No behavior change. Rename a local variable to make the calculation easier to read.

## Proposed diff

```diff
 def total_with_tax(subtotal, tax_rate):
-    x = subtotal * tax_rate
-    return subtotal + x
+    tax_amount = subtotal * tax_rate
+    return subtotal + tax_amount
```

## Test evidence

```text
$ pytest tests/test_totals.py
12 passed
```

Visible tests include zero subtotal, fractional rate and normal positive values.

## Repository convention

Local variables use descriptive snake_case names. No formatter, API, persistence or security boundary is affected.
