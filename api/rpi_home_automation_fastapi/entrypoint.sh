#!/bin/bash

project_dir=$PWD

echo "Running migrations"
cd ../
alembic upgrade heads

cd $project_dir
echo "Starting server"
python main.py
