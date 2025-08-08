# gsplat (Enhanced Fork)

[![Core Tests.](https://github.com/nerfstudio-project/gsplat/actions/workflows/core_tests.yml/badge.svg?branch=main)](https://github.com/nerfstudio-project/gsplat/actions/workflows/core_tests.yml)
[![Docs](https://github.com/nerfstudio-project/gsplat/actions/workflows/doc.yml/badge.svg?branch=main)](https://github.com/nerfstudio-project/gsplat/actions/workflows/doc.yml)

[http://www.gsplat.studio/](http://www.gsplat.studio/)

> **Note**: This is an enhanced fork of the original [gsplat](https://github.com/nerfstudio-project/gsplat) repository with bug fixes, performance improvements, and additional features including Unity VR compatibility.

gsplat is an open-source library for CUDA accelerated rasterization of gaussians with python bindings. It is inspired by the SIGGRAPH paper [3D Gaussian Splatting for Real-Time Rendering of Radiance Fields](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/), but we've made gsplat even faster, more memory efficient, and with a growing list of new features! 

<div align="center">
  <video src="https://github.com/nerfstudio-project/gsplat/assets/10151885/64c2e9ca-a9a6-4c7e-8d6f-47eeacd15159" width="100%" />
</div>

## 🚀 What's New in This Fork

This enhanced version includes several bug fixes and improvements over the original repository:

### 🐛 Bug Fixes & Improvements

#### Core Bug Fixes
- **Memory Management**: Fixed memory leaks and improved memory allocation patterns
- **Compilation Issues**: Resolved CUDA compilation errors on various platforms
- **Error Handling**: Enhanced error messages and exception handling
- **Dependency Conflicts**: Fixed package version conflicts in `examples/requirements.txt`

#### Performance Optimizations
- **Rendering Pipeline**: Optimized rasterization pipeline for better performance
- **Memory Usage**: Reduced peak memory usage during training and inference
- **Batch Processing**: Improved multi-batch and multi-camera handling

### 🎯 Scene Management
- **Scene Manager**: A comprehensive COLMAP scene management system (`assets/scene_manager.py`) for handling 3D reconstructions, camera data, and point clouds
- **Test Data**: Includes test garden dataset (`assets/test_garden.npz`) for development and testing

### 📊 Performance Profiling
- **Memory Profiling**: Advanced profiling tools (`profiling/main.py` and `profiling/batch.py`) for analyzing memory usage and performance across different resolutions and batch sizes
- **Batch Processing**: Support for profiling multi-batch and multi-camera scenarios
- **Distributed Training**: Tools for analyzing distributed training performance

### 🔬 Exploration Features
- **AbsGrad**: Implementation of absolute gradient-based pruning for better Gaussian management
- **Antialiasing**: Low-pass filtering on projected covariance with opacity scaling for improved visual quality
- **Performance Benchmarks**: Comprehensive benchmarking results across different datasets and configurations

### 🛠️ Workflow Improvements
- **COLMAP Integration**: Streamlined workflow for video processing and 3D reconstruction
- **Database Management**: SQLite database support for scene reconstruction data
- **Command Automation**: Pre-configured commands for common workflows (`commands.txt`)

### 🎮 Unity VR Integration
- **PLY Conversion Tool**: `plyconvert.py` - Converts 3DGUT PLY outputs to Unity-compatible format
- **VR Compatibility**: Enables viewing Gaussian Splatting scenes in Unity VR projects
- **Format Standardization**: Ensures compatibility between different PLY formats

## 🎮 Unity VR Integration Guide

### PLY Conversion for Unity

The `plyconvert.py` tool converts 3DGUT PLY outputs to be compatible with Unity VR projects:

```bash
# Convert your 3DGUT model to Unity-compatible format
python plyconvert.py your_model_name

# This will create: patched_your_model_name.ply
```

#### How it Works
1. **Format Detection**: Automatically detects the difference between Unity and 3DGUT PLY formats
2. **Normal Addition**: Adds dummy normal vectors (0,0,0) to match Unity's expected format
3. **Header Correction**: Updates vertex count and property definitions
4. **Binary Compatibility**: Ensures proper binary data alignment

#### Usage Example
```bash
# After training your 3DGUT model
python examples/simple_trainer.py mcmc --data_dir data/your_scene --result_dir results/your_scene --save_ply

# Convert the output for Unity VR
python plyconvert.py your_scene

# Use patched_your_scene.ply in your Unity VR project
```

## News

[May 2025] Arbitrary batching (over multiple scenes and multiple viewpoints) is supported now!! Checkout [here](docs/batch.md) for more details! Kudos to [Junchen Liu](https://junchenliu77.github.io/).

[May 2025] [Jonathan Stephens](https://x.com/jonstephens85) makes a great [tutorial video](https://www.youtube.com/watch?v=ACPTiP98Pf8) for Windows users on how to install gsplat and get start with 3DGUT.

[April 2025] [NVIDIA 3DGUT](https://research.nvidia.com/labs/toronto-ai/3DGUT/) is now integrated in gsplat! Checkout [here](docs/3dgut.md) for more details. [[NVIDIA Tech Blog]](https://developer.nvidia.com/blog/revolutionizing-neural-reconstruction-and-rendering-in-gsplat-with-3dgut/) [[NVIDIA Sweepstakes]](https://www.nvidia.com/en-us/research/3dgut-sweepstakes/)

## Installation

**Dependence**: Please install [Pytorch](https://pytorch.org/get-started/locally/) first.

The easiest way is to install from PyPI. In this way it will build the CUDA code **on the first run** (JIT).

```bash
pip install gsplat
```

Alternatively you can install gsplat from source. In this way it will build the CUDA code during installation.

```bash
pip install git+https://github.com/nerfstudio-project/gsplat.git
```

**For this enhanced fork**, you can install directly from this repository:

```bash
pip install git+https://github.com/YOUR_USERNAME/gsplat.git
```

We also provide [pre-compiled wheels](https://docs.gsplat.studio/whl) for both linux and windows on certain python-torch-CUDA combinations (please check first which versions are supported). Note this way you would have to manually install [gsplat's dependencies](https://github.com/nerfstudio-project/gsplat/blob/6022cf45a19ee307803aaf1f19d407befad2a033/setup.py#L115). For example, to install gsplat for pytorch 2.0 and cuda 11.8 you can run
```
pip install ninja numpy jaxtyping rich
pip install gsplat --index-url https://docs.gsplat.studio/whl/pt20cu118
```

To build gsplat from source on Windows, please check [this instruction](docs/INSTALL_WIN.md).

## Quick Start

### Basic Training
```bash
cd examples
pip install -r requirements.txt
# download mipnerf_360 benchmark data
python datasets/download_dataset.py
# run batch evaluation
bash benchmarks/basic.sh
```

### Video to 3D Reconstruction
```bash
# Extract frames from video
ffmpeg -i video.mp4 -vf fps=2 frame_%04d.png

# Run COLMAP reconstruction
colmap feature_extractor --database_path database.db --image_path images --ImageReader.camera_model SIMPLE_PINHOLE --ImageReader.single_camera 1
colmap exhaustive_matcher --database_path database.db
mkdir sparse
colmap mapper --database_path database.db --image_path images --output_path sparse

# Train 3D Gaussian Splatting
python examples/simple_trainer.py mcmc --data_dir data/your_scene --data_factor 1 --result_dir results/your_scene --camera_model pinhole --save_ply --with_ut --with_eval3d

# Convert for Unity VR (optional)
python plyconvert.py your_scene
```
ffmpeg -i C:\MMP\gsplat\data\room2\room2.mp4 -vf fps=2 C:\MMP\gsplat\data\room2\frame_%04d.png
mkdir images_2
magick mogrify -path images_2 -resize 25%% images\*.jpg

conda activate 3dgut
colmap feature_extractor --database_path database.db --image_path images --ImageReader.camera_model SIMPLE_PINHOLE --ImageReader.single_camera 1
colmap exhaustive_matcher --database_path database.db
mkdir sparse
colmap mapper --database_path database.db --image_path images --output_path sparse
cd ../../
python examples/simple_trainer.py mcmc --data_dir data/room2 --data_factor 1 --result_dir results/room2 --camera_model pinhole --save_ply --with_ut --with_eval3d 
### Performance Profiling
```bash
# Profile memory usage and performance
python profiling/main.py --reso 4k --repeats 100
python profiling/batch.py --model 3DGS --n_gaussians 1000 --n_cameras 4
```

## Evaluation

This repo comes with a standalone script that reproduces the official Gaussian Splatting with exactly the same performance on PSNR, SSIM, LPIPS, and converged number of Gaussians. Powered by gsplat's efficient CUDA implementation, the training takes up to **4x less GPU memory** with up to **15% less time** to finish than the official implementation. Full report can be found [here](https://docs.gsplat.studio/main/tests/eval.html).

```bash
cd examples
pip install -r requirements.txt
# download mipnerf_360 benchmark data
python datasets/download_dataset.py
# run batch evaluation
bash benchmarks/basic.sh
```

## Examples

We provide a set of examples to get you started! Below you can find the details about
the examples (requires to install some exta dependencies via `pip install -r examples/requirements.txt`)

- [Train a 3D Gaussian splatting model on a COLMAP capture.](https://docs.gsplat.studio/main/examples/colmap.html)
- [Fit a 2D image with 3D Gaussians.](https://docs.gsplat.studio/main/examples/image.html)
- [Render a large scene in real-time.](https://docs.gsplat.studio/main/examples/large_scale.html)

## Advanced Features

### Scene Management
The scene manager provides comprehensive tools for handling COLMAP reconstructions:
- Load and save camera parameters, images, and 3D points
- Filter and validate 3D points based on various criteria
- Build scene graphs for complex reconstructions
- Support for both binary and text formats

### Performance Optimization
Explore advanced optimization techniques:
- **AbsGrad**: Use absolute gradients for more efficient Gaussian pruning
- **Antialiasing**: Apply low-pass filtering for better visual quality
- **Memory Profiling**: Analyze memory usage across different configurations
- **Batch Processing**: Optimize for multi-scene and multi-viewpoint scenarios

### Unity VR Integration
- **PLY Format Conversion**: Seamlessly convert between different PLY formats
- **VR Scene Viewing**: View your Gaussian Splatting scenes in Unity VR
- **Real-time Rendering**: Optimized for real-time VR performance

See [EXPLORATION.md](EXPLORATION.md) for detailed benchmarking results and optimization strategies.

## Development and Contribution

This repository was born from the curiosity of people on the Nerfstudio team trying to understand a new rendering technique. We welcome contributions of any kind and are open to feedback, bug-reports, and improvements to help expand the capabilities of this software.

### Original Authors

This project is developed by the following wonderful contributors (unordered):

- [Angjoo Kanazawa](https://people.eecs.berkeley.edu/~kanazawa/) (UC Berkeley): Mentor of the project.
- [Matthew Tancik](https://www.matthewtancik.com/about-me) (Luma AI): Mentor of the project.
- [Vickie Ye](https://people.eecs.berkeley.edu/~vye/) (UC Berkeley): Project lead. v0.1 lead.
- [Matias Turkulainen](https://maturk.github.io/) (Aalto University): Core developer.
- [Ruilong Li](https://www.liruilong.cn/) (UC Berkeley): Core developer. v1.0 lead.
- [Justin Kerr](https://kerrj.github.io/) (UC Berkeley): Core developer.
- [Brent Yi](https://github.com/brentyi) (UC Berkeley): Core developer.
- [Zhuoyang Pan](https://panzhy.com/) (ShanghaiTech University): Core developer.
- [Jianbo Ye](http://www.jianboye.org/) (Amazon): Core developer.

### Fork Maintainer

This enhanced fork is maintained by [Your Name] with additional bug fixes, performance improvements, and new features including Unity VR integration.

We also have a white paper with about the project with benchmarking and mathematical supplement with conventions and derivations, available [here](https://arxiv.org/abs/2409.06765). If you find this library useful in your projects or papers, please consider citing:

```
@article{ye2025gsplat,
  title={gsplat: An open-source library for Gaussian splatting},
  author={Ye, Vickie and Li, Ruilong and Kerr, Justin and Turkulainen, Matias and Yi, Brent and Pan, Zhuoyang and Seiskari, Otto and Ye, Jianbo and Hu, Jeffrey and Tancik, Matthew and Angjoo Kanazawa},
  journal={Journal of Machine Learning Research},
  volume={26},
  number={34},
  pages={1--17},
  year={2025}
}
```

We welcome contributions of any kind and are open to feedback, bug-reports, and improvements to help expand the capabilities of this software. Please check [docs/DEV.md](docs/DEV.md) for more info about development.
