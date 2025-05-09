#!/bin/bash
# init_repo.sh

# Create directories
mkdir -p {.github/workflows,configs,core/{fpga,ai,execution},data/{sample,live},models,tests/{unit,integration}}

# Add sample files
touch configs/{bitget,risk_params}.yaml \
      core/fpga/{hft_kernel.cpp,Makefile} \
      core/ai/{train.py,predict.py} \
      README.md

# Initialize Git
git init
git add .
git commit -m "Initial commit"