import pandas as pd

df = pd.read_csv('classify_data.csv')
df.to_json('box_offset.json',orient='records')
# df.to_json('box_offset.json',orient='records',force_ascii=False)