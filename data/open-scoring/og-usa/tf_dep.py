import sys, os, json, pickle, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_nsra import tax_funcs, IIT_REFORM, DEF, OUT
from ogcore.parameters import Specifications
import ogusa.get_micro_data as GMD
_orig = GMD.get_data
def _one_year(**kw):
    md, v = _orig(**kw)
    # time-invariant tax functions: estimate once on 2028 data (first year the reform is in effect)
    return {str(kw['start_year']): md['2028']}, v
GMD.get_data = _one_year
def main():
    ty = sys.argv[1]
    p = Specifications(baseline=True, num_workers=2, output_base=os.path.join(OUT, 'tfdir_' + ty))
    p.update_specifications({k: v for k, v in DEF.items() if k != 'BW'})
    p.update_specifications({'tax_func_type': ty})
    print(time.strftime('%H:%M:%S'), 'base', ty, flush=True)
    tb = tax_funcs(p, {}); tb['tax_func_type'] = ty
    pickle.dump(tb, open(os.path.join(OUT, 'tf_base_%s.pkl' % ty), 'wb'))
    print(time.strftime('%H:%M:%S'), 'reform', ty, flush=True)
    tr = tax_funcs(p, IIT_REFORM); tr['tax_func_type'] = ty
    pickle.dump(tr, open(os.path.join(OUT, 'tf_ref_%s.pkl' % ty), 'wb'))
    print(time.strftime('%H:%M:%S'), 'done', flush=True)

if __name__ == '__main__':
    main()
