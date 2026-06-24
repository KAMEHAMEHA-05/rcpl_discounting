# BOX RATE CALCULATION TOOL

## Overview

This tool calculates final product rates by combining information from three Excel files:

1. CustomSizeData.xlsx
2. ProductRate.xlsx
3. ProductWiseUps.xlsx

The program generates:

* FinalResult.xlsx (calculated rates)
* Error.xlsx (products that could not be processed correctly)

## How the Calculation Works

Step 1: Find the Product's Reference Size
Using ProductWiseUps.xlsx, the program finds:

* Ref. Size for Rate
* Ups value

based on the product's Media Type and Product Size.

Step 2: Find the Base Rate
Using ProductRate.xlsx, the program searches for the same product code with the reference size obtained in Step 1.

This reference-size product acts as the base product for rate calculation.

Step 3: Calculate Total Rate

Total Rate = Reference Size Rate × Ups

Step 4: Find Packaging Cost and Discount
Using CustomSizeData.xlsx, the program looks up:

* Package Cost per Up
* Basic Discount %

based on:

* Media Type
* Product Quantity
* Reference Size

and the matching Ups range.

Step 5: Calculate Final Rate

Total Package Cost = Package Cost per Up × Ups

Interim Rate = Total Rate − Total Package Cost

Discount Amount = Interim Rate × Discount %

Final Rate = Interim Rate − Discount Amount

The final result is written to FinalResult.xlsx.

## Error Handling

Products are written to Error.xlsx in the following cases:

Error Flag = N
Reference-size product could not be found in ProductRate.xlsx.

Error Flag = 0
Reference-size product was found, but its rate is 0.

## Input Files

CustomSizeData.xlsx
Contains packaging cost and discount information for different Ups ranges.

ProductRate.xlsx
Contains product details and base rates.

ProductWiseUps.xlsx
Contains mapping between Product Size and:
- Ref. Size for Rate
- Ups

## Output Files

FinalResult.xlsx
Successfully calculated product rates.

Error.xlsx
Products that could not be processed.

## Usage

Place the following files in the same folder as the executable:

```
CustomSizeData.xlsx
ProductRate.xlsx
ProductWiseUps.xlsx
rcpl_discounting_windows.exe
```

Run:

```
rcpl_discounting_windows.exe
```

The program will automatically read the input files and generate:

```
FinalResult.xlsx
Error.xlsx
```

in the same folder.

Note:
If FinalResult.xlsx or Error.xlsx already exist, they may be overwritten with the latest results.
