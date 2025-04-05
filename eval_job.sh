#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --time=0:40:00
#SBATCH --job-name="model evaluation"
#SBATCH --mem-per-cpu=2048
#SBATCH --output="./evals/datasets/frames_test_set.csv"
#SBATCH --open-mode=append

 python ./evals/eval_tasks.py --parallel-workers=48 --num-trials=1 --eval-tasks=./evals/datasets/frames_test_set.csv