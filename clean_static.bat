@echo off

cd frontend/public/static
rd /S/Q manifests paths projects
del *.json *.list
cd ../../..
