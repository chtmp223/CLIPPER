#!/bin/bash
#SBATCH --job-name=pipeline
#SBATCH --partition=cpu-preempt
#SBATCH --nodes=1
#SBATCH --mem=80G
#SBATCH --time=48:00:00
#SBATCH --open-mode=truncate
#SBATCH --mail-type=ALL

conda activate clipper

echo "===> Extracting summaries"
python3 summary.py --batch batch

echo "===> Running outline extraction"
python3 pipeline.py