#!/bin/bash

curl http://127.0.0.1/api/v1/classification/training/pipeline \
-X POST  \
-H "Content-Type:application/json" \
-d '{
    "pipeline_name": "pipeline-default"
    }'