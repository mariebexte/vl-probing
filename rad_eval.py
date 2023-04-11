from utils import rad

y_orig_true = [True, True, True, True]
y_orig_pred = [True, False, True, False]
y_aug_true = [False, False, False, False]
y_aug_pred = [False, False, False, True]

score = rad(y_orig_true, y_orig_pred, y_aug_true, y_aug_pred)
print(score)

