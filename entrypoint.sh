#!/bin/bash
source /opt/conda/etc/profile.d/conda.sh
conda activate nlp_project
cd app
python -u grpc_server.py