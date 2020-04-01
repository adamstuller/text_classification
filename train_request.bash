#!/bin/bash

curl localhost:5000/api/v1/classification/training/pipeline/pepco \
-X POST  \
-H "Content-Type:application/json" \
-d '{
    "pipeline_name": "pipeline-default"
    }'