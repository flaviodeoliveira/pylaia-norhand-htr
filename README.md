# pylaia-norhand-htr
Use of PyLaia library and NorHand Dataset for handwritten text recognition (HTR).

[PyLaia](https://github.com/jpuigcerver/PyLaia) is a device agnostic, PyTorch-based, deep learning toolkit for handwritten document analysis. This particular model was trained using PyLaia library on Norwegian historical documents ([NorHand Dataset](https://zenodo.org/record/6542056)) during the [HUGIN-MUNIN project](https://hugin-munin-project.github.io) for handwritten text recognition.

* HF `model card`: [Teklia/pylaia-huginmunin](https://huggingface.co/Teklia/pylaia-huginmunin) | [A Comprehensive Comparison of Open-Source Libraries for Handwritten Text Recognition in Norwegian](https://doi.org/10.1007/978-3-031-06555-2_27)

## Create an environment
    conda create -n pylaia-norhand-htr python=3.8

## Install the requirements
    conda activate pylaia-norhand-htr
    pip install -r requirements.txt

## Run
    python app.py