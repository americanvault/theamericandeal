"""Write the OG-USA README from the result files (round 2, DEP tax functions)."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
def R(v):
    p = os.path.join(H, 'results2_DEP_%s.json' % v)
    return json.load(open(p)) if os.path.exists(p) else None
def m(o, yr, k):
    for r in o['macro']:
        if r['year'] == yr:
            return r[k]
def f(x, d=1):
    return ('%+.' + str(d) + 'f') % x

C = R('fullp')
VAR = [('fullp', '**Central: the bill as written (v2026.6, with the middle-class package)**'),
       ('full', 'v2026.5 bill (25% corporate rate, infrastructure fee, no Sec. 2421), same full accounting'),
       ('c2', 'v2026.5 bill, narrow accounting (no private drug savings, consumer-finance savings or public-capital productivity)'), ('dn', 'v2026.5 narrow accounting, with the net savings returned to every adult as an equal payment (deficit-neutral test)'),
       ('c', 'v2026.5 **reference mapping**: enforcement, royalties and the 28% limit treated as consumption taxes'),
       ('t10', 'v2026.5 reference, debt rule starts Year 10'), ('t30', 'v2026.5 reference, debt rule starts Year 30'),
       ('f027', 'v2026.5 reference, labor supply less responsive (Frisch 0.27)'), ('f060', 'v2026.5 reference, labor supply more responsive (Frisch 0.60)'),
       ('pub', 'v2026.5 reference, public capital raises productivity (elasticity 0.05)')]
L = []
w = L.append
w('# NSRA: OG-USA dynamic analysis (round 2, November 2026)\n')
w('We ran OG-USA, the open-source overlapping-generations model of the U.S. economy maintained by the Policy Simulation Library, on the NSRA as written (methodology v2026.6, which adds the middle-class tax relief of Sec. 2421, keeps the 21% corporate rate, withdraws the infrastructure fee and extends household energy credits to 400% of poverty). **We ran it ourselves. It is not an independent score and not a CBO or JCT estimate.** Every input, script and result is in this folder so anyone can reproduce or challenge it. Corrections are welcome.\n')
w('> This run was made before methodology v2026.7, which moved the rewilding and regional food-system programs to annual appropriations and withdrew the Phase 2 wage-floor credit, about $50 billion a year less mandatory spending. With that change, debt would fall slightly faster than shown here.\n')
w('## Headline (central run)\n')
w('| | Year 1 | Year 5 | Year 10 | Year 20 |')
w('|---|---|---|---|---|')
for k, lab in [('Y', 'GDP, % change'), ('w', 'Wages, % change'), ('I', 'Private investment, % change'), ('L', 'Hours worked, % change'), ('debt_gdp_pts', 'Federal debt, points of GDP')]:
    w('| %s | %s |' % (lab, ' | '.join(f(m(C, y, k), 1 if k == 'debt_gdp_pts' else 2) for y in (1, 5, 10, 20))))
w('\nThe bill raises about %.1f%% of GDP in revenue and returns about %.1f%% as transfers, including the middle-class tax relief; the rest reduces the deficit. Households in roughly the bottom 70%% of lifetime income consume more from Year 1. The economy is smaller at first and debt falls more slowly than in the v2026.5 bill, because less of the revenue goes to deficit reduction (see Sensitivity).\n' % (m(C, 10, 'revenue_gdp_pts'), m(C, 10, 'transfers_gdp_pts')))
w('## Who gains and who pays (central run, Year 10)\n')
w('Change in consumption per person by lifetime-income group (percentiles of lifetime earnings ability):\n')
w('| Group | Consumption | Hours worked |')
w('|---|---|---|')
for g, d in C['by_income_group']['year_10'].items():
    w('| %s | %s%% | %s%% |' % (g, f(d['consumption_pct'], 2), f(d['hours_pct'], 2)))
w('\nRemaining-lifetime consumption by generation (discounted at 3%), all income groups combined:\n')
w('| Cohort | Bottom 25% | 25–50% | 50–70% | 90–99% | Top 1% band (99–99.5) | All |')
w('|---|---|---|---|---|---|---|')
for k, d in C['generations_lifetime_consumption_pct'].items():
    w('| %s | %s | %s | %s | %s | %s | %s |' % (k, f(d['0-25'], 2), f(d['25-50'], 2), f(d['50-70'], 2), f(d['90-99'], 2), f(d['99-99.5'], 2), f(d['all'], 2)))
w('\n**How to read this.** The model counts a household as better off only through its own consumption and leisure. It gives no value to health coverage beyond its cost or to lower federal debt except through the economy, so deficit reduction always reads as lost consumption today. The central run counts lower drug prices in private plans, the consumer-finance protections and the productivity of public investment (see the mapping table).\n')
w('## Sensitivity\n')
w('| Run | GDP Y1 | GDP Y10 | GDP Y20 | GDP Y30 | Debt Y10 (pts) | Debt Y20 (pts) | Bottom 25% cons. Y10 | 50–70% cons. Y10 |')
w('|---|---|---|---|---|---|---|---|---|')
for v, lab in VAR:
    o = R(v)
    if not o:
        w('| %s | not completed | | | | | | | |' % lab); continue
    b = o['by_income_group']['year_10']
    w('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (lab, f(m(o, 1, 'Y'), 2), f(m(o, 10, 'Y'), 2), f(m(o, 20, 'Y'), 2), f(m(o, 30, 'Y'), 2),
                                                          f(m(o, 10, 'debt_gdp_pts')), f(m(o, 20, 'debt_gdp_pts')), f(b['0-25']['consumption_pct'], 2), f(b['50-70']['consumption_pct'], 2)))
w('\nThe calibration and closure tests were run on the v2026.5 reference mapping; compare each with the reference row. The two rows above them show the effect of the middle-class package on the same accounting: more consumption for the bottom 70%, slower debt reduction and lower investment.\n')
w('The dip after Year 20 in most runs comes from the model\'s debt rule: from the start year, government purchases and transfers adjust to steer debt back to its long-run target, so the bill\'s savings are spent on purchases the model does not value. Moving the start to Year 30 removes most of it.\n')
w('## Calibration\n')
w('| Setting | Value | Why |')
w('|---|---|---|')
for row in [
    ('Tax functions', 'DEP (ratio of polynomials), estimated on Tax-Calculator 6.9 output for 2028', 'The OG-USA default (HSV) has two parameters and captured only about 60% of the static revenue of the bill\'s top-end changes; DEP reproduces the Tax-Calculator change (about 6.7% of income and payroll tax). Held constant after 2028.'),
    ('Frisch elasticity of labor supply', '0.40 (0.27 and 0.60 tested)', 'Middle of the micro-evidence range; 0.27 is close to the values CBO uses.'),
    ('Risk aversion (CRRA)', '1.5', 'OG-USA default; standard in the literature.'),
    ('Capital share', '0.38', 'OG-USA default.'),
    ('Public capital in production', 'on: investment 2.8% of GDP, output elasticity 0.083', 'Nondefense public gross investment 2024: federal $223B (BEA) plus state and local $598B (NIPA Table 5.9.5) = 2.8% of GDP; elasticity from Bom and Ligthart (2014). The narrow-accounting runs leave it off.'),
    ('Foreign purchases of new debt / capital', '40% / 50%', 'OG-USA defaults; partly open economy.'),
    ('Debt rule', 'starts Year 20 (10 and 30 tested)', 'OG-USA default; see Sensitivity.'),
    ('Baseline', 'OG-USA 0.6.2 defaults, current law including P.L. 119-21', 'Not re-targeted to CBO\'s February 2026 baseline.'),
]:
    w('| %s | %s | %s |' % row)
w('\n## How each provision enters the model (central run)\n')
w('| Provision | Model input |')
w('|---|---|')
for row in [
    ('Secs. 2408, 2420(a)-(c); paid-leave contribution (Title XXXVIII)', 'Re-estimated individual and payroll tax functions (Tax-Calculator 6.9, `iit_reform.json`)'),
    ('Sec. 2421 middle-class tax relief, $128B a year (Tax-Calculator: $142.5B static, less $11.8B recapture above $400K / $450K, less 2% response)', 'Income support distributed by the average cut at each income level. Conservative: no work-incentive effect from the lower rates'),
    ('Corporate rate kept at 21%; Pillar Two, buyback excise, excess-profits assessment, acquisition-debt cap, carried interest, export-income deduction repeal; IRS enforcement; federal royalties', 'Effective corporate rate, calibrated to the model\'s own corporate base'),
    ('LIFO, advertising and fossil-fuel cost-recovery changes', 'Lower tax depreciation rate'),
    ('Carbon fee (Sec. 2410, with the Sec. 3410(f) increase)', 'Consumption tax'),
    ('Household energy credits to 400% of poverty', 'Transfers; the run used +$20B for the extension, the bill as costed uses $17.5B (Schedule G), so this is slightly generous'),
    ('Financial transaction tax, carryover basis, FTA, 28% limit on tax preferences', 'Tax on wealth, falling mainly on high-wealth households'),
    ('Lower drug prices in private plans: about $42B a year', 'Transfers to all adults, phased in. Based on the Milliman / West Health estimate of $293B over 2023-2029 for all-payer negotiated prices under H.R. 3 (2021); a comparable policy, not an estimate for the NSRA'),
    ('Overdraft cap and 36% rate cap: $7.9B a year', 'Transfers to lower-income adults (CFPB 2024 overdraft rule estimate $5B; Center for Responsible Lending 2023 estimate $2.9B)'),
    ('Basic Minimum Plan, student loans, wage credit, TANF, housing, child accounts, veterans, Social Security protections, child care, paid-leave benefits', 'Transfers aimed at the ages and income groups each program reaches, phased in on the Schedule E timetable'),
    ('Medicare payment integrity and Sec. 3410(c) drug negotiation', 'Lower government purchases: the government buys the same care for less, so benefits are unchanged'),
    ('Improper payments, crop insurance, fraud recovery', 'Lower transfers, in proportion to existing transfers in the affected groups'),
    ('Sec. 3410(b) Social Security solvency', 'Lower earnings-linked benefits from Year 8, phased over 40 years'),
    ('Infrastructure and science', 'Public investment that raises productivity'),
    ('Digital government, IRS investment, rural health; appropriations caps', 'Government purchases (caps phased over 10 years)'),
]:
    w('| %s | %s |' % row)
w('\n## Benefits the model still does not count\n')
w('- **Health coverage** is valued only at its cost to the government; protection from medical bills and better health are not counted.')
w('- **Medical debt off credit reports (Sec. 2416) and rent and utility payments counted toward credit (Sec. 1612).** The CFPB estimated that removing about $49 billion of medical bills from 15 million credit reports would raise scores about 20 points on average. Better credit is not something the model can price.')
w('- **Lower risk of a financial crisis (Secs. 1605-1611).** The model has no financial crises in it.')
w('\n## What this run does not do\n')
w('- It has not been reviewed by anyone outside the project.')
w('- Transfers are lump-sum; the model cannot represent the phase-outs that reduce work disincentives, so the drop in hours among lower-income households is likely overstated.')
w('- Health effects, crime, education and other non-market outcomes are outside the model.')
w('- The household groups are lifetime-earnings groups, not annual income brackets.\n')
w('## Files\n')
w('`run_nsra2.py` (all runs), `tf_dep.py` (tax functions), `analyze2.py` (results), `fidelity.py` (tax-function check), `iit_reform.json`, and `results2_DEP_<run>.json` for each run. Earlier first-round files (`run_nsra.py`, `results_*.json`) are kept for the record; their GDP figures are superseded because the first round collected only part of the bill\'s taxes.')
open(os.path.join(H, 'README_og.md'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L)[:1500])
