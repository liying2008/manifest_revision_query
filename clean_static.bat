@echo off

cd frontend/static
rd /S/Q manifests paths projects
del *.json *.list
cd ../..
