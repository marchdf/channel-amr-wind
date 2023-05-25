python plotter.py -f smag_0 smag_1 smag_2 -n 50 -l 'z_ref = first cell' 'z_ref = second cell' 'z_ref = third cell'  -p smag_zref.pdf
python plotter.py -f smag_2 smag_2_bds 'smag_2_cfl0.5' -l 'weno-z (cfl 0.95)' 'bds' 'weno-z (cfl 0.5)'  -n 50 -p smag_weno_bds.pdf
python plotter.py -f smag_0 no_sgs_weno no_sgs_bds -l 'Smag (first cell)' 'No SGS (weno)' 'No SGS (bds)'  -n 50 -p smag_vs_nosgs.pdf
python plotter.py -f smag_2 no_sgs_weno2 no_sgs_bds2 -l 'Smag (thrid cell)' 'No SGS (weno, third cell)' 'No SGS (bds, third cell)'  -n 50 -p smag_vs_nosgs_zref.pdf
