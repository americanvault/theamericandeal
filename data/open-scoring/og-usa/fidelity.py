"""Static revenue implied by fitted tax functions vs. Tax-Calculator, at 2028 incomes."""
import pickle, sys, numpy as np, os
from ogcore import txfunc
H = os.path.dirname(os.path.abspath(__file__))
md = pickle.load(open(os.path.join(H, 'out/baseline/micro_data_baseline.pkl'), 'rb'))['2028']
def total(tf, ty, yidx):
    tot = 0.0
    for s, age in enumerate(range(21, 101)):
        d = md[md['age'] == min(age, 80)] if age > 80 else md[md['age'] == age]
        if age > 80: continue
        X = d['total_labinc'].values; Y = d['total_capinc'].values; w = d['weight'].values
        prm = tf['etr_params'][yidx][s]
        etr = txfunc.get_tax_rates(prm, X, Y, None, ty, 'etr', for_estimation=False)
        m = np.isfinite(etr) & ((X + Y) > 0); tot += np.sum((w * etr * (X + Y))[m])
    return tot
ty = sys.argv[1]; sfx = '' if ty == 'HSV' else '_' + ty
tb = pickle.load(open(os.path.join(H, 'out/tf_base%s.pkl' % sfx), 'rb'))
tr = pickle.load(open(os.path.join(H, 'out/tf_ref%s.pkl' % sfx), 'rb'))
yi = 2 if ty == 'HSV' else 0
true_b = float((md['total_tax_liab'] * md['weight']).sum())
b = total(tb, ty, yi); r = total(tr, ty, yi)
print(ty, 'model base tax $B %.0f (micro truth %.0f), model reform change $B %.1f' % (b / 1e9, true_b / 1e9, (r - b) / 1e9))
