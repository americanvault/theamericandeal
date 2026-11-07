"""Secs. 2420(b) and 2420(c) estimated from IRS SOI Table 1.4, tax year 2023 (https://www.irs.gov/pub/irs-soi/23in14ar.xls).
Amounts in $ billions. The public CPS file used by Tax-Calculator has no partnership, S-corp or capital-gain income."""
G = 1.25  # growth of these incomes 2023 -> 2028 (about 4.5% a year)
# AGI class: (partnership net income, partnership loss, S-corp net income, S-corp loss, net capital gain, qualified dividends)
SOI = {
 "200K-500K": (70.268, 17.781, 129.920, 10.620, 122.880, 69.612),
 "500K-1M":   (75.603, 12.507, 113.950,  5.704,  97.513, 39.704),
 "1M-1.5M":   (44.441,  7.057,  62.816,  2.764,  54.328, 18.132),
 "1.5M-2M":   (27.276,  5.034,  45.640,  1.717,  36.454, 11.062),
 "2M-5M":     (72.910, 13.981, 121.690,  4.524, 109.230, 28.048),
 "5M-10M":    (40.827,  9.310,  71.565,  2.434,  81.225, 17.343),
 "10M+":      (76.643, 41.366, 157.763, 12.263, 358.365, 66.846)}
# 2420(b): NIIT (3.8%) on active pass-through income not already subject to NIIT or SECA, MAGI above $400K/$500K
share_above = {"200K-500K": 0.15}  # rough share of the $200K-$500K class above the thresholds
part = sum((v[0] - v[1]) * share_above.get(k, 1) for k, v in SOI.items())
scorp = sum((v[2] - v[3]) * share_above.get(k, 1) for k, v in SOI.items())
active_part, active_scorp = 0.35, 0.80   # share not passive and not under SECA (assumption)
b_static = 0.038 * (part * active_part + scorp * active_scorp) * G
b = b_static * 0.90                      # 10% response (reclassification, timing)
# 2420(c): gains and qualified dividends above $1M AGI taxed at 39.6% instead of 20% (+19.6 pts)
top = ["1M-1.5M", "1.5M-2M", "2M-5M", "5M-10M", "10M+"]
qd = sum(SOI[k][5] for k in top); cg = sum(SOI[k][4] for k in top)
div = 0.196 * qd * G * 0.60              # 40% response (payout shifts to buybacks, which Sec. 2420(d) taxes at 4%)
gains = -5.0                             # higher rate without tax at death mostly defers sales; assume small loss
print("2420(b): pass-through base $%.0fB (2023); static $%.1fB, scored $%.1fB a year (2028)" % (part + scorp, b_static, b))
print("2420(c): dividends $%.0fB, gains $%.0fB (2023); dividends +$%.1fB, gains %.1fB -> $%.1fB a year (2028)" % (qd, cg, div, gains, div + gains))
