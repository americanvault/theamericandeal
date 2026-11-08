import pickle, json, numpy as np, os
H = os.path.dirname(os.path.abspath(__file__))
b = pickle.load(open(os.path.join(H, 'out/baseline/TPI/TPI_vars.pkl'), 'rb'))
import sys
RD = sys.argv[1] if len(sys.argv) > 1 else 'reform'
r = pickle.load(open(os.path.join(H, 'out', RD, 'TPI', 'TPI_vars.pkl'), 'rb'))
# CBO Feb 2026 baseline nominal GDP, FY2028-2037 ($B), as used in the NSRA model
GDP = [34300, 35700, 37100, 38600, 40100, 41700, 43400, 45100, 46900, 48800]
EMP = 166.0  # million payroll + self-employed workers, approx. 2028 (CBO/BLS)
def pct(k, t):
    return 100 * (np.array(r[k])[t] / np.array(b[k])[t] - 1)
rows = []
for t in [0, 1, 2, 4, 9, 19, 29]:
    row = {'year': t + 1}
    for k in ['Y', 'C', 'I', 'K', 'L', 'w', 'r']:
        row[k] = round(float(pct(k, t)), 2) if k != 'r' else round(100 * float(np.array(r['r'])[t] - np.array(b['r'])[t]), 3)
    row['debt_to_gdp_pts'] = round(100 * float(np.array(r['D'])[t] / np.array(r['Y'])[t] - np.array(b['D'])[t] / np.array(b['Y'])[t]), 1)
    row['revenue_pct_gdp_pts'] = round(100 * float(np.array(r['total_tax_revenue'])[t] / np.array(r['Y'])[t] - np.array(b['total_tax_revenue'])[t] / np.array(b['Y'])[t]), 2)
    row['transfers_pct_gdp_pts'] = round(100 * float(np.array(r['TR'])[t] / np.array(r['Y'])[t] - np.array(b['TR'])[t] / np.array(b['Y'])[t]), 2)
    row['G_pct_gdp_pts'] = round(100 * float(np.array(r['G'])[t] / np.array(r['Y'])[t] - np.array(b['G'])[t] / np.array(b['Y'])[t]), 2)
    if t < 10:
        row['gdp_change_billion'] = round(GDP[t] * row['Y'] / 100)
    row['fte_jobs_thousand'] = round(EMP * 1000 * row['L'] / 100)
    rows.append(row)
avg10 = float(np.mean([pct('Y', t) for t in range(10)]))
out = {'rows': rows, 'avg_gdp_pct_years_1_10': round(avg10, 2),
       'cum_gdp_change_10yr_billion': round(sum(GDP[t] * pct('Y', t) / 100 for t in range(10)))}
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(H, 'results_%s.json' % RD), 'w'), indent=1)
