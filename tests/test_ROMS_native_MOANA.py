import os
import sys
import time
import numpy as np
import matplotlib
from datetime import datetime, timedelta
from opendrift.readers import reader_ROMS_native_MOANA
from opendrift.models.bivalvelarvae import BivalveLarvae


r = reader_ROMS_native_MOANA.Reader('input/nz5km_avg_200601.nc')
o = BivalveLarvae(loglevel=0)
o.add_reader([r])

###############################
#Set Configs
###############################
o.set_config('general:use_auto_landmask', True)
o.set_config('environment:fallback:x_wind', 0.0)
o.set_config('environment:fallback:y_wind', 0.0)
o.set_config('environment:fallback:x_sea_water_velocity', 0.0)
o.set_config('environment:fallback:y_sea_water_velocity', 0.0)
o.set_config('environment:fallback:sea_floor_depth_below_sea_level', 100000.0)

Kxy = 0.1176  #m2/s-1
Kz = 0.01 #m2/s-1

o.set_config('drift:horizontal_diffusivity',Kxy) 
o.set_config('environment:fallback:ocean_vertical_diffusivity', Kz) 
o.set_config('seed:ocean_only',True)
o.set_config('drift:advection_scheme','runge-kutta4')
o.set_config('drift:current_uncertainty', 0.0)
o.set_config('drift:max_age_seconds', 3600*24*35)
o.set_config('drift:min_settlement_age_seconds', 3600*24*21)
o.set_config('general:seafloor_action', 'lift_to_seafloor')
o.set_config('drift:vertical_mixing', False)
o.set_config('general:coastline_action','previous')

o.list_config()

lonmin, lonmax = 170., 180.
latmin, latmax = -50., -45.
npoints = 4
dlon, dlat = (lonmax - lonmin)/float(npoints), (latmax - latmin)/float(npoints)


lons = np.array([lonmin + i*dlon for i in range(npoints)])
lats = np.array([latmin + i*dlat for i in range(npoints)])

nseed = 10
o.seed_within_polygon(lons, lats, time=datetime(year=2006, month=1, day=1), z = -5.)
#o.plot()

o.run(stop_on_error=False,
      end_time=datetime(year=2006, month=1, day=10),
      time_step=900, 
      time_step_output = 86400.0,
      export_variables = [])

#o.animation()