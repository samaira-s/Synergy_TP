# Replicate Analysis

## Which replicate group is most stable?
**Electronics / low_load (input_value=10.0 ohm)** — lowest CV (0.0051).

## Which replicate group is most noisy?
**Mechanical / high_load (input_value=150.0 N)** — highest CV (0.1005), flagged **moderate**.

## Which group has the widest confidence interval?
**Mechanical / high_load (input_value=150.0 N)**, width = 0.9405.

## Which group has the highest coefficient of variation?
Same as most noisy: **Mechanical / high_load (input_value=150.0 N)**.

## Why is mean alone not enough for judging reliability?
Mean shows the center but nothing about spread — two groups can share a mean while one is tightly clustered and one is scattered. Only std/SE/CI/CV reveal that difference.

## Why does replicate count affect confidence interval width?
SE = std / sqrt(n). Larger n shrinks SE, narrowing the CI, giving a more precise estimate of the mean.

## Which readings should be investigated before ML use?
The **Mechanical / high_load (input_value=150.0 N)** group — specifically its reading furthest from its replicate peers.
