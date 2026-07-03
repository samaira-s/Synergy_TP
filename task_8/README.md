# Task 8 — Descriptive Statistics and Technical Interpretation

## 1. Task Title
Descriptive Statistics and Technical Interpretation (Week 2, Day 2)

## 2. Objective
Go beyond just computing descriptive statistics to interpreting them correctly:
understanding center vs. spread, when the mean misleads, how sample size affects
trust in a statistic, how to judge whether an outlier is an error or a real
signal, how to pick the right plot for a given question, the difference between
correlation and causation, and why measurements can't be compared or averaged
across domains/units without care. No code — this is a written technical note.

## 3. Learning Resources Used
- Khan Academy — Statistics and Probability: https://www.khanacademy.org/math/statistics-probability
- OpenIntro Statistics: https://www.openintro.org/book/os/
- NIST Engineering Statistics Handbook — Exploratory Data Analysis: https://www.itl.nist.gov/div898/handbook/eda/eda.htm

## 4. Final Submitted Report Path
`Task8_SamairaSingh.pdf` (source: `Day2_SamairaSingh.docx`)

## 5. What Was Learned
- Descriptive statistics are a fast first check (seconds, not code-heavy) run
  before cleaning, visualization, feature engineering, or modelling — they can
  catch obvious problems (e.g. an "age" column with max=150) before any real
  work is done on a column that turns out to be broken.
- Stats alone have a blind spot: two very different underlying behaviours (a
  steady noisy signal vs. one switching between two states) can produce the
  *exact same* mean and standard deviation. Std tells you *how much* spread,
  not *what kind* of spread — that's what a histogram is for.
- Median and IQR are more robust to outliers/skew than mean and range, because
  they depend on position in sorted order rather than magnitude.
- A statistic from a very small sample (e.g. 5 readings) is far less trustworthy
  than the same statistic from hundreds of readings — one unusual point can
  dominate a small sample.
- Not every outlier is an error — some are the actual signal worth
  investigating (e.g. a rare real event). Deleting one without checking risks
  losing the most important data point.
- Choosing the right plot matters: histogram (single variable's distribution),
  box plot (spread/outliers, especially across groups), bar chart (numeric
  value across categories), scatter plot (relationship between two numeric
  variables), line plot (a variable over time/sequence).
- Correlation is not causation — a third, confounding variable can drive both
  quantities independently and create an apparent relationship that isn't
  cause-and-effect.
- Values are only comparable if they share domain, measurement type, unit, and
  experimental condition — mixing these (e.g. averaging pH with voltage, or
  MPa with psi) produces a number that is arithmetically valid but physically
  meaningless.

## Folder Structure
```
task_8/
├── README.md
├── report/
    ├── Task8_SamairaSingh.docx  # source
    ├── Task8_SamairaSingh.pdf    # final submission
        
```
