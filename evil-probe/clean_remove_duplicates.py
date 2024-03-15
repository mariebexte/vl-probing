import os
import numpy as np
import pandas as pd
import sys

in_dir = 'benchmark'
out_dir = 'benchmark_clean'

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

for file in os.listdir(in_dir):

    if file.endswith('jsonl'):

        df = pd.read_json(os.path.join(in_dir, file), lines=True)

        if len(df) > 0:
            df['sent_1_lower'] = df['sent_1'].apply(str.lower)
            df['sent_2_lower'] = df['sent_2'].apply(str.lower)

            df.drop(df[df['sent_1_lower'] == df['sent_2_lower']].index, inplace = True)

            arr = np.array(df['sent_1_lower'] == df['sent_2_lower'])

            if sum(arr) > 0:
                print(file, sum(arr))
            
            df.to_json(os.path.join(out_dir, file), orient='records', lines=True)