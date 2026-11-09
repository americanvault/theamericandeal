# NSRA: OG-USA dynamic analysis (round 2, November 2026)

We ran OG-USA, the open-source overlapping-generations model of the U.S. economy maintained by the Policy Simulation Library, on the NSRA as written (methodology v2026.6, which adds the middle-class tax relief of Sec. 2421, keeps the 21% corporate rate, withdraws the infrastructure fee and extends household energy credits to 400% of poverty). **We ran it ourselves. It is not an independent score and not a CBO or JCT estimate.** Every input, script and result is in this folder so anyone can reproduce or challenge it. Corrections are welcome.

> This run was made before methodology v2026.7, which moved the rewilding and regional food-system programs to annual appropriations and withdrew the Phase 2 wage-floor credit, about $50 billion a year less mandatory spending. With that change, debt would fall slightly faster than shown here.

## Headline (central run)

| | Year 1 | Year 5 | Year 10 | Year 20 |
|---|---|---|---|---|
| GDP, % change | -1.90 | -1.77 | -1.48 | -0.98 |
| Wages, % change | -0.29 | -0.39 | -0.35 | -0.07 |
| Private investment, % change | -4.50 | -3.16 | -2.78 | -1.56 |
| Hours worked, % change | -1.62 | -1.39 | -1.14 | -0.91 |
| Federal debt, points of GDP | +2.0 | -0.5 | -4.0 | -13.1 |

The bill raises about 2.3% of GDP in revenue and returns about 1.8% as transfers, including the middle-class tax relief; the rest reduces the deficit. Households in roughly the bottom 70% of lifetime income consume more from Year 1. The economy is smaller at first and debt falls more slowly than in the v2026.5 bill, because less of the revenue goes to deficit reduction (see Sensitivity).


## Update: current bill (v2026.11, run "fullC", November 9, 2026)

Same model and accounting as "fullB", with Titles III, XXVII, XXXI, XXXII, XXXIII and XXXVII and Sec. 3408 back in the bill: science funding ($30B a year) and the Strategic Compute Node ($7.7B) enter as public investment; the global health fund ($8B), the Press Freedom Monitor and the one-time dollar-security funds ($2.5B in Year 1) enter as government purchases with no domestic productivity effect.

| | Year 1 | Year 5 | Year 10 | Year 20 |
|---|---|---|---|---|
| GDP, % change | -1.92 | -1.89 | -1.70 | -1.36 |
| Private investment, % change | -4.78 | -3.40 | -3.16 | -2.30 |
| Hours worked, % change | -1.65 | -1.49 | -1.28 | -1.08 |
| Federal debt, points of GDP | +2.0 | -0.5 | -3.3 | -10.6 |

Consumption in Year 10 by lifetime-income group: bottom 25% +1.93%, 25-50 +1.20%, 50-70 +0.32%, 70-90 -0.07% to -0.25%, 90-99 -1.09%, top 1% -2.30% to -11.12%. Compared with "fullB", the added public investment raises long-run output slightly, while the added spending slows the fall in debt. Files: results2_DEP_fullC.json, run_nsra5.py.

## Update: previous bill (v2026.10, run "fullB", November 9, 2026)

Same model and accounting as "fullA", with the two-term changes: the middle-class tax cut narrowed to the 12% bracket only ($85.3B a year, Sec. 2421); Medicare buy-in for ages 50 to 64 (Sec. 2113, $18.4B a year in premium help from Year 2); the hospital price limit in commercial insurance (Sec. 3410(b), about $99B a year in lower private premiums and cost sharing, phased in from Year 2 over four years, from CRFB's estimate of $987B over ten years); and the Social Security formula change withdrawn. Titles moved to companion Acts are not modeled.

| | Year 1 | Year 5 | Year 10 | Year 20 |
|---|---|---|---|---|
| GDP, % change | -1.92 | -1.92 | -1.77 | -1.47 |
| Private investment, % change | -4.68 | -3.24 | -2.98 | -2.02 |
| Hours worked, % change | -1.64 | -1.49 | -1.29 | -1.07 |
| Federal debt, points of GDP | +2.0 | -0.8 | -4.1 | -12.3 |

Consumption in Year 10 by lifetime-income group: bottom 25% +1.90%, 25-50 +1.16%, 50-70 +0.29%, 70-90 -0.09% to -0.28%, 90-99 -1.11%, top 1% -2.34% to -11.16%. Compared with "fullA", lower-income and middle-income households consume more and work slightly less, so GDP and investment are somewhat lower and debt falls a little more slowly. Files: results2_DEP_fullB.json, run_nsra4.py.

## Update: previous bill (v2026.8, run "fullA", November 8, 2026)

Same model and accounting as the central run, with the changes made since: the Phase 2 wage-floor credit withdrawn, rewilding and food-system funding moved from automatic infrastructure spending ($95B) to the annual budget ($55B remains), and crop-insurance savings returned to farmers (Sec. 705(d)), so they no longer count as a cut. Title XL adds no direct spending and is not modeled.

| | Year 1 | Year 5 | Year 10 | Year 20 |
|---|---|---|---|---|
| GDP, % change | -1.89 | -1.79 | -1.55 | -1.10 |
| Private investment, % change | -4.39 | -2.99 | -2.60 | -1.30 |
| Hours worked, % change | -1.60 | -1.37 | -1.13 | -0.89 |
| Federal debt, points of GDP | +2.0 | -0.8 | -4.8 | -14.7 |

Consumption in Year 10 by lifetime-income group: bottom 25% +1.35%, 25-50 +0.82%, 50-70 +0.12%, 70-90 -0.10% to -0.22%, 90-99 -1.03%, top 1% -2.31% to -11.10%. Files: results2_DEP_fullA.json, run_nsra3.py.

## Who gains and who pays (central run, Year 10)

Change in consumption per person by lifetime-income group (percentiles of lifetime earnings ability):

| Group | Consumption | Hours worked |
|---|---|---|
| 0-25 | +1.49% | -2.87% |
| 25-50 | +0.91% | -2.50% |
| 50-70 | +0.18% | -2.05% |
| 70-80 | -0.09% | -1.81% |
| 80-90 | -0.21% | -1.72% |
| 90-99 | -1.03% | -0.67% |
| 99-99.5 | -2.33% | +0.95% |
| 99.5-99.9 | -3.68% | +2.17% |
| 99.9-99.99 | -6.67% | +3.56% |
| top 0.01 | -11.06% | +2.93% |

Remaining-lifetime consumption by generation (discounted at 3%), all income groups combined:

| Cohort | Bottom 25% | 25–50% | 50–70% | 90–99% | Top 1% band (99–99.5) | All |
|---|---|---|---|---|---|---|
| age 65 in Year 1 | -0.12 | -0.30 | -0.39 | -1.19 | -1.90 | -0.81 |
| age 45 in Year 1 | +0.76 | +0.17 | -0.35 | -2.01 | -4.04 | -1.54 |
| age 25 in Year 1 | +1.77 | +1.03 | +0.31 | -1.40 | -3.76 | -0.75 |
| turns 21 in Year 10 | +1.78 | +1.26 | +0.45 | -1.48 | -4.01 | -0.70 |
| turns 21 in Year 20 | +1.80 | +1.21 | +0.41 | -1.56 | -4.24 | -0.78 |

**How to read this.** The model counts a household as better off only through its own consumption and leisure. It gives no value to health coverage beyond its cost or to lower federal debt except through the economy, so deficit reduction always reads as lost consumption today. The central run counts lower drug prices in private plans, the consumer-finance protections and the productivity of public investment (see the mapping table).

## Sensitivity

| Run | GDP Y1 | GDP Y10 | GDP Y20 | GDP Y30 | Debt Y10 (pts) | Debt Y20 (pts) | Bottom 25% cons. Y10 | 50–70% cons. Y10 |
|---|---|---|---|---|---|---|---|---|
| **Central: the bill as written (v2026.6, with the middle-class package)** | -1.90 | -1.48 | -0.98 | -1.14 | -4.0 | -13.1 | +1.49 | +0.18 |
| v2026.5 bill (25% corporate rate, infrastructure fee, no Sec. 2421), same full accounting | -1.97 | -1.29 | -0.52 | -0.96 | -10.7 | -26.7 | +1.22 | -0.53 |
| v2026.5 bill, narrow accounting (no private drug savings, consumer-finance savings or public-capital productivity) | -1.55 | -1.17 | -0.62 | -1.22 | -10.2 | -25.6 | +0.55 | -0.86 |
| v2026.5 narrow accounting, with the net savings returned to every adult as an equal payment (deficit-neutral test) | -2.19 | -2.35 | -2.46 | -2.44 | +2.6 | +2.9 | +3.24 | +0.49 |
| v2026.5 **reference mapping**: enforcement, royalties and the 28% limit treated as consumption taxes | -1.38 | -0.97 | -0.40 | -1.02 | -10.8 | -26.7 | +0.46 | -0.95 |
| v2026.5 reference, debt rule starts Year 10 | -1.34 | -0.85 | -1.64 | -1.52 | -11.0 | +7.6 | +0.38 | -1.04 |
| v2026.5 reference, debt rule starts Year 30 | -1.38 | -0.99 | -0.47 | -0.33 | -10.8 | -26.6 | +0.46 | -0.94 |
| v2026.5 reference, labor supply less responsive (Frisch 0.27) | -1.19 | -0.90 | -0.41 | -1.01 | -10.5 | -25.5 | +1.09 | -0.67 |
| v2026.5 reference, labor supply more responsive (Frisch 0.60) | -1.61 | -1.05 | -0.39 | -1.04 | -11.1 | -27.8 | -0.17 | -1.10 |
| v2026.5 reference, public capital raises productivity (elasticity 0.05) | -1.43 | -0.87 | -0.17 | -0.67 | -11.1 | -27.4 | +0.69 | -0.80 |

The calibration and closure tests were run on the v2026.5 reference mapping; compare each with the reference row. The two rows above them show the effect of the middle-class package on the same accounting: more consumption for the bottom 70%, slower debt reduction and lower investment.

The dip after Year 20 in most runs comes from the model's debt rule: from the start year, government purchases and transfers adjust to steer debt back to its long-run target, so the bill's savings are spent on purchases the model does not value. Moving the start to Year 30 removes most of it.

## Calibration

| Setting | Value | Why |
|---|---|---|
| Tax functions | DEP (ratio of polynomials), estimated on Tax-Calculator 6.9 output for 2028 | The OG-USA default (HSV) has two parameters and captured only about 60% of the static revenue of the bill's top-end changes; DEP reproduces the Tax-Calculator change (about 6.7% of income and payroll tax). Held constant after 2028. |
| Frisch elasticity of labor supply | 0.40 (0.27 and 0.60 tested) | Middle of the micro-evidence range; 0.27 is close to the values CBO uses. |
| Risk aversion (CRRA) | 1.5 | OG-USA default; standard in the literature. |
| Capital share | 0.38 | OG-USA default. |
| Public capital in production | on: investment 2.8% of GDP, output elasticity 0.083 | Nondefense public gross investment 2024: federal $223B (BEA) plus state and local $598B (NIPA Table 5.9.5) = 2.8% of GDP; elasticity from Bom and Ligthart (2014). The narrow-accounting runs leave it off. |
| Foreign purchases of new debt / capital | 40% / 50% | OG-USA defaults; partly open economy. |
| Debt rule | starts Year 20 (10 and 30 tested) | OG-USA default; see Sensitivity. |
| Baseline | OG-USA 0.6.2 defaults, current law including P.L. 119-21 | Not re-targeted to CBO's February 2026 baseline. |

## How each provision enters the model (central run)

| Provision | Model input |
|---|---|
| Secs. 2408, 2420(a)-(c); paid-leave contribution (Title XXXVIII) | Re-estimated individual and payroll tax functions (Tax-Calculator 6.9, `iit_reform.json`) |
| Sec. 2421 middle-class tax relief, $128B a year (Tax-Calculator: $142.5B static, less $11.8B recapture above $400K / $450K, less 2% response) | Income support distributed by the average cut at each income level. Conservative: no work-incentive effect from the lower rates |
| Corporate rate kept at 21%; Pillar Two, buyback excise, excess-profits assessment, acquisition-debt cap, carried interest, export-income deduction repeal; IRS enforcement; federal royalties | Effective corporate rate, calibrated to the model's own corporate base |
| LIFO, advertising and fossil-fuel cost-recovery changes | Lower tax depreciation rate |
| Carbon fee (Sec. 2410, with the Sec. 3410(f) increase) | Consumption tax |
| Household energy credits to 400% of poverty | Transfers; the run used +$20B for the extension, the bill as costed uses $17.5B (Schedule G), so this is slightly generous |
| Financial transaction tax, carryover basis, FTA, 28% limit on tax preferences | Tax on wealth, falling mainly on high-wealth households |
| Lower drug prices in private plans: about $42B a year | Transfers to all adults, phased in. Based on the Milliman / West Health estimate of $293B over 2023-2029 for all-payer negotiated prices under H.R. 3 (2021); a comparable policy, not an estimate for the NSRA |
| Overdraft cap and 36% rate cap: $7.9B a year | Transfers to lower-income adults (CFPB 2024 overdraft rule estimate $5B; Center for Responsible Lending 2023 estimate $2.9B) |
| Basic Minimum Plan, student loans, wage credit, TANF, housing, child accounts, veterans, Social Security protections, child care, paid-leave benefits | Transfers aimed at the ages and income groups each program reaches, phased in on the Schedule E timetable |
| Medicare payment integrity and Sec. 3410(c) drug negotiation | Lower government purchases: the government buys the same care for less, so benefits are unchanged |
| Improper payments, crop insurance, fraud recovery | Lower transfers, in proportion to existing transfers in the affected groups |
| Sec. 3410(b) Social Security solvency | Lower earnings-linked benefits from Year 8, phased over 40 years |
| Infrastructure and science | Public investment that raises productivity |
| Digital government, IRS investment, rural health; appropriations caps | Government purchases (caps phased over 10 years) |

## Benefits the model still does not count

- **Health coverage** is valued only at its cost to the government; protection from medical bills and better health are not counted.
- **Medical debt off credit reports (Sec. 2416) and rent and utility payments counted toward credit (Sec. 1612).** The CFPB estimated that removing about $49 billion of medical bills from 15 million credit reports would raise scores about 20 points on average. Better credit is not something the model can price.
- **Lower risk of a financial crisis (Secs. 1605-1611).** The model has no financial crises in it.

## What this run does not do

- It has not been reviewed by anyone outside the project.
- Transfers are lump-sum; the model cannot represent the phase-outs that reduce work disincentives, so the drop in hours among lower-income households is likely overstated.
- Health effects, crime, education and other non-market outcomes are outside the model.
- The household groups are lifetime-earnings groups, not annual income brackets.

## Files

`run_nsra2.py` (all runs), `tf_dep.py` (tax functions), `analyze2.py` (results), `fidelity.py` (tax-function check), `iit_reform.json`, and `results2_DEP_<run>.json` for each run. Earlier first-round files (`run_nsra.py`, `results_*.json`) are kept for the record; their GDP figures are superseded because the first round collected only part of the bill's taxes.
