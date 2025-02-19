#!/bin/bash
#SBATCH --job-name=pipeline_wp
#SBATCH --partition=cpu-preempt
#SBATCH --nodes=1
#SBATCH --mem=80G
#SBATCH --time=48:00:00
#SBATCH --mail-type=ALL

conda activate clipper

echo "===> Constructing WritingPrompts dataset"
python3 wp.py