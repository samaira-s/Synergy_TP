# Data Cleaning Report

## 1. Duplicates
Removed duplicate row for S005 (Rohan) which appeared twice.

## 2. Domain Standardization
Mapped all variations to: ML, Web, Electronics, Mechanical.

## 3. Attendance
Removed % signs. Set -10 and 105% to None (invalid). Filled with median.

## 4. Score
Converted word 'nine' to 9. Missing values filled with median.

## 5. Study Hours
Converted word 'two' to 2. Missing values filled with median.

## 6. Height
Converted all values to cm. 1.62 m became 162.0 cm.

## 7. Weight
Removed kg units and converted to float.

## 8. Submitted
Mapped Y/Yes/N/No to consistent yes/no values.

## 9. Missing Values
Numeric columns filled with median. Submitted filled with 'no'.

