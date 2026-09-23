import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///review.db")

# ルール別・状態別の件数
df = pd.read_sql(
    """
    SELECT rule_type, status, COUNT(*) as count
    FROM findings
    GROUP BY rule_type, status
    """,
    engine,
)
print(df)
print()

# 承認率(ルールごと)
summary = pd.read_sql(
    """
    SELECT
        rule_type,
        COUNT(*) as total,
        SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) as approved,
        SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) as rejected
    FROM findings
    GROUP BY rule_type
    """,
    engine,
)
summary["approval_rate"] = summary["approved"] / summary["total"]
print(summary)

# グラフ:ルール別、承認・却下の件数
import matplotlib.pyplot as plt

pivot = df.pivot(index="rule_type", columns="status", values="count").fillna(0)
pivot.plot(kind="bar", stacked=True)
plt.title("Findings by rule type and status")
plt.xlabel("Rule type")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("findings_summary.png")
print("\nSaved chart to findings_summary.png")