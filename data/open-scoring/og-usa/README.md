# NSRA: OG-USA dynamic analysis (round 2, November 2026)

We ran OG-USA, the open-source overlapping-generations model of the U.S. economy maintained by the Policy Simulation Library, on the NSRA as introduced (methodology v2026.5). **We ran it ourselves. It is not an independent score and not a CBO or JCT estimate.** Every input, script and result is in this folder so anyone can reproduce or challenge it. Corrections are welcome.

## Headline (central run)

| | Year 1 | Year 5 | Year 10 | Year 20 |
|---|---|---|---|---|
| GDP, % change | -1.55 | -1.41 | -1.17 | -0.62 |
| Wages, % change | -0.64 | -0.74 | -0.73 | -0.44 |
| Private investment, % change | -3.27 | -1.89 | -1.24 | +1.02 |
| Hours worked, % change | -0.92 | -0.67 | -0.44 | -0.18 |
| Federal debt, points of GDP | +1.6 | -3.4 | -10.2 | -25.6 |

The bill raises about 2.5% of GDP in revenue and returns about 1.0% as transfers; the rest reduces the deficit. In this model that shows up as lower private consumption and a smaller economy at first, and as much lower debt and higher investment later.

## Who gains and who pays (central run, Year 10)

Change in consumption per person by lifetime-income group (percentiles of lifetime earnings ability):

| Group | Consumption | Hours worked |
|---|---|---|
| 0-25 | +0.55% | -2.39% |
| 25-50 | -0.08% | -1.94% |
| 50-70 | -0.86% | -1.38% |
| 70-80 | -1.13% | -1.08% |
| 80-90 | -1.39% | -0.91% |
| 90-99 | -2.33% | +0.05% |
| 99-99.5 | -4.06% | +1.67% |
| 99.5-99.9 | -5.00% | +3.04% |
| 99.9-99.99 | -7.62% | +4.58% |
| top 0.01 | -11.67% | +3.87% |

Remaining-lifetime consumption by generation (discounted at 3%), all income groups combined:

| Cohort | Bottom 25% | 25–50% | 50–70% | 90–99% | Top 1% band (99–99.5) | All |
|---|---|---|---|---|---|---|
| age 65 in Year 1 | -0.94 | -1.27 | -1.45 | -2.61 | -4.52 | -1.95 |
| age 45 in Year 1 | -0.34 | -0.96 | -1.47 | -3.51 | -6.02 | -2.63 |
| age 25 in Year 1 | +0.53 | -0.21 | -0.99 | -2.96 | -5.37 | -2.01 |
| turns 21 in Year 10 | +0.43 | -0.18 | -1.09 | -3.19 | -5.69 | -2.13 |
| turns 21 in Year 20 | +0.29 | -0.40 | -1.29 | -3.44 | -6.07 | -2.36 |

**How to read this.** The model counts a household as better off only through its own consumption and leisure. It gives no value to health coverage beyond its cost, to infrastructure or research, or to lower federal debt except through the economy. Deficit reduction therefore always reads as lost consumption today. The deficit-neutral test below shows how much of the result comes from the deficit reduction itself.

## Sensitivity

| Run | GDP Y1 | GDP Y10 | GDP Y20 | GDP Y30 | Debt Y10 (pts) | Debt Y20 (pts) | Bottom 25% cons. Y10 | 50–70% cons. Y10 |
|---|---|---|---|---|---|---|---|---|
| **Central** | -1.55 | -1.17 | -0.62 | -1.22 | -10.2 | -25.6 | +0.55 | -0.86 |
| Central, with the net savings returned to every adult as an equal payment (deficit-neutral test) | -2.19 | -2.35 | -2.46 | -2.44 | +2.6 | +2.9 | +3.24 | +0.49 |
| **Reference mapping**: enforcement, royalties and the 28% limit treated as consumption taxes | -1.38 | -0.97 | -0.40 | -1.02 | -10.8 | -26.7 | +0.46 | -0.95 |
| Reference, debt rule starts Year 10 | -1.34 | -0.85 | -1.64 | -1.52 | -11.0 | +7.6 | +0.38 | -1.04 |
| Reference, debt rule starts Year 30 | -1.38 | -0.99 | -0.47 | -0.33 | -10.8 | -26.6 | +0.46 | -0.94 |
| Reference, labor supply less responsive (Frisch 0.27) | -1.19 | -0.90 | -0.41 | -1.01 | -10.5 | -25.5 | +1.09 | -0.67 |
| Reference, labor supply more responsive (Frisch 0.60) | -1.61 | -1.05 | -0.39 | -1.04 | -11.1 | -27.8 | -0.17 | -1.10 |
| Reference, public capital raises productivity (elasticity 0.05) | -1.43 | -0.87 | -0.17 | -0.67 | -11.1 | -27.4 | +0.69 | -0.80 |

The calibration and closure tests were run on the reference mapping; compare each with the reference row.

The dip after Year 20 in most runs comes from the model's debt rule: from the start year, government purchases and transfers adjust to steer debt back to its long-run target, so the bill's savings are spent on purchases the model does not value. Moving the start to Year 30 removes most of it.

## Calibration

| Setting | Value | Why |
|---|---|---|
| Tax functions | DEP (ratio of polynomials), estimated on Tax-Calculator 6.9 output for 2028 | The OG-USA default (HSV) has two parameters and captured only about 60% of the static revenue of the bill's top-end changes; DEP reproduces the Tax-Calculator change (about 6.7% of income and payroll tax). Held constant after 2028. |
| Frisch elasticity of labor supply | 0.40 (0.27 and 0.60 tested) | Middle of the micro-evidence range; 0.27 is close to the values CBO uses. |
| Risk aversion (CRRA) | 1.5 | OG-USA default; standard in the literature. |
| Capital share | 0.38 | OG-USA default. |
| Public capital in production | off (0.05 tested) | Conservative; infrastructure counted as spending only. |
| Foreign purchases of new debt / capital | 40% / 50% | OG-USA defaults; partly open economy. |
| Debt rule | starts Year 20 (10 and 30 tested) | OG-USA default; see Sensitivity. |
| Baseline | OG-USA 0.6.2 defaults, current law including P.L. 119-21 | Not re-targeted to CBO's February 2026 baseline. |

## How each provision enters the model

| Provision | Model input |
|---|---|
| Secs. 2408, 2420(a)-(c); paid-leave contribution (Title XXXVIII) | Re-estimated individual and payroll tax functions (Tax-Calculator 6.9, `iit_reform.json`) |
| Corporate rate 25% (Sec. 2409(b)); Pillar Two, buyback excise, excess-profits assessment, acquisition-debt cap, carried interest, export-income deduction repeal; IRS enforcement; federal royalties | Effective corporate rate, calibrated to the model's own corporate base (about 30% rising to 31%) |
| LIFO, advertising and fossil-fuel cost-recovery changes | Lower tax depreciation rate (0.0009 a year) |
| Carbon fee (Sec. 2410, with the Sec. 3410(f) increase) and NIMA | Consumption tax |
| Financial transaction tax, carryover basis, FTA, 28% limit on tax preferences | Tax on wealth, falling mainly on high-wealth households |
| Basic Minimum Plan, student loans, wage credit, TANF, housing, child accounts, veterans, Social Security protections, energy credits, child care, paid-leave benefits | Transfers aimed at the ages and income groups each program reaches, phased in on the Schedule E timetable |
| Medicare integrity and drug savings, improper payments, crop insurance, fraud recovery | Lower transfers, in proportion to existing transfers in the affected groups |
| Sec. 3410(b) Social Security solvency | Lower earnings-linked benefits from Year 8, phased over 40 years |
| Infrastructure, science, digital government, IRS investment, rural health; appropriations caps | Government purchases (caps phased over 10 years) |

## What this run does not do

- It has not been reviewed by anyone outside the project.
- Transfers are lump-sum; the model cannot represent the phase-outs that reduce work disincentives, so the drop in hours among lower-income households is likely overstated.
- Health effects, crime, education and other non-market outcomes are outside the model.
- The household groups are lifetime-earnings groups, not annual income brackets.

## Files

`run_nsra2.py` (all runs), `tf_dep.py` (tax functions), `analyze2.py` (results), `fidelity.py` (tax-function check), `iit_reform.json`, and `results2_DEP_<run>.json` for each run. Earlier first-round files (`run_nsra.py`, `results_*.json`) are kept for the record; their GDP figures are superseded because the first round collected only part of the bill's taxes.
