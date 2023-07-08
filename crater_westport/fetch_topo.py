
from clawpack.clawutil.data import get_remote_file

url = 'https://depts.washington.edu/clawpack/geoclaw/topo/etopo/' \
        + 'etopo1_-137_-122_38_51_1min.asc'
get_remote_file(url, output_dir='.', verbose=True)

url = 'https://depts.washington.edu/clawpack/geoclaw/topo/WA/' \
        + 'grays_harbor_mhw_1sec.asc'
get_remote_file(url, output_dir='.', verbose=True)
