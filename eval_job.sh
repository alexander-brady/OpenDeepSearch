#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --time=0:50:00
#SBATCH --job-name="model evaluation"
#SBATCH --output=/OpenDeepSearch/sbatch.out
#SBATCH --mem-per-cpu=2048

python  $HOME/OpenDeepSearch/evals/eval_tasks.py --parallel-workers=48 --num-trials=1 --eval-tasks=$HOME/OpenDeepSearch/evals/datasets/frames_test_set.csv