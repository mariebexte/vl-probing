## Dict to show which files are to be aggregated into which new file
MERGE_SUBDATASETS = {

    ### VIDEO-BASED
    'EqBen_eqbengebc.jsonl': ['EqBen_eqbengebc.jsonl'],
    'EqBen_eqbenag.jsonl': ['EqBen_eqbenag.jsonl'],
    'EqBen_eqbenyoucook2.jsonl': ['EqBen_eqbenyoucook2.jsonl'],

    ### SPATIAL RELATIONS
    'EqBen_eqbenkubric_loc.jsonl': ['EqBen_eqbenkubric_loc.jsonl'],
    'VALSE-relations.jsonl': ['VALSE-relations.jsonl'],
    'vl-checklist-relation-vg_spatial.jsonl': ['vl-checklist-relation-vg_spatial.jsonl'],
    'visual_spatial_reasoning.jsonl': ['visual_spatial_reasoning.jsonl'],
    'aro_relation.jsonl': ['aro_relation.jsonl'],

    ### COLOR
    'vl-checklist-attribute_color.jsonl': ['vl-checklist-attribute-vaw_color.jsonl', 'vl-checklist-attribute-vg_color.jsonl'],
    'EqBen_eqbensd_color.jsonl': ['EqBen_eqbensd_color.jsonl'],

    ### ATTRIBUTE
    'vl-checklist-attribute_material.jsonl': ['vl-checklist-attribute-vaw_material.jsonl', 'vl-checklist-attribute-vg_material.jsonl'],
    'vl-checklist-attribute_action.jsonl': ['vl-checklist-attribute-vg_action.jsonl', 'vl-checklist-attribute-vaw_action.jsonl'],
    'vl-checklist-attribute_size.jsonl': ['vl-checklist-attribute-vaw_size.jsonl', 'vl-checklist-attribute-vg_size.jsonl'],
    'vl-checklist-attribute_state.jsonl': ['vl-checklist-attribute-vaw_state.jsonl', 'vl-checklist-attribute-vg_state.jsonl'],
    'EqBen_eqbenkubric_attr.jsonl': ['EqBen_eqbenkubric_attr.jsonl'],
    'aro_attribute.jsonl': ['aro_attribute.jsonl'],

    ### NUMBER
    'EqBen_eqbenkubric_cnt.jsonl': ['EqBen_eqbenkubric_cnt.jsonl'],
    'VALSE-counting-adversarial.jsonl': ['VALSE-counting-adversarial.jsonl'],
    'VALSE-counting-hard.jsonl': ['VALSE-counting-hard.jsonl'],
    'VALSE-counting-small-quant.jsonl': ['VALSE-counting-small-quant.jsonl'],
    'VALSE-plurals.jsonl': ['VALSE-plurals.jsonl'],
    'visual7w_counting_hard_split_test.jsonl': ['visual7w_counting_hard_split_test.jsonl'],
    'visual7w_counting_standard_split_test.jsonl': ['visual7w_counting_standard_split_test.jsonl'],

    ### PERSPECTIVE
    'High-level_test_action.jsonl': ['High-level_test_action.jsonl'],
    'High-level_test_rationale.jsonl': ['High-level_test_rationale.jsonl'],
    'High-level_test_scene.jsonl': ['High-level_test_scene.jsonl'],

    ### HYPERNYMS
    'WH_semanticwordbased_replacehypernyms.jsonl': 'WH_semanticwordbased_replacehypernyms.jsonl',

    ### NEGATION
    'VALSE-coreference_question-only.jsonl': ['VALSE-coreference-hard_question-only.jsonl', 'VALSE-coreference-standard_question-only.jsonl'],
    'VALSE-coreference.jsonl': ['VALSE-coreference-hard.jsonl', 'VALSE-coreference-standard.jsonl'],
    'VALSE-existence.jsonl': ['VALSE-existence.jsonl'],

    ### NOUNS
    'vl-checklist-object_swig.jsonl': ['vl-checklist-object-location_swig_tool_center.jsonl',
                                       'vl-checklist-object-location_swig_tool_margin.jsonl',
                                       'vl-checklist-object-location_swig_tool_mid.jsonl',
                                       'vl-checklist-object-location_swig_destination_center.jsonl',
                                       'vl-checklist-object-location_swig_destination_margin.jsonl',
                                       'vl-checklist-object-location_swig_destination_mid.jsonl',
                                       'vl-checklist-object-location_swig_item_center.jsonl',
                                       'vl-checklist-object-location_swig_item_margin.jsonl',
                                       'vl-checklist-object-location_swig_item_mid.jsonl',
                                       'vl-checklist-object-location_swig_agent_center.jsonl',
                                       'vl-checklist-object-location_swig_agent_margin.jsonl',
                                       'vl-checklist-object-location_swig_agent_mid.jsonl',
                                       'vl-checklist-object-size_swig_tool_large.jsonl',
                                       'vl-checklist-object-size_swig_tool_medium.jsonl',
                                       'vl-checklist-object-size_swig_tool_small.jsonl',
                                       'vl-checklist-object-size_swig_destination_large.jsonl',
                                       'vl-checklist-object-size_swig_destination_medium.jsonl',
                                       'vl-checklist-object-size_swig_destination_small.jsonl',
                                       'vl-checklist-object-size_swig_item_large.jsonl',
                                       'vl-checklist-object-size_swig_item_medium.jsonl',
                                       'vl-checklist-object-size_swig_item_small.jsonl',
                                       'vl-checklist-object-size_swig_agent_large.jsonl',
                                       'vl-checklist-object-size_swig_agent_medium.jsonl',
                                       'vl-checklist-object-size_swig_agent_small.jsonl'],
    'vl-checklist-object_hake.jsonl': ['vl-checklist-object-location_hake_obj_center.jsonl',
                                       'vl-checklist-object-location_hake_obj_margin.jsonl',
                                       'vl-checklist-object-location_hake_obj_mid.jsonl',
                                       'vl-checklist-object-size_hake_obj_large.jsonl',
                                       'vl-checklist-object-size_hake_obj_medium.jsonl',
                                       'vl-checklist-object-size_hake_obj_small.jsonl'],
    'vl-checklist_object_vg.jsonl': ['vl-checklist-object-location_vg_subj_center.jsonl',
                                     'vl-checklist-object-location_vg_subj_margin.jsonl',
                                     'vl-checklist-object-location_vg_subj_mid.jsonl',
                                     'vl-checklist-object-size_vg_subj_large.jsonl',
                                     'vl-checklist-object-size_vg_subj_medium.jsonl',
                                     'vl-checklist-object-size_vg_subj_small.jsonl',
                                     'vl-checklist-object-location_vg_obj_center.jsonl',
                                     'vl-checklist-object-location_vg_obj_margin.jsonl',
                                     'vl-checklist-object-location_vg_obj_mid.jsonl',
                                     'vl-checklist-object-size_vg_obj_large.jsonl',
                                     'vl-checklist-object-size_vg_obj_medium.jsonl',
                                     'vl-checklist-object-size_vg_obj_small.jsonl'],
    'predicate-noun_subject.jsonl': ['predicate-noun_subject.jsonl'],
    'compositional_visual_genome.jsonl': ['compositional_visual_genome_object.jsonl', 'compositional_visual_genome_subject.jsonl'],
    'SVO_probes.jsonl': ['SVO_probes_object.jsonl', 'SVO_probes_subject.jsonl'],
    'foil_test.jsonl': ['foil_test.jsonl'],
    'EqBen_eqbensd_noun.jsonl': ['EqBen_eqbensd_noun.jsonl'],

    ### PARAPHRASES
    'WH_paraphrasing_backtranslation.jsonl': ['WH_paraphrasing_backtranslation.jsonl'],
    'WH_paraphrasing_diverseparaphrase.jsonl': ['WH_paraphrasing_backtranslation.jsonl'],
    'WH_semanticwordbased_synonymsubstitution.jsonl.jsonl': ['WH_semanticwordbased_synonymsubstitution.jsonl.jsonl'],

    ### RANDOM
    'coco_random.jsonl': ['coco_random.jsonl'],
    'flickr30k_random.jsonl': ['flickr30k_random.jsonl'],

    ### SLANG
    'WH_semanticwordbased_slangificator.jsonl': ['WH_semanticwordbased_slangificator.jsonl'],

    ### SYNONYMS
    'WH_semanticwordbased_synonymsubstitution.jsonl': ['WH_semanticwordbased_synonymsubstitution.jsonl'],

    ### VERBS
    'compositional_visual_genome_verb.jsonl': ['compositional_visual_genome_verb.jsonl'],
    'SVO_probes_verb.jsonl': ['SVO_probes_verb.jsonl'],
    'vl-checklist-relation_swig_action.jsonl': ['vl-checklist-relation_swig_action.jsonl'],
    'vl-checklist-relation_hake_action.jsonl': ['vl-checklist-relation_hake_action.jsonl'],
    'vl-checklist-relation-vg_action.jsonl': ['vl-checklist-relation-vg_action.jsonl'],
    'predicate-noun_object.jsonl': ['predicate-noun_object.jsonl'],
    'VALSE-action-replacement.jsonl': ['VALSE-action-replacement.jsonl'],   

    ### SEMANTIC ROLE
    'VALSE-actant-swap.jsonl': ['VALSE-actant-swap.jsonl'],

    ### WORD ORDER
    'WH_rulebased_propbanksrlroles.jsonl': ['WH_rulebased_propbanksrlroles.jsonl'],
    'Winoground.jsonl': ['winoground_object.jsonl', 'winoground_relation.jsonl', 'winoground_both.jsonl'],

    ### SPECIFICITY
    'EqBen_eqbensd_specificity.jsonl': ['EqBen_eqbensd_specificity.jsonl'],

    ### IMAGE TYPE
    'EqBen_eqbensd_img_type.jsonl': ['EqBen_eqbensd_img_type.jsonl'],

}


MERGE_CATEGORIES = {

    ### VIDEO-BASED
    'VIDEO_BASED.jsonl': ['EqBen_eqbengebc.jsonl', 'EqBen_eqbenag.jsonl', 'EqBen_eqbenyoucook2.jsonl'],

    ### SPATIAL RELATIONS
    'SPATIAL_RELATIONS.jsonl': ['EqBen_eqbenkubric_loc.jsonl', 'VALSE-relations.jsonl', 'vl-checklist-relation-vg_spatial.jsonl',
                                'visual_spatial_reasoning.jsonl', 'aro_relation.jsonl'],

    ### COLOR
    'COLOR.jsonl': ['vl-checklist-attribute_color.jsonl', 'EqBen_eqbensd_color.jsonl'],

    ### ATTRIBUTE
    'ATTRIBUTE.jsonl': ['vl-checklist-attribute_material.jsonl', 'vl-checklist-attribute_action.jsonl',
                        'vl-checklist-attribute_size.jsonl', 'vl-checklist-attribute_state.jsonl',
                        'EqBen_eqbenkubric_attr.jsonl', 'aro_attribute.jsonl'],

    ### NUMBER
    'NUMBER.jsonl': ['EqBen_eqbenkubric_cnt.jsonl', 'VALSE-counting-adversarial.jsonl', 'VALSE-counting-hard.jsonl',
                     'VALSE-counting-small-quant.jsonl', 'VALSE-plurals.jsonl', 'visual7w_counting_hard_split_test.jsonl',
                     'visual7w_counting_standard_split_test.jsonl'],

    ### PERSPECTIVE
    'PERSPECTIVE.jsonl': ['High-level_test_action.jsonl', 'High-level_test_rationale.jsonl', 'High-level_test_scene.jsonl'],

    ### HYPERNYMS
    'HYPERNYMS.jsonl': 'WH_semanticwordbased_replacehypernyms.jsonl',

    ### NEGATION
    'NEGATION.jsonl': ['VALSE-coreference_question-only.jsonl', 'VALSE-coreference.jsonl', 'VALSE-existence.jsonl'],

    ### NOUNS
    'NOUNS.jsonl': ['vl-checklist-object_swig.jsonl', 'vl-checklist-object_hake.jsonl', 'vl-checklist_object_vg.jsonl',
                    'predicate-noun_subject.jsonl', 'compositional_visual_genome.jsonl', 'SVO_probes.jsonl',
                    'foil_test.jsonl', 'EqBen_eqbensd_noun.jsonl'],

    ### PARAPHRASES
    'PARAPHRASES.jsonl': ['WH_paraphrasing_backtranslation.jsonl', 'WH_paraphrasing_diverseparaphrase.jsonl'],

    ### RANDOM
    'RANDOM.jsonl': ['coco_random.jsonl', 'flickr30k_random.jsonl'],

    ### SLANG
    'SLANG.jsonl': ['WH_semanticwordbased_slangificator.jsonl'],

    ### SYNONYMS
    'SYNONYMS.jsonl': ['WH_semanticwordbased_synonymsubstitution.jsonl'],

    ### VERBS
    'VERBS.jsonl': ['compositional_visual_genome_verb.jsonl', 'SVO_probes_verb.jsonl', 'vl-checklist-relation_swig_action.jsonl',
                    'vl-checklist-relation_hake_action.jsonl', 'vl-checklist-relation-vg_action.jsonl', 'predicate-noun_object.jsonl',
                    'VALSE-action-replacement.jsonl'],   

    ### SEMANTIC ROLE
    'SEMANTIC_ROLE.jsonl': ['VALSE-actant-swap.jsonl'],

    ### SPECIFICITY
    'SPECIFICITY.jsonl': ['EqBen_eqbensd_specificity.jsonl'],

    ### IMAGE TYPE
    'IMAGE_TYPE.jsonl': ['EqBen_eqbensd_img_type.jsonl'],

    ### WORD ORDER: PRESERVING
    'WORD_ORDER': ['WH_rulebased_propbanksrlroles.jsonl'],
    ### WORD ORDER: SEMANTIC CHANGE
    'WORD_ORDER_SEMANTIC_CHANGE.jsonl': ['Winoground.jsonl'],
}