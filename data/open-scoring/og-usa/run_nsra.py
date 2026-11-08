"""Stylized OG-USA run of the NSRA (methodology v2026.4).

Baseline: OG-USA 0.6.2 / OG-Core 0.24.3 defaults (current law incl. P.L. 119-21),
tax functions re-estimated from Tax-Calculator 6.9 on the bundled CPS file.

Reform, all at full effect from 2028 (model year index 2):
  Individual and payroll (Tax-Calculator reform -> new tax functions):
    Sec. 2408   Social Security tax on wages above $400,000 (donut)
    Sec. 2420a  39.6% top rate above $400K single / $450K joint
    Sec. 2420b  NIIT on active pass-through income
    Sec. 2420c  capital gains and dividends at 39.6% above $1M
    Title XXXVIII paid leave: 0.8% payroll contribution (0.4% + 0.4%, modeled on the Medicare tax base)
  Business taxes -> corporate rate 21% to 33.1% (28% statutory plus the
    revenue of Pillar Two, buyback excise, excess-profits assessment and the
    acquisition-debt cap, at JCT's ~$15.7B per point)
  Carbon fee incl. Sec. 3410(f) rise, NIMA, IRS enforcement, royalties and
    fraud recovery ($211B) -> consumption tax +0.90 pts
  Financial transaction tax and carryover basis ($90B) -> 0.056% tax on wealth
  Spending (share of GDP, 2028 GDP $34.3T):
    transfers +$347B (BMP, student loans, SPI credit, energy credits, paid
      leave benefits, other; less Medicare/payment-integrity/crop savings)
    government purchases +$1B (science, child care, IRS investment and
      infrastructure +$161B, less appropriations caps -$160B); infrastructure
      is given no productivity effect (conservative)
Sensitivity B (stage reformB): statutory corporate rate 28% only; Pillar Two,
buyback excise, excess-profits assessment and acquisition-debt cap ($80B)
moved to the broad consumption-tax proxy (+1.24 pts in total).
Revised version C (stage reformC): corporate rate 25%; the $47B difference from
28% replaced by base-broadening, and the $80B of other business taxes, both in the
broad-tax proxy (+1.45 pts); deeper appropriations caps (inflation minus 1.5%),
about $50B more a year in spending restraint.
Final bill D (stage reformD, v2026.5): as C, with appropriations caps at inflation
minus 1.5% worth about $80B a year more restraint (Sec. 3410(d), $240B at full effect).
"""
import os, sys, json, time, copy, pickle
import numpy as np
from ogcore.parameters import Specifications
from ogcore.execute import runner
from ogcore.utils import safe_read_pickle
from ogusa.calibrate import Calibration
import ogusa

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
BASE = os.path.join(OUT, 'baseline'); REF = os.path.join(OUT, 'reform')
REFB = os.path.join(OUT, 'reformB')
REFC = os.path.join(OUT, 'reformC')
REFD = os.path.join(OUT, 'reformD')
GDP28 = 34300.0
START = 2026; K = 0  # reform applied from the first model year (tax functions are time-invariant)

DEF = json.load(open(os.path.join(os.path.dirname(ogusa.__file__), 'ogusa_default_parameters.json')))

IIT_REFORM = json.load(open(os.path.join(HERE, 'iit_reform.json')))


def log(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


def tax_funcs(p, reform):
    c = Calibration(p, estimate_tax_functions=True, iit_reform=reform,
                    client=None, num_workers=2)
    d = c.get_dict()
    return {k: d[k] for k in ('etr_params', 'mtrx_params', 'mtry_params',
                              'mean_income_data', 'frac_tax_payroll')
            if k in d}


def path(v, new, T):
    """Return a time path equal to v before index K and new from K on."""
    a = np.array(v, dtype=float).reshape(-1)
    full = np.concatenate([a, np.repeat(a[-1:], max(0, T - len(a)))])[:T]
    full[K:] = new(full[K:])
    return full.tolist()


def make_p(baseline, outdir, tf):
    p = Specifications(baseline=baseline, num_workers=2,
                       baseline_dir=BASE, output_base=outdir)
    d = copy.deepcopy(DEF)
    d.pop('BW', None)
    p.update_specifications(d)
    p.update_specifications(tf)
    return p


def main(stage):
    os.makedirs(OUT, exist_ok=True)
    if stage == 'tf':
        p = Specifications(baseline=True, num_workers=2, output_base=BASE)
        p.update_specifications({k: v for k, v in DEF.items() if k != 'BW'})
        log('baseline tax functions'); tfb = tax_funcs(p, {})
        pickle.dump(tfb, open(os.path.join(OUT, 'tf_base.pkl'), 'wb'))
        log('reform tax functions'); tfr = tax_funcs(p, IIT_REFORM)
        pickle.dump(tfr, open(os.path.join(OUT, 'tf_ref.pkl'), 'wb'))
        log('tax functions done')
    elif stage == 'base':
        tfb = pickle.load(open(os.path.join(OUT, 'tf_base.pkl'), 'rb'))
        p = make_p(True, BASE, tfb)
        log('baseline solve'); runner(p, time_path=True, client=None); log('baseline done')
    elif stage in ('reform', 'reformB', 'reformC', 'reformD'):
        alt = stage == 'reformB'; rev = stage in ('reformC', 'reformD'); fin = stage == 'reformD'
        tfr = pickle.load(open(os.path.join(OUT, 'tf_ref.pkl'), 'rb'))
        p = make_p(False, {'reform': REF, 'reformB': REFB, 'reformC': REFC, 'reformD': REFD}[stage], tfr)
        T = p.T + p.S
        upd = {
            'cit_rate': [[x] for x in path(np.array(p.cit_rate).reshape(-1), lambda x: x * 0 + (0.25 if rev else 0.28 if alt else 0.331), T)],
            'tau_c': [[x] for x in path(np.array(p.tau_c).reshape(-1), lambda x: x + (0.0145 if rev else 0.0124 if alt else 0.0090), T)],
            'alpha_T': path(p.alpha_T, lambda x: x + 347 / GDP28, T),
            'alpha_G': path(p.alpha_G, lambda x: x + ((1 - 80) if fin else (1 - 50) if rev else 1) / GDP28, T),
            'h_wealth': [10.0], 'm_wealth': [0.1],
            'p_wealth': path(np.zeros(T), lambda x: x + 0.00056, T),
        }
        p.update_specifications(upd)
        log('reform solve'); runner(p, time_path=True, client=None); log('reform done')


if __name__ == '__main__':
    main(sys.argv[1])
