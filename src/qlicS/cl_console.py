import click
from .pylion import pylion as pl
from .pylion import functions as pl_func

from . import __version__

import time
import os

@click.command()
@click.version_option(version=__version__)
def main():
    """qlicS"""
    
    
    dump_dir = str(os.getcwd())+'/data/'+time.strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(dump_dir)
    os.chdir(dump_dir)

    s = pl.Simulation('test')

    ions = {'mass': 40, 'charge': 1}
    s.append(pl_func.createioncloud(ions, 1e-3, 50))

    trap = {'radius': 3.75e-3, 'length': 2.75e-3, 'kappa': 0.244,
        'frequency': 3.85e6, 'voltage': 500, 'endcapvoltage': 15, 'pseudo':True, 'timestep': 1e-8}
    s.append(pl_func.linearpaultrap(trap, ions=ions))

    s.append(pl_func.langevinbath(0, 1e-5))

    s.append(pl_func.dump('positions.txt', variables=['x', 'y', 'z'], steps=10))
    vavg = pl_func.timeaverage(20, variables=['vx', 'vy', 'vz'])
    s.append(pl_func.dump('secv.txt', vavg, steps=200))

    s.append(pl_func.evolve(1e4))
    s.execute()

