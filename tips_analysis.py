# 导入所有需要的库
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# 解决中文显示问题（必须加，否则图表中文会变成方块）
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# ---------------------- 1. 读取数据（重点：不用你下载任何文件！） ----------------------
# 直接用seaborn自带的tips数据集，一行代码搞定
df = sns.load_dataset("tips")

# ---------------------- 2. 初步查看数据（确认数据读取成功） ----------------------
print("=== 数据前5行（看一眼结构） ===")
print(df.head())
print("\n=== 数据基本信息+（有没有缺失值） ===")
print(df.info())
print("\n=== 数值列统计信息（账单、小费的平均值/最大值等） ===")
print(df.describe())

# ---------------------- 3. 数据清洗（这个数据集非常干净，几乎不用清洗） ----------------------
# 只做最基础的去重，其他不用管
df = df.drop_duplicates()
print(f"\n清洗后数据量：{df.shape[0]}条")

# ---------------------- 4. 核心分析1：不同用餐时段（午餐/晚餐）的账单和小费差异 ----------------------
time_stats = df.groupby("time")[["total_bill", "tip"]].agg(["mean", "max"]).round(1)
print("\n=== 不同用餐时段的账单与小费统计 ===")
print(time_stats)

# ---------------------- 5. 核心分析2：用餐人数和平均小费率的关系（小费率=小费/总账单） ----------------------
# 先计算小费率（这一步能体现你处理衍生指标的能力）
df["tip_rate"] = df["tip"] / df["total_bill"] * 100  # 转成百分比
size_tip_rate = df.groupby("size")["tip_rate"].mean().round(1)
print("\n=== 不同用餐人数的平均小费率（%） ===")
print(size_tip_rate)

# ---------------------- 6. 生成可视化图表（面试的加分项） ----------------------
# 图表1：午餐vs晚餐的平均账单对比
plt.figure(figsize=(8, 5))
time_stats["total_bill"]["mean"].plot(kind="bar", color=["#1f77b4", "#ff7f0e"])
plt.title("午餐vs晚餐的平均账单金额对比", fontsize=14)
plt.xlabel("用餐时段", fontsize=12)
plt.ylabel("平均账单金额（美元）", fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("时段账单对比.png", dpi=300)
plt.close()

# 图表2：用餐人数与平均小费率的关系
plt.figure(figsize=(8, 5))
size_tip_rate.plot(kind="line", marker="o", color="#2ca02c", linewidth=2)
plt.title("用餐人数与平均小费率的关系", fontsize=14)
plt.xlabel("用餐人数", fontsize=12)
plt.ylabel("平均小费率（%）", fontsize=12)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("人数小费率关系.png", dpi=300)
plt.close()

# ---------------------- 7. 导出清洗后的数据（可选，方便你后续分析） ----------------------
df.to_csv("tips分析结果.csv", index=False)

print("\n✅ 分析完成！图表和数据都保存在你的项目文件夹里啦")