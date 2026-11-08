"""NSRA OG-USA runs, round 2 (methodology v2026.5, detailed mapping).

Model: OG-USA 0.6.2 / OG-Core 0.24.3. Tax functions re-estimated from Tax-Calculator 6.9
(public CPS file) for the baseline and for the individual/payroll reform in iit_reform.json
(Secs. 2408, 2420(a)-(c) and the Title XXXVIII paid-leave contribution).

Stages
  base_<v>   baseline solve for calibration variant v (default baseline is out/baseline)
  E_<v>      reform solve for variant v

Variants
  c     central calibration (OG-USA defaults), closure starts Year 20 (tG1 = 20)
  t10   as c, closure starts Year 10
  t30   as c, closure starts Year 30
  f027  Frisch elasticity 0.27 (baseline and reform)
  f060  Frisch elasticity 0.60 (baseline and reform)
  pub   public capital on: baseline public investment 2.0% of GDP moved from G to I_g,
        output elasticity of public capital 0.05; NSRA infrastructure enters as I_g

All dollar amounts are first-year (2028) dollars converted to shares of GDP ($34.3T).
Model year 1 is the first year of the reform.
"""
import os, sys, json, time, copy, pickle
import numpy as np
from ogcore.parameters import Specifications
from ogcore.execute import runner
import ogusa

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
GDP28 = 34300.0
DEF = json.load(open(os.path.join(os.path.dirname(ogusa.__file__), 'ogusa_default_parameters.json')))

TFT = os.environ.get('TFT', 'HSV')   # tax-function form: HSV (OG-USA default) or DEP
SFX = '' if TFT == 'HSV' else '_' + TFT
BASEDIR = {'c': 'baseline', 't10': 'baseline', 't30': 'baseline',
           'f027': 'base_f027', 'f060': 'base_f060', 'pub': 'base_pub', 'c2': 'baseline', 'dn': 'baseline'}
if SFX:
    BASEDIR = {k: 'base' + SFX + ('' if v == 'baseline' else v[4:]) for k, v in BASEDIR.items()}
CAL = {'c': {}, 't10': {}, 't30': {}, 'f027': {'frisch': 0.27}, 'f060': {'frisch': 0.60}, 'pub': {}, 'c2': {}, 'dn': {}}
# start alternative-calibration steady states from the central baseline solution
_ss = os.path.join(OUT, 'baseline', 'SS', 'SS_vars.pkl')
if os.path.exists(_ss):
    _s = pickle.load(open(_ss, 'rb'))
    for _v in ('f027', 'f060', 'pub'):
        CAL[_v].update({'initial_guess_r_SS': float(_s['r']), 'initial_guess_TR_SS': float(_s['TR']),
                        'initial_guess_factor_SS': float(_s['factor'])})

RAMP = [0.86, 0.94, 0.98] + [1.0] * 397       # revenue realization (Schedule G sec. 4)
OUTRAMP = [0.55, 0.75, 0.90] + [1.0] * 397    # programs phase in behind Schedule E gates


def log(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


def phase(start, years, T):
    """Fraction of full effect by model year (1-based start), linear over `years`."""
    out = np.zeros(T)
    for y in range(T):
        k = y + 1 - start + 1
        if k > 0:
            out[y] = min(1.0, k / years)
    return out


def make_p(baseline, outdir, basedir, tf, cal):
    p = Specifications(baseline=baseline, num_workers=1,
                       baseline_dir=os.path.join(OUT, basedir), output_base=outdir)
    d = copy.deepcopy(DEF); d.pop('BW', None)
    p.update_specifications(d)
    p.update_specifications(tf)
    if cal:
        p.update_specifications(cal)
    return p


def pub_baseline(p):
    T = p.T + p.S
    aG = np.array(p.alpha_G, dtype=float).reshape(-1)[:T]
    return {'alpha_I': [0.02] * T, 'gamma_g': [0.05], 'initial_Kg_ratio': 0.6,
            'alpha_G': (aG - 0.02).tolist()}


# ---------------------------------------------------------------- transfers
# (name, $B full effect, timing, age range [lo, hi] in years, per-person weight by lifetime-income group j=0..9)
TRANSFERS = [
    ('Basic Minimum Plan (Title XXI), net new federal cost', 180, 'out', (21, 64), [3, 2.5, 1.5, .8, .5, .3, .1, .1, .1, .1]),
    ('Zero-interest student loans (Sec. 1501)', 55, 'out', (22, 45), [.5, 1, 1.3, 1.5, 1.5, 1.3, 1, .8, .5, .3]),
    ('SPI wage-floor credit (Sec. 2407)', 10, 'out', (21, 64), [3, 2, 1, .2, 0, 0, 0, 0, 0, 0]),
    ('TANF enhancement', 5, 'out', (21, 45), [4, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
    ('Housing security and down payment help (Title XIV)', 1.5, 'out', (25, 40), [.5, 1.5, 1.5, 1, .3, 0, 0, 0, 0, 0]),
    ('Child Prosperity Trust deposits (Sec. 502)', 7.6, 'out', (25, 40), [1.5, 1.3, 1, 1, 1, .8, .5, .5, .5, .5]),
    ('Veterans Health Security Fund (Title XXV)', 8, 'out', (25, 100), [1] * 10),
    ('Social Security anti-erosion protections', 30, 'out', (65, 100), [1.5, 1.3, 1.1, 1, .9, .8, .7, .7, .7, .7]),
    ('Household energy bill credits (Sec. 2410(c))', 25, 'out', (21, 100), [2, 2, 1.2, .3, 0, 0, 0, 0, 0, 0]),
    ('Child care (Title XXXVIII)', 16, 'out', (25, 45), [1.5, 1.4, 1.2, 1, .8, .5, .3, .2, .1, .1]),
    ('Paid family and medical leave benefits (Title XXXVIII)', 100, 'full', (22, 50), [.4, .7, 1, 1.3, 1.6, 2, 2.5, 3, 3, 3]),
    ('Medicare payment integrity savings (Sec. 2112)', -40, 'out', (65, 100), [1] * 10),
    ('FSP-2 Medicare drug negotiation and post-acute reform', -25, (2, 5), (65, 100), [1] * 10),
    ('FSP-6 improper-payment reduction', -8, (2, 3), (21, 100), [1] * 10),
    ('FSP-7 crop insurance reform', -5, (2, 1), (40, 80), [.2, .3, .5, .8, 1, 1.5, 3, 3, 3, 3]),
    ('Fraud recovery (Title I)', -9, 'full', (21, 100), [1] * 10),
]


def timing(tag, T):
    if tag == 'out':
        return np.array(OUTRAMP[:T])
    if tag == 'full':
        return np.ones(T)
    return phase(tag[0], tag[1], T)


def target_shares(p, ages, jw, T, base_eta=None):
    """Share of a transfer received by each (t, s, j) cell: population x age selector x weight.
    For a cut (base_eta given), shares follow existing transfers in the selected cells, so no cell goes negative."""
    S, J = p.S, p.J
    ageyrs = np.linspace(p.starting_age, p.ending_age, S, endpoint=False)
    sel = ((ageyrs >= ages[0]) & (ageyrs < ages[1] + 1)).astype(float)
    om = np.array(p.omega, dtype=float)[:T]          # (T, S, J): population share by age and group
    w = (om if base_eta is None else base_eta) * sel[None, :, None] * np.array(jw, dtype=float)[None, None, :]
    tot = w.sum(axis=(1, 2), keepdims=True)
    return w / np.where(tot > 0, tot, 1)


def reform_update(p, v):
    T = p.T + p.S
    upd = {}
    # ---- business taxes on capital (calibrated to the model's own corporate base: 6.05% of GDP at 21%)
    # Pillar Two 50 + buyback excise 15 + excess-profits 10 + acquisition-debt cap 5 + carried interest 1.4
    # + FDDEI share of base broadening 28.7 = $110.1B -> +5.3 points on the 25% statutory rate.
    cit = 0.25 + (110.1 / GDP28) / 0.000605 / 100
    upd['cit_rate'] = [[cit]] * T
    inc = v in ('c2', 'dn')
    if inc:
        # c2: IRS enforcement (mostly business and high-income underreporting) and federal royalties (resource rents)
        # are placed on capital, not on consumption
        citp = 0.25 + ((110.1 + 12 + 35 * np.array(RAMP[:T])) / GDP28) / 0.000605 / 100
        upd['cit_rate'] = [[x] for x in citp.tolist()]
        cit = float(citp[3])
    # timing share of base broadening (LIFO, advertising, fossil cost recovery) $18.3B -> lower tax depreciation
    kc_y = 3.47 * 0.55
    dtau = (18.3 / GDP28) / (cit * kc_y)
    upd['_dtau'] = dtau
    # ---- consumption-tax proxy: carbon fee 85, NIMA 30, IRS enforcement 35 (ramped), royalties 12,
    #      FSP-4 28% limit 22; FSP-5 carbon rise 40 from Year 2 over 7 years. C/Y = 0.71.
    cbase = 0.71 * GDP28
    yrs = np.arange(T)
    cons = (85 + 30 + 12 + 22 + 35 * np.array(RAMP[:T]) + 40 * phase(2, 7, T)) / cbase
    if inc:  # c2: only the carbon fee and NIMA, taxes that pass into prices, stay in the consumption proxy
        cons = (85 + 30 + 40 * phase(2, 7, T)) / cbase
    tc = np.array(p.tau_c, dtype=float).reshape(-1)[:T]
    upd['tau_c'] = [[x] for x in (tc + cons).tolist()]
    # ---- wealth-tax proxy: FTT 75 + carryover basis 15 + FTA 3 = $93B
    upd['h_wealth'] = [10.0]; upd['m_wealth'] = [0.1]
    upd['p_wealth'] = [0.00056 * (93 + (22 if inc else 0)) / 90] * T   # c2 adds the 28% limit (top incomes)
    upd['wealth_tax_filer'] = [[1.0] * p.J] * T   # OG-USA default exempts all groups; the FTT and carryover basis apply to all
    # ---- transfers: amount path and time-varying distribution (eta)
    aT = np.array(p.alpha_T, dtype=float).reshape(-1)[:T]
    eta_b = np.array(p.eta, dtype=float)[:T]
    num = aT[:, None, None] * eta_b
    add = np.zeros(T)
    for name, amt, tag, ages, jw in TRANSFERS:
        a = amt / GDP28 * timing(tag, T)
        add += a
        sh = target_shares(p, ages, jw, T, num / num.sum(axis=(1, 2), keepdims=True) if amt < 0 else None)
        num += a[:, None, None] * sh
    if v == 'dn':
        # counterfactual: return the run-c2 net fiscal saving (revenue - transfers - purchases, % of GDP)
        # to every adult as an equal per-person payment, so the debt path stays near baseline
        net = np.interp(np.arange(T), [0, 1, 2, 4, 9, 19], [1.48, 1.34, 1.26, 1.31, 1.70, 1.72]) / 100
        add += net
        num += net[:, None, None] * target_shares(p, (21, 100), [1] * 10, T)
    assert num.min() >= -1e-12, num.min()
    num = np.clip(num, 0, None)
    eta_r = num / num.sum(axis=(1, 2), keepdims=True)
    upd['alpha_T'] = (aT + add).tolist()
    upd['_eta'] = eta_r
    # FSP-1 Social Security solvency, $45B at full effect from Year 8 over 40 years, as a cut in the
    # replacement rate (pension outlays ~7.3% of GDP). The bill targets top earners and raises the
    # minimum benefit; the model applies the net cut through the earnings-linked benefit formula.
    upd['replacement_rate_adjust'] = [[x] for x in (1 - (45 / GDP28) / 0.073 * phase(8, 40, T)).tolist()]
    # ---- government purchases: science 30, digital 5, IRS investment 15, rural health 3 (+ infrastructure 95
    #      unless public capital is on); less appropriations caps 240 phased over 10 years (FSP-3)
    aG = np.array(p.alpha_G, dtype=float).reshape(-1)[:T]
    infra = 95 / GDP28 * np.array(OUTRAMP[:T])
    other = (30 * np.array(OUTRAMP[:T]) + 5 + 15 + 3 * np.array(OUTRAMP[:T])) / GDP28
    caps = 240 / GDP28 * phase(1, 10, T)
    if v == 'pub':
        upd['alpha_G'] = (aG + other - caps).tolist()
        aI = np.array(p.alpha_I, dtype=float).reshape(-1)[:T]
        upd['alpha_I'] = (aI + infra).tolist()
    else:
        upd['alpha_G'] = (aG + infra + other - caps).tolist()
    if v == 't10':
        upd['tG1'] = 10
    if v == 't30':
        upd['tG1'] = 30
    return upd


def main(stage):
    kind, v = stage.split('_', 1)
    tf_b = pickle.load(open(os.path.join(OUT, 'tf_base%s.pkl' % SFX), 'rb'))
    tf_r = pickle.load(open(os.path.join(OUT, 'tf_ref%s.pkl' % SFX), 'rb'))
    if kind == 'base':
        bd = BASEDIR[v]
        p = make_p(True, os.path.join(OUT, bd), bd, tf_b, CAL[v])
        if v == 'pub':
            p.update_specifications(pub_baseline(p))
        log('baseline', v); runner(p, time_path=True, client=None); log('baseline done', v)
    else:
        bd = BASEDIR[v]
        p = make_p(False, os.path.join(OUT, 'E' + SFX + '_' + v), bd, tf_r, CAL[v])
        if v == 'pub':
            p.update_specifications(pub_baseline(p))
        aT0 = float(np.array(p.alpha_T).reshape(-1)[0]); tc0 = float(np.array(p.tau_c).reshape(-1)[0])
        upd = reform_update(p, v)
        dtau = upd.pop('_dtau'); eta_r = upd.pop('_eta')
        p.update_specifications(upd)
        p.eta = eta_r
        # lower tax depreciation directly on the model-period array (1 model period = 1 year)
        p.delta_tau = np.clip(np.array(p.delta_tau, dtype=float) - dtau, 0, None)
        json.dump({'cit_rate': upd['cit_rate'][0][0], 'delta_tau_cut': dtau,
                   'tau_c_add_y1': upd['tau_c'][0][0] - tc0,
                   'alpha_T_add_y1_pct_gdp': 100 * (upd['alpha_T'][0] - aT0),
                   'alpha_G_y1': upd['alpha_G'][0], 'tG1': int(np.array(p.tG1).reshape(-1)[0]),
                   'frisch': float(np.array(p.frisch).reshape(-1)[0])},
                  open(os.path.join(OUT, 'E%s_%s_inputs.json' % (SFX, v)), 'w'), indent=1)
        log('reform', v, 'cit %.4f dtau %.5f' % (upd['cit_rate'][0][0], dtau))
        runner(p, time_path=True, client=None); log('reform done', v)


if __name__ == '__main__':
    main(sys.argv[1])
