import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# 解决Matplotlib中文显示乱码
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 1. 数据读取
df = sns.load_dataset("tips")

# 2. 数据探索与质量检查
print("=== 数据前5行预览 ===")
print(df.head())
print("\n=== 数据基本信息 ===")
print(df.info())
print("\n=== 数值型字段统计描述 ===")
print(df.describe())

# 3. 数据清洗
# 去除重复行
df = df.drop_duplicates()
print(f"\n清洗后数据量：{df.shape[0]}条")

# 4. 核心分析
# 4.1 不同用餐时段的消费与小费差异
time_stats = df.groupby("time")[["total_bill", "tip"]].agg(["mean", "max"]).round(1)
print("\n=== 不同用餐时段统计 ===")
print(time_stats)

# 4.2 用餐人数与小费率的关系
df["tip_rate"] = df["tip"] / df["total_bill"] * 100
size_tip_rate = df.groupby("size")["tip_rate"].mean().round(1)
print("\n=== 不同用餐人数平均小费率(%) ===")
print(size_tip_rate)

# 4.3 不同性别的消费差异
gender_stats = df.groupby("sex")[["total_bill", "tip"]].agg(["mean", "max"]).round(1)
print("\n=== 不同性别消费统计 ===")
print(gender_stats)

# 5. 数据可视化
# 图1：午餐vs晚餐平均账单对比
plt.figure(figsize=(8, 5))
time_stats["total_bill"]["mean"].plot(kind="bar", color=["#1f77b4", "#ff7f0e"])
plt.title("不同用餐时段平均账单对比", fontsize=14)
plt.xlabel("用餐时段", fontsize=12)
plt.ylabel("平均账单金额(美元)", fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("时段账单对比.png", dpi=300)
plt.close()

# 图2：用餐人数与平均小费率关系
plt.figure(figsize=(8, 5))
size_tip_rate.plot(kind="line", marker="o", color="#2ca02c", linewidth=2)
plt.title("用餐人数与平均小费率关系", fontsize=14)
plt.xlabel("用餐人数", fontsize=12)
plt.ylabel("平均小费率(%)", fontsize=12)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("人数小费率关系.png", dpi=300)
plt.close()

# 6. 导出清洗后数据
df.to_csv("tips分析结果.csv", index=False)

print("\n✅ 分析完成，结果已导出")
