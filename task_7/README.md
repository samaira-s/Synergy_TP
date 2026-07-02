# Task 7 — Day 1: Data Understanding and Measurement Basics

## 1. Task Title
Data Understanding and Measurement Basics

## 2. Objective
Build the theoretical foundation required for data analysis before moving into
pandas, feature creation, visualization, or machine learning — understanding
what a dataset represents, how measurements are structured, how variables
differ, and why domain context and units matter, using examples from
Biochemistry, Electronics, and Mechanical domains.

## 3. Learning Resources Used
- Khan Academy — Statistics and Probability: https://www.khanacademy.org/math/statistics-probability
- OpenIntro Statistics: https://www.openintro.org/book/os/
- NIST Engineering Statistics Handbook — Exploratory Data Analysis: https://www.itl.nist.gov/div898/handbook/eda/eda.htm

## 4. Final Submitted Report Path
`report/Task7_SamairaSingh.pdf` (source: `report/Task3_SamairaSingh.docx`)

## 5. What Was Learned
- A dataset value is only meaningful when tied to its variable name, unit, and
  experimental condition — not just a raw number.
- Observations (rows) and variables (columns) are easy to confuse but require
  different handling; categorical and numerical data need different summary
  treatment (counts/proportions vs. mean/median/std).
- Raw data must be sanitized (missing values, implausible readings) before it
  becomes trustworthy processed data.
- The mean alone can mislead when outliers or skew are present — median and a
  visual check (histogram/boxplot) matter too.
- Before analyzing data from another team, it's worth asking about instrument
  used, units, experimental conditions, and whether cleaning has already
  happened.

## Folder Structure
```
task_7/
├── README.md
└── report/
    ├── Task7_SamairaSingh.docx      # source
    └── Task7_SamairaSingh.pdf       # final submission
```
