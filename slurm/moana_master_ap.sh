#!/bin/bash -e

#SBATCH --account=nesi99999                   #Type the project code you want to use for this analyis		 $
#SBATCH --job-name=TAS          #This willl be the name appear on the queue			 $
#SBATCH --mem=20G                               #Amount of memory you need                                       $
#SBATCH --cpus-per-task=1                       #Amount of CPUs (logical)                                        $
#SBATCH --hint=multithread
#SBATCH --time=04:00:00                         #Duration dd-hh:mm:ss                                            $
##SBATCH --profile=task

#SBATCH --export NONE

export SLURM_EXPORT_ENV=ALL

#purging any modules/software loaded in the background prior to submitting script
module purge

#Load the required module for analysis/simulation
module load Anaconda3
source activate opendrift_simon

#Set variables
inPath='/nesi/nobackup/mocean02574/NZB_N50/'
topdir='/home/pletzera/opendriftxmoana-calquigs/'
outPath="$topdir/output/"
name='TAS' 
lon=173.1
lat=-41.2

#run jobs
#python -m cProfile -o output.pstats /nesi/project/vuw03073/opendriftxmoana/scripts/moana_master.py -i $inPath -o $outPath -n $name -ym ${ym[$SLURM_ARRAY_TASK_ID]} -lon $lon -lat $lat
srun python $topdir/scripts/moana_master.py -i $inPath -o $outPath -n $name -ym 200107 -lon $lon -lat $lat


