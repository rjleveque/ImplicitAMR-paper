
from clawpack.clawutil.data import get_remote_file

url = 'https://raw.githubusercontent.com/rjleveque/tohoku2011-paper1/master/sources/Fujii.txydz'
get_remote_file(url, output_dir='.', verbose=True)

url = 'https://raw.githubusercontent.com/rjleveque/tohoku2011-paper1/master/sources/UCSB3.txydz'
get_remote_file(url, output_dir='.', verbose=True)

