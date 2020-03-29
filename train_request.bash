#!/bin/bash

curl http://localhost:5000//api/v1/classification/training/pipeline \
-X POST  \
-H "Content-Type:application/json" \
-d '{
    "pipeline_name": "pipeline-default"
    }'