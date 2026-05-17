import seaborn as sns
import pandas as pd
import sqlite3

# 加载tips数据集
df = sns.load_dataset('tips')

# 保存为SQLite数据库
conn = sqlite3.connect('tips.db')
df.to_sql('tips', conn, if_exists='replace', index=False)
conn.close()

print("✅ tips.db数据库生成成功！")