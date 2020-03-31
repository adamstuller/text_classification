#!/bin/bash

curl ec2-3-125-39-228.eu-central-1.compute.amazonaws.com/api/v1/classification/training/pipeline \
-X POST  \
-H "Content-Type:application/json" \
-d '{
    "pipeline_name": "pipeline-default"
    }'