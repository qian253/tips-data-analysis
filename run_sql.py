import sqlite3
import pandas as pd

# 连接数据库
conn = sqlite3.connect('tips.db')

# 定义所有SQL查询（直接写死，避免读取文件的空行问题）
queries = {
    "1. 查看数据前10行": """
        SELECT * FROM tips LIMIT 10;
    """,
    "2. 统计数据总行数": """
        SELECT COUNT(*) AS total_records FROM tips;
    """,
    "3. 不同用餐时段的消费分析": """
        SELECT 
            time,
            COUNT(*) AS order_count,
            ROUND(AVG(total_bill), 2) AS avg_bill,
            ROUND(MAX(total_bill), 2) AS max_bill,
            ROUND(AVG(tip), 2) AS avg_tip,
            ROUND(MAX(tip), 2) AS max_tip
        FROM tips
        GROUP BY time
        ORDER BY avg_bill DESC;
    """,
    "4. 不同用餐人数的小费率分析": """
        SELECT 
            size,
            COUNT(*) AS order_count,
            ROUND(AVG(tip / total_bill * 100), 2) AS avg_tip_rate
        FROM tips
        GROUP BY size
        ORDER BY size;
    """,
    "5. 不同性别的消费差异": """
        SELECT 
            sex,
            COUNT(*) AS order_count,
            ROUND(AVG(total_bill), 2) AS avg_bill,
            ROUND(AVG(tip / total_bill * 100), 2) AS avg_tip_rate
        FROM tips
        GROUP BY sex;
    """,
    "6. 不同星期的消费分析": """
        SELECT 
            day,
            COUNT(*) AS order_count,
            ROUND(AVG(total_bill), 2) AS avg_bill
        FROM tips
        GROUP BY day
        ORDER BY avg_bill DESC;
    """,
    "7. 吸烟与不吸烟顾客的小费率对比": """
        SELECT 
            smoker,
            COUNT(*) AS order_count,
            ROUND(AVG(tip / total_bill * 100), 2) AS avg_tip_rate
        FROM tips
        GROUP BY smoker;
    """,
    "8. 账单金额与小费金额的相关系数": """
        SELECT 
            ROUND(
                (COUNT(*) * SUM(total_bill * tip) - SUM(total_bill) * SUM(tip)) /
                SQRT((COUNT(*) * SUM(total_bill * total_bill) - SUM(total_bill) * SUM(total_bill)) *
                     (COUNT(*) * SUM(tip * tip) - SUM(tip) * SUM(tip))),
                2
            ) AS correlation
        FROM tips;
    """
}

# 执行每个查询并打印结果
for name, sql in queries.items():
    print(f"\n{'='*60}")
    print(f"【{name}】")
    print(f"{'='*60}")
    try:
        result = pd.read_sql(sql, conn)
        print(result)
    except Exception as e:
        print(f"❌ 错误: {e}")

conn.close()
print("\n✅ 所有SQL查询执行完成！")