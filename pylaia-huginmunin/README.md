---
library_name: PyLaia
license: mit
tags:
- PyLaia
- PyTorch
- Handwritten text recognition
metrics:
- CER
- WER
language:
- 'no'
---

# Hugin-Munin handwritten text recognition

This model performs Handwritten Text Recognition in Norwegian. It was developed during the [HUGIN-MUNIN project](https://hugin-munin-project.github.io/).

## Model description

The model has been trained using the PyLaia library on the [NorHand](https://zenodo.org/record/6542056) document images.
Training images were resized with a fixed height of 128 pixels, keeping the original aspect ratio.

## Evaluation results

The model achieves the following results:

| set   | CER (%)    | WER (%)   |
| ----- | ---------- | --------- | 
| train | 2.17       | 7.65     |
| val   | 8.78       | 24.93     |
| test  | 7.94       | 24.04     |


Results improve on validation and test sets when PyLaia is combined with a 6-gram language model. 
The language model is trained on [this text corpus](https://www.nb.no/sprakbanken/en/resource-catalogue/oai-nb-no-sbr-73/) published by the National Library of Norway.

| set   | CER (%)    | WER (%)   |
| ----- | ---------- | --------- | 
| train | 2.40       | 8.10      |
| val   | 7.45       | 19.75     |
| test  | 6.55       | 18.2      |


## How to use

Please refer to the PyLaia [library page](https://pypi.org/project/pylaia/) and [wiki](https://github.com/jpuigcerver/PyLaia/wiki/inference) to use this model.

# Cite us!

```bibtex
@inproceedings{10.1007/978-3-031-06555-2_27,
author = {Maarand, Martin and Beyer, Yngvil and K\r{a}sen, Andre and Fosseide, Knut T. and Kermorvant, Christopher},
title = {A Comprehensive Comparison of Open-Source Libraries for Handwritten Text Recognition in Norwegian},
year = {2022},
isbn = {978-3-031-06554-5},
publisher = {Springer-Verlag},
address = {Berlin, Heidelberg},
url = {https://doi.org/10.1007/978-3-031-06555-2_27},
doi = {10.1007/978-3-031-06555-2_27},
booktitle = {Document Analysis Systems: 15th IAPR International Workshop, DAS 2022, La Rochelle, France, May 22–25, 2022, Proceedings},
pages = {399–413},
numpages = {15},
keywords = {Norwegian language, Open-source, Handwriting recognition},
location = {La Rochelle, France}
}
```