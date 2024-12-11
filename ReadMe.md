# Handwriting Synthesis Project

## Prerequisites

- Python 3.8+
- Anaconda or Miniconda

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/rudyoactiv/handwriting-synthesis.git
cd handwriting-synthesis
```

### 2. Create the Conda environment from `environment.yml`

The project dependencies are specified in the `environment.yml` file. To set up the environment, run the following command:

```bash
conda env create -f environment.yml
```

This will create a new environment with all the required dependencies installed.

### 3. Activate the environment

Once the environment is created, activate it with the following command:

```bash
conda activate test_hand
```

This will activate the `test_hand` environment, where the project dependencies are installed.

### 4. Run the `gui.py` script

To start the application, run the `gui.py` script using the Python executable from the activated environment:

```bash
python "path/to/handwriting-synthesis/gui.py"
```

This will launch the GUI, where you can input text and generate handwriting-style SVG files.

### 5. Deactivating the environment

Once you're done using the environment, deactivate it with the following command:

```bash
conda deactivate
```

---

## Dependencies

The following dependencies are included in the `environment.yml`:

- `CairoSVG==2.7.1`
- `matplotlib==3.7.5`
- `numpy==1.23.5`
- `pandas==2.0.3`
- `scikit_learn==1.3.2`
- `scipy==1.10.1`
- `svgwrite==1.4.3`
- `tensorflow==2.12.0`
- `tensorflow_intel==2.12.0`
- `tensorflow_probability==0.20.1`

---
