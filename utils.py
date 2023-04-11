import numpy as np

def rad(y_orig_gold, y_orig_pred, y_aug_orig, y_aug_pred):

    # Convert to numpy to allow easy index-wise comparison
    y_orig_gold = np.array(y_orig_gold)
    y_orig_pred = np.array(y_orig_pred)
    y_aug_orig = np.array(y_aug_orig)
    y_aug_pred = np.array(y_aug_pred)

    # Correct in orig
    correct_in_orig = y_orig_gold == y_orig_pred
    print(correct_in_orig.sum(), correct_in_orig)

    # Correct in augmented
    correct_in_aug = y_aug_orig == y_aug_pred
    print(correct_in_aug.sum(), correct_in_aug)

    # Correct in both
    correct_in_both = correct_in_orig & correct_in_aug
    print(correct_in_both.sum(), correct_in_both)

    # Rad(orig, aug)
    rad_orig_aug = correct_in_both.sum()/(correct_in_orig.sum())
    # Rad(aug, orig)
    rad_aug_orig = correct_in_both.sum()/(correct_in_aug.sum())

    return rad_orig_aug, rad_aug_orig
