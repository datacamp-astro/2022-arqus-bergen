# The data repository 
To carry on the hands-on of this school we have selected a set of available real data from actual experiments in the field. Some of these data are publicly 
availble, some other are proprietary of the collaborations, so please do not share.

## Instruments
We have selected data from the following instruments:
* MAGIC (Major Atmospheric Gamma-ray Imaging Cherenkov) telescopes are a pair of 17 m class telescopes located in the Roque de Los Muchachos Observatory (ORM), La Palma, Spain www.magic.mpp.mpg.de. MAGIC is sensitive in the range 30 GeV - 100 TeV
* H.E.S.S. (High Energy Stereoscopic System) is an array of 4 12m class telescopes and 1 28m class telescope located in Namibia https://www.mpi-hd.mpg.de/hfm/HESS/. H.E.S.S. is sensitive in the range 50 GeV - 200 TeV 
* VERITAS is a set of 4 12m class telescopes located in Arizona, US. VERITAS is sensitive in the range 200 GeV - 100 GeV https://veritas.sao.arizona.edu/
* Fermi-LAT (Large Area Telescope) is a satellite born detector sensitive in the range 0.5-300 GeV. https://fermi.gsfc.nasa.gov/

Other minor:
* FACT is a single dish telescope, 4m class also, fully robotic, also located at ORM https://www.isdc.unige.ch/fact/. FACT is sensitive in the range 10-100 TeV

## Targets
We have selected different astrophysical targets:
* Crab Nebula. It is a galactic object, of the class of Pulsar Wind Nebulae. It is the brightest GeV and TeV emitter in the sky
* NGC1275 is an Active Galactic Nuclei hosted in the center of the Perseus Galaxy Cluster
* IC310 is the second most bright AGN hosted in the Perseus Galaxy Clusters
* PKS2155+504 is an Active Galactic Nuclei of the Blazar class 


## How to download the data
Data are stored locally at INFN servers. To download data, open a terminal and run
```
./download_data.sh
```

The full dataset occupies only 18 MB of data at the moment, so no special storage requirements are needed. The file `arqus_filelist.txt` also displays the structure of the data folder.
