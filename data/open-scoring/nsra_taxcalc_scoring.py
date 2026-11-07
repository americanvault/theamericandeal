"""Open-standards check of NSRA income and payroll tax provisions with Tax-Calculator (Policy Simulation Library).
pip install taxcalc==6.9.0 ; python nsra_taxcalc_scoring.py
Data: the public CPS file bundled with Tax-Calculator. It under-represents top incomes and omits capital gains and
partnership/S-corporation income, so Secs. 2420(b) and 2420(c) cannot be scored with it. Static results, calendar 2028,
current-law baseline (Public Law 119-21). NSRA applies behavioral and income-tax-offset adjustments on top (Schedule G)."""
import taxcalc as tc, numpy as np, json, warnings; warnings.filterwarnings('ignore')
Y = '2028'; recs = tc.Records.cps_constructor()
def calc(ref=None):
    p = tc.Policy()
    if ref: p.implement_reform(ref)
    c = tc.Calculator(policy=p, records=recs); c.advance_to_year(int(Y)); c.calc_all(); return c
base = calc(); w = base.array('s006'); agi = base.array('c00100'); res = {}
def score(name, ref, var='combined'):
    c = calc(ref); res[name] = round(((c.array(var) - base.array(var)) * w).sum() / 1e9, 1); print(name, res[name])
# Sec. 2420(a): 39.6% above $400K single / $450K joint / $425K head of household / $225K separate
score('2420(a) top rate 39.6%', {'II_rt7': {Y: 0.396}, 'II_brk5': {Y: [270431.19, 450000, 225000, 270404.81, 450000]},
                                 'II_brk6': {Y: [400000, 450001, 225001, 425000, 450001]}})
# Sec. 2408: OASDI tax on wages above $400,000 (gap between the current cap and $400,000 untouched)
score('2408 payroll tax above $400K', {'SS_Earnings_thd': {Y: 400000}}, var='payrolltax')
# Sec. 3410(e): 28% limit on itemized deductions and on retirement and tax-exempt-interest exclusions, AGI > $400K
m = base.mtr('e00200p')[1]; hi = agi > 400e3
item = np.where(base.array('c04470') > base.array('standard'), base.array('c04470'), 0)
res['3410(e) itemized'] = round((np.where(hi, np.maximum(m - 0.28, 0) * item, 0) * w).sum() / 1e9, 1)
excl = base.array('pencon_p') + base.array('pencon_s') + base.array('e00400')
res['3410(e) retirement + muni exclusions'] = round((np.where(hi, np.maximum(m - 0.28, 0) * excl, 0) * w).sum() / 1e9, 1)
print(json.dumps(res, indent=1)); json.dump(res, open('nsra_taxcalc_results_2028.json', 'w'), indent=1)
