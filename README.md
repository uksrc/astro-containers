# astro-containers

Apptainer/Singularity definition files for radio astronomy software images published to `harbor.ral.uksrc.org` (project: `radio-astro-software`). Each subdirectory contains a single `.def` file for the named application/version.

## Contents
- `aegean/aegean-v2.3.5.def` – Aegean radio source finding stack.
- `casacore/casacore-v3.7.1.def` – Casacore libraries built from source.
- `casa-modular/casa-modular-v6.7.0.def` – CASA 6 modular build (pip-based).
- `casa-standalone/casa-standalone-v6.7.2.def` – CASA 6.7.2 standalone bundle with bundled GUIs unpacked.
- `miriad/miriad-v2025.10.14.def` – MIRIAD prebuilt binaries with environment setup.
- `pybdsf/pybdsf-v1.13.0.def` – PyBDSF source finder.
- `sofia/sofia-v2.6.43.def` – SoFiA-2 line/source finder.
- `tricolour/tricolour-v0.8.1.2.def` – Tricolour flagging/calibration tools.
- `wsclean/wsclean-v3.6.def` – WSClean + EveryBeam + IDG stack.

## Build locally
```bash
# With fakeroot (preferred on shared systems)
apptainer build --fakeroot miriad-v2025.10.14.sif miriad/miriad-v2025.10.14.def

# With sudo if fakeroot is unavailable
sudo apptainer build miriad-v2025.10.14.sif miriad/miriad-v2025.10.14.def
```

## Run/test an image
```bash
apptainer exec miriad-v2025.10.14.sif miriad help
apptainer shell miriad-v2025.10.14.sif
```

## Push/pull from Harbor (oras)
```bash
# Push a built image
apptainer push miriad-v2025.10.14.sif \
  oras://harbor.ral.uksrc.org/radio-astro-software/miriad:v2025.10.14

# Pull a published image
apptainer pull oras://harbor.ral.uksrc.org/radio-astro-software/miriad:v2025.10.14
```
Authenticate with your Harbor robot account or token if required (`APPTAINER_DOCKER_USERNAME`/`APPTAINER_DOCKER_PASSWORD` or `--oci-authfile` or pass `--docker-password` and `--docker-username`).

## Updating/adding images
1) Edit or add the relevant `.def` file.
2) Build and test the `.sif`.
3) Push to Harbor with a versioned tag.
4) Update this README if a new image or version is added.
