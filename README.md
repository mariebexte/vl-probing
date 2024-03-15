# Visio-Linguistic Probing

This repository contains the Rainbow (to appear at EACL 2024) and EViL-Probe (to appear at LREC-COLING 2024) visio-lingusitic probing benchmarks.
It provides the code to derive the respective benchmark from the existing datasets.

Source datasets have to be placed into the respective directories as detailed below:

| subdir of ```source_datasets```       | files           | corresponding images found here  |
| ------------- |-------------| -----|
| ```/ARO```   | from [ARO](https://github.com/mertyg/vision-language-models-are-bows/blob/main/README.md): ```visual_genome_attribution.json``` (generated using VG_Attribution(image_preprocess=preprocess, download=True, root_dir=root_dir), as described in the repo) and ```visual_genome_relation.json``` (generated using VG_Relation(image_preprocess=preprocess, download=True, root_dir=root_dir, as described in the repo ) | uses [Flickr30k](https://forms.illinois.edu/sec/229675) and [MS COCO](https://cocodataset.org/#download) images |
| ```/Compositional-Visual-Genome```  | [ComVG.csv](https://github.com/eric-ai-lab/ComCLIP/blob/main/datasets/ComVG.csv) | uses [VisualGenome](https://homes.cs.washington.edu/~ranjay/visualgenome/api.html) images |
| ```/Counting-Probe``` | git clone [Counting Probe](https://github.com/Heidelberg-NLP/counting-probe) | [linked](http://vision.stanford.edu/yukezhu/visual7w_images.zip) in the Counting Probe repo |
| ```/EqBen``` | [this file](https://drive.google.com/file/d/1-CWEuZ5F0KQ4d94Y9rRtBsMIcqb8V7nm/view) linked in the [EqBen Repository](https://github.com/Wangt-CN/EqBen?tab=readme-ov-file#eqben-1) | [linked](https://drive.google.com/file/d/1e608uhd36ak_v7SnlMVaYcekBc4gBqzn/view?usp=drive_link) in the EqBen repo
| ```/Flickr30k``` | ```dataset_flickr30k.json``` as linked [here](http://cs.stanford.edu/people/karpathy/deepimagesent/caption_datasets.zip) by [this](https://github.com/jiasenlu/NeuralBabyTalk/blob/master/data/README.md) repository | sign up [here](https://forms.illinois.edu/sec/229675)
| ```/FOIL-IT``` | ```foilv1.0_test_2017.json``` as linked [here](https://www.dropbox.com/s/u4ntgo73szg6yai/foilv1.0_test_2017.json) from the [FOIL-IT page](https://foilunitn.github.io)| uses [MS COCO](https://cocodataset.org/#download) images
| ```/High-level``` | ```test.jsonl``` from [here](https://github.com/michelecafagna26/HL-dataset/tree/main/annotations) | [here](https://huggingface.co/datasets/michelecafagna26/hl/resolve/main/data/images.tar.gz)
| ```/MS_COCO``` | ```dataset_coco.json``` as linked [here](http://cs.stanford.edu/people/karpathy/deepimagesent/caption_datasets.zip) by [this](https://github.com/jiasenlu/NeuralBabyTalk/blob/master/data/README.md) repository | [here](https://cocodataset.org/#download)
| ```/Predicate-Noun``` | [eval_set.json](https://github.com/mitjanikolaus/multimodal-predicate-noun-dependencies/blob/main/data/sentence-semantics/eval_set.json) | uses images from [OpenImages](https://storage.googleapis.com/openimages/web/index.html)
| ```/SVO-Probes```| [svo_probes.csv](https://github.com/google-deepmind/svo_probes/blob/main/svo_probes.csv) | image urls are linked in [svo_probes.csv](https://github.com/google-deepmind/svo_probes/blob/main/svo_probes.csv), uncomment line 180 of ```evil-probe/prepare_SVO_probes.py``` to download
| ```/VALSE```| all of [these](https://github.com/Heidelberg-NLP/VALSE/tree/main/data) files | uses SWiG,
| ```/Visual-Spatial-Reasoning```| [all_vsr_validated_data.jsonl](https://github.com/cambridgeltl/visual-spatial-reasoning/blob/master/data/data_files/all_vsr_validated_data.jsonl) | uses [MS COCO](https://cocodataset.org/#download) images
| ```/VL-Checklist```| [these](https://github.com/om-ai-lab/VL-CheckList/tree/main/data) subdirs | uses [VisualGenome](https://homes.cs.washington.edu/~ranjay/visualgenome/api.html), 
| ```/Why-Winoground-Hard```| ```examples_augmented.jsonl``` as generated per the instructions in [this](https://github.com/ajd12342/why-winoground-hard/tree/main) repository | [here](https://huggingface.co/datasets/facebook/winoground/tree/main/data)
| ```/Winoground```| [examples.jsonl](https://huggingface.co/datasets/facebook/winoground/blob/main/data/examples.jsonl) | [here](https://huggingface.co/datasets/facebook/winoground/tree/main/data)
  

## EViL-Probe
To compile EViL-Probe:
- Place the source datasets in the subdirectories of ```source_datasets``` as detailed in the above table.
- Execute ```bash evil-probe/build_benchmark.sh```. (If you only wish to compile part of the benchmark, uncomment the respective line(s) in the script.

## Rainbow

## Citations
EViL-Probe
```
@inproceedings{evil-probe-2024,
    title = "EVil-Probe - A Composite Benchmark for Extensive Visio-Linguistic Probing",
    author = "Bexte, Marie  and
      Horbach, Andrea  and
      Zesch, Torsten",
    booktitle = "Proceedings of LREC-COLING",
    year = "2024",
}
```

Rainbow
```
@inproceedings{rainbow-2024,
    title = "Rainbow - A Benchmark for Systematic Testing of How Sensitive Visio-Linguistic Models are to Color Naming",
    author = "Bexte, Marie  and
      Horbach, Andrea  and
      Zesch, Torsten",
    booktitle = "Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics",
    year = "2024",
}
```
