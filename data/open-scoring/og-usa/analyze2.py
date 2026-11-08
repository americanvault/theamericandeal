"""Compare an NSRA reform run with its baseline: macro paths, distribution and generations."""
import pickle, json, os, sys
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
BASEDIR = {'c': 'baseline', 't10': 'baseline', 't30': 'baseline',
           'f027': 'base_f027', 'f060': 'base_f060', 'pub': 'base_pub', 'c2': 'baseline', 'dn': 'baseline'}
GDP = [34300, 35700, 37100, 38600, 40100, 41700, 43400, 45100, 46900, 48800]
EMP = 166.0


def load(d):
    return pickle.load(open(os.path.join(H, 'out', d, 'TPI', 'TPI_vars.pkl'), 'rb'))


SFX = '' if os.environ.get('TFT', 'HSV') == 'HSV' else '_' + os.environ['TFT']
if SFX:
    BASEDIR = {k: 'base' + SFX + ('' if v == 'baseline' else v[4:]) for k, v in BASEDIR.items()}


def run(v):
    b = load(BASEDIR[v]); r = load('E' + SFX + '_' + v)
    pb = pickle.load(open(os.path.join(H, 'out', BASEDIR[v], 'model_params.pkl'), 'rb'))
    om = np.array(pb.omega)            # (T, S, J) population shares
    S, J = pb.S, pb.J
    ages = np.linspace(pb.starting_age, pb.ending_age, S, endpoint=False)

    def pct(k, t):
        return 100 * (float(np.array(r[k])[t]) / float(np.array(b[k])[t]) - 1)

    def share(k, t):
        return 100 * (float(np.array(r[k])[t] / np.array(r['Y'])[t]) - float(np.array(b[k])[t] / np.array(b['Y'])[t]))

    rows = []
    for t in [0, 1, 2, 4, 9, 19, 29, 49]:
        row = {'year': t + 1}
        for k in ['Y', 'C', 'I', 'K', 'L', 'w']:
            row[k] = round(pct(k, t), 2)
        row['r_pts'] = round(100 * float(np.array(r['r'])[t] - np.array(b['r'])[t]), 3)
        row['debt_gdp_pts'] = round(share('D', t), 1)
        row['revenue_gdp_pts'] = round(share('total_tax_revenue', t), 2)
        row['transfers_gdp_pts'] = round(share('TR', t), 2)
        row['G_gdp_pts'] = round(share('G', t), 2)
        row['fte_thousand'] = round(EMP * 1000 * row['L'] / 100)
        rows.append(row)
    out = {'variant': v, 'macro': rows,
           'avg_gdp_pct_y1_10': round(float(np.mean([pct('Y', t) for t in range(10)])), 2),
           'cum_gdp_change_10yr_billion': round(sum(GDP[t] * pct('Y', t) / 100 for t in range(10))),
           'max_resource_constraint_error': float(np.max(np.abs(np.array(r['resource_constraint_error'])[:300])))}

    cb, cr = np.array(b['c']), np.array(r['c'])      # (T, S, J) consumption per person
    nb, nr = np.array(b['n']), np.array(r['n'])
    # by lifetime-income group: population-weighted mean consumption and hours
    names = ['0-25', '25-50', '50-70', '70-80', '80-90', '90-99', '99-99.5', '99.5-99.9', '99.9-99.99', 'top 0.01']
    byj = {}
    for t in [0, 9, 19]:
        w = om[t]
        byj['year_%d' % (t + 1)] = {names[j]: {'consumption_pct': round(100 * ((w[:, j] * cr[t, :, j]).sum() / (w[:, j] * cb[t, :, j]).sum() - 1), 2),
                                             'hours_pct': round(100 * ((w[:, j] * nr[t, :, j]).sum() / (w[:, j] * nb[t, :, j]).sum() - 1), 2)}
                                     for j in range(J)}
    out['by_income_group'] = byj
    bands = [(21, 34), (35, 49), (50, 64), (65, 100)]
    byage = {}
    for t in [0, 9]:
        w = om[t]
        d = {}
        for lo, hi in bands:
            m = (ages >= lo) & (ages <= hi)
            d['%d-%d' % (lo, hi)] = round(100 * ((w[m] * cr[t, m]).sum() / (w[m] * cb[t, m]).sum() - 1), 2)
        byage['year_%d' % (t + 1)] = d
    out['by_age_consumption_pct'] = byage

    # generations: remaining-lifetime consumption, discounted at 3% a year, along each cohort's path
    def cohort(age0, t0):
        s0 = int(np.argmin(np.abs(ages - age0)))
        res = {}
        tot_b = tot_r = 0.0
        for j in range(J):
            sb = sr = 0.0
            for k in range(S - s0):
                t = t0 + k; s = s0 + k
                if t >= cb.shape[0]:
                    break
                df = 1.03 ** (-k)
                sb += df * cb[t, s, j]; sr += df * cr[t, s, j]
            res[names[j]] = round(100 * (sr / sb - 1), 2)
            lam = float(np.array(pb.lambdas).reshape(-1)[j])
            tot_b += lam * sb; tot_r += lam * sr
        res['all'] = round(100 * (tot_r / tot_b - 1), 2)
        return res
    out['generations_lifetime_consumption_pct'] = {
        'age 65 in Year 1': cohort(65, 0), 'age 45 in Year 1': cohort(45, 0), 'age 25 in Year 1': cohort(25, 0),
        'turns 21 in Year 10': cohort(21, 9), 'turns 21 in Year 20': cohort(21, 19)}
    json.dump(out, open(os.path.join(H, 'results2%s_%s.json' % (SFX, v)), 'w'), indent=1)
    return out


if __name__ == '__main__':
    for v in sys.argv[1:]:
        o = run(v)
        print(v, json.dumps(o['macro'][:5])[:600])
