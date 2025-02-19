# ✂️ CLIPPER: Compression enables long-context synthetic data generation

[![arXiV](https://img.shields.io/badge/arxiv-link-red)](https://arxiv.org/abs/2406.19371) [![Website](https://img.shields.io/badge/website-link-purple)](https://chtmp223.github.io/suri) [![Dataset](https://img.shields.io/badge/dataset-huggingface-yellow)](https://huggingface.co/datasets/chtmp223/suri/) [![Suri-I-ORPO](https://img.shields.io/badge/iorpo-model-green)](https://huggingface.co/chtmp223/suri-i-orpo) [![Suri-SFT](https://img.shields.io/badge/sft-model-blue)](https://huggingface.co/chtmp223/suri-sft)

![Pipeline Overview](assets/img/pipeline.png)

This repository hosts the code and data for our paper, [CLIPPER: Compression enables long-context synthetic data generation](). 

We release ✂️ CLIPPER, a compression-based approach to generating instruction-following data. CLIPPER works by compressing long-form documents (e.g., books) into smaller, information-rich representations (e.g. chapter outlines), which are then used to create grounded instructions for tasks like *narrative claim verification*.

## 📣 Updates
- **[2025-01-20]**: Dataset and models for CLIPPER are now available here: [https://huggingface.co/collections/chtmp223/clipper-67b60b1edbfa3407b571a827](https://huggingface.co/collections/chtmp223/clipper-67b60b1edbfa3407b571a827). 


## 📦 Using CLIPPER
### Getting Started
1. Install the requirements for CLIPPER:
    ```
    conda create -n clipper python=3.10 
    conda activate clipper
    pip install -r requirements.txt
    python -m pip install flash-attn --no-build-isolation
    huggingface-cli login       # Log in to Huggingface using your access token 
    sudo apt-get install git-lfs
    ```
2. Set up Huggingface cache directory:
    - Open your shell configuration file, which is typically `~/.bashrc` or `~/.bash_profile` for Bash, or `~/.zshrc` for Zsh. 
    - Add `HF_HOME` huggingface cache directory path to your configuration file: `HF_HOME=/path/to/huggingface_cache`.
    - Add `HF_TOKEN` huggingface access token to your configuration file: `HF_TOKEN=<your_token>`. 
    - Save and close the file. Source the file to apply the changes: `source ~/.bashrc` or `source ~/.bash_profile` or `source ~/.zshrc`.
    - Double-check that the environment variable is set correctly: `echo $HF_HOME`. 


### Project Structure
```
.
├── README.md
├── assets
│   ├── img
│   └── styles
├── data
├── eval
│   ├── automatic
│   ├── human
│   └── inference
├── ft
│   ├── README.md
│   ├── deepspeed_zero3.yaml
│   ├── i-orpo
│   ├── lib
│   │   ├── alignment_mod
│   │   └── trl_mod
│   └── sft
├── index.html
├── prompts
├── requirements.txt
└── utils.py
```
- `data` contains `b3.py`, which can be used to reconstruct the gold responses of the books3 subset.
- `eval` contains: 
    - `automatic`, which includes code to compute the ranking accuracy metric. 
    - `human`, which includes the XML code for the human evaluation interfaces. 
    - `inference`, which includes code to do inference with the fine-tuned models using either Transformers Huggingface or vLLM.
- `ft` contains code to fine-tune the models using I-ORPO or SFT: 
    - `i-orpo` directory includes `orpo.yaml`, which defines the training hyperparameters; `run_orpo.py`, which contains the training code; and `run_orpo.sh`, which consolidates the training process into a single executable command.
    - `sft` directory includes `sft.yaml`, which defines the training hyperparameters; `run_sft.py`, which contains the training code; and `run_sft.sh`, which consolidates the training process into a single executable command.
    - `deepspeed_zero3.yaml` contains the hyperparameters for deepspeed zero3. 
- `prompts` contains all prompts used in the paper. 


### Dataset and Models
- The dataset is available on Huggingface: [https://huggingface.co/datasets/chtmp223/suri/](https://huggingface.co/datasets/chtmp223/suri/). 

### Finetuning code
- 


## 📜 Citation
```

```