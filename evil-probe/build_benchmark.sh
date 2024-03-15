#!/bin/sh

python3 prepare_aro.py
python3 prepare_coco_random.py
python3 prepare_compositional_visual_genome.py
python3 prepare_counting_probe.py
python3 prepare_EqBen.py
python3 prepare_flickr_random.py
python3 prepare_foil_it.py
python3 prepare_high_level.py
python3 prepare_predicate_noun.py
python3 prepare_SVO_probes.py
python3 prepare_valse.py
python3 prepare_visual_spatial_reasoning.py
python3 prepare_vl_checklist
python3 prepare_winoground_hard.py
python3 prepare_winoground.py

python3 postprocess_eqben.py
python3 clean_remove_duplicates.py