# Load and parse the software modules list
import pandas as pd
# Used to read json and flatten nested data
import json
import numpy as np
# Used to sort the versions in a reasonable way
from natsort import index_natsorted

# Load the JSON data
with open('software_list_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Normalize the JSON data to handle nested data
df = pd.json_normalize(data['data'])

# Sort so that the versions are in order
df = df.sort_values(by='version', ascending=False, key=lambda x: np.argsort(index_natsorted(x)))

# Join the name and version columns
df['nameVersion'] = df['name']+'/'+df['version']+'    - Dependencies: '+df['prereqs']
print(df.describe())

# Create a groupby object
grouped_df = df.groupby(by=['name', 'system'], as_index=False)
print(grouped_df.describe())

#  Aggregate the nameVersion column
df_pkg_summary = grouped_df.agg({
    'description': 'first',
    'homepage': 'first',
    'nameVersion': lambda x: ' <br />'.join(x.astype(str).unique()),
})
print(df_pkg_summary.describe())
print(df_pkg_summary.tail())

# Save the DataFrame to a AJAX file
df_pkg_summary.to_json('software_list_group.json', orient='table', mode='w')
