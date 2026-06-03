# Blender and STL Mesh Phantom Pose Library

This repository contains Blender scripts and a generated upper-extremity moving phantom library for GGEMS/Monte Carlo simulation workflows.

## Generated Library

The current generated set contains 120 upper-extremity poses:

- `poses/`: STL mesh files and per-pose bone-center CSV files.
- `numpy_masks_poses/`: NumPy binary masks matching the pose IDs.
- `poses/stl_mapping.csv`: mapping from pose ID to generated pose name.
- `pose_library_manifest.csv`: consolidated metadata for each pose.
- `male_mesh_2025.stl`: reference male phantom STL.

Each pose ID has three matching files:

```text
poses/<pose_id>.stl
poses/<pose_id>.csv
numpy_masks_poses/<pose_id>_mask.npy
```

The pose library currently covers:

- both-arm elevation/inward sweeps
- forearm sweeps with restricted ranges to avoid hand overlap
- right-arm-only poses
- left-arm-only poses
- two-arm poses

## Manifest

`pose_library_manifest.csv` includes:

- `pose_id`
- `pose_name`
- `pose_family`
- `stl_file`
- `bone_coordinates_csv`
- `mask_file`
- `mask_shape`
- `mask_dtype`
- `mask_nonzero_voxels`
- `stl_size_bytes`
- `mask_size_bytes`

The generated masks currently have shape `63x184x85` and dtype `float32`.

## Scripts

- `to_do_script_csv123.py`: Blender pose generation, STL export, and bone-coordinate logging.
- `run_blender_csv123.py`: helper launcher for running the Blender script.
- `coordinates.py`: analytical coordinate plotting/checking for upper-extremity pose ranges.

## Blender Source

The source Blender file used during generation is:

```text
/home/harb/blender/male_mesh_2025_dose.blend
```

The armature is `metarig`. Important pose bones include:

```text
shoulder.L, upper_arm.L, forearm.L, hand.L,
shoulder.R, upper_arm.R, forearm.R, hand.R,
pelvis.L, pelvis.R, thigh.L, shin.L, foot.L, toe.L,
thigh.R, shin.R, foot.R, toe.R,
Lumbar, Thoracic, Cervical
```

## Data Size

The generated STL and NumPy mask library is large:

- `poses/`: about 468 MB
- `numpy_masks_poses/`: about 452 MB

For GitHub, use Git LFS or publish the heavy generated files as a release/data archive. The scripts and manifest are small enough for normal Git.

## Suggested Next Libraries

After the upper-extremity library, the same structure can be extended to:

- walking poses: pelvis, thighs, shins, feet, toes
- sitting poses: pelvis, thighs, shins, feet, lumbar/thoracic
- bending poses: lumbar, thoracic, cervical
- lateral body shift: pelvis and torso rotations/translations
