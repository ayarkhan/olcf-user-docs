# Load and parse the software modules list
import pandas as pd
import subprocess
import csv


# Read the CSV file into a DataFrame
df = pd.read_csv(f'/Users/3gy/saue/olcf-user-docs/software/software_list/2024_12_17_modules_on_olcf_machines.csv',
    usecols=['name','version','system','prereqs','path_to_module'],
    quotechar='"', skipinitialspace=True)
# print(df.head(),'\n')
print(df)
print(df.columns)
print(df.dtypes)

### First try at grouping
# # Group by the 'name' column and calculate the mean of other columns
# print('Group the database\n')
grouped_df = df.groupby('name')
# # grouped_df.describe()
# print(grouped_df.first())
# for name, group in grouped_df:
#     print(name)
#     print(group.head())
print( grouped_df['system'].agg(lambda x: ', '.join(x.unique())) )

print( grouped_df.agg( {
    'system': lambda x: ', '.join(x.unique()),
    'version': lambda x: ', '.join(x.astype(str).unique()),
    } ) )


import numpy as np
from natsort import index_natsorted
df = df.sort_values( by='version', ascending=False, key=lambda x: np.argsort(index_natsorted(df["version"])))

### Second try at grouping
df['versionPlus'] = '`'+df['version'].astype(str)+" <moduleinfo/"+df['name']+'_'+df['version']+'>`_'
print(df)
print(df.columns)

df['nameVersion'] = df['name']+'/'+df['version']
print(df)
print(df.columns)

grouped2_df = df.groupby(['name', 'system'], as_index=False)
df_pkg_summary = grouped2_df.agg( {
#    'version': lambda x: ', '.join(x.astype(str).unique()),
#     'versionPlus': lambda x: ', '.join(x.astype(str).unique()),
     'nameVersion': lambda x: ', '.join(x.astype(str).unique()),
    } )
print( df_pkg_summary )
print( type(df_pkg_summary) )

# df_pkg_summary.to_csv(f'/Users/3gy/saue/olcf-user-docs/software/software_list/pkg_summary.csv', index=False)

# sw, machine, versions, spack-top-line, link, spider-line, details-on-a-link, sw->link-to-user-docs

df_pkg_descriptions = pd.read_csv(f'/Users/3gy/saue/olcf-user-docs/software/software_list/pkg_descriptions.csv',
    quotechar='"', skipinitialspace=True, dtype=str)

# df_pkg_summary['version'] = df_pkg_summary['name'] + '/' + df_pkg_summary['version']

# Join on the index
df_pkg_summary.set_index('name', inplace=True)
df_pkg_descriptions.set_index('name', inplace=True)
df_pkg_summary = df_pkg_summary.join(df_pkg_descriptions)

print(df_pkg_summary)

df_pkg_summary.to_csv(f'/Users/3gy/saue/olcf-user-docs/software/software_list/pkg_summary.csv',
    index=True, quoting=csv.QUOTE_NONNUMERIC, na_rep="")
