
from clawpack.clawutil.data import get_remote_file

url = 'https://depts.washington.edu/clawpack/geoclaw/topo/etopo/' \
        + 'etopo1min130E210E0N60N.asc'
get_remote_file(url, output_dir='.', verbose=True)

url = 'https://depts.washington.edu/clawpack/geoclaw/topo/hawaii/' \
        + 'kahului_1s.txt'
get_remote_file(url, output_dir='.', verbose=True)
