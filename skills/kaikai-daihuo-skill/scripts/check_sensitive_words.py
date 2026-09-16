#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kaikai-daihuo-skill 千川投流敏感词检测脚本。

用法:
    python3 check_sensitive_words.py <文案文件.txt>
    echo "文案内容" | python3 check_sensitive_words.py
    python3 check_sensitive_words.py --list   # 列出全部敏感词

退出码:
    0 = 未命中敏感词
    1 = 命中敏感词（输出命中明细）

说明: 命中项需人工判断是否为真实违规（如「第一天」命中「第一」是误报，
按清单口径宁可标红复查）。改写后必须重新运行本脚本确认无命中。
"""

import sys
import re

# 与 references/qianchuan-sensitive-words.md 保持一致的最小可检查清单
SENSITIVE_WORDS = {
    "0/无添加类": [
        "0蔗糖", "0添加", "零添加", "0防腐剂", "0色素", "无添加", "没有添加",
        "不含添加剂", "无任何添加剂", "无糖", "零糖", "低糖", "纯天然",
        "天然无添加", "配料表干干净净",
    ],
    "绝对化/极限词": [
        "最", "第一", "唯一", "首个", "首选", "顶级", "极致", "巅峰", "王牌",
        "冠军", "国家级", "世界级", "天花板", "独家", "首发", "绝无仅有",
        "史无前例", "万能", "永久", "100%", "100%有效", "零风险", "零差评",
        "必备", "性价比之王", "全网最低价", "地板价", "绝对", "彻底", "永不反弹",
        "特效", "神器",
    ],
    "医疗/功效词": [
        "治疗", "疗效", "根治", "治愈", "预防", "防治", "康复", "改善", "调节",
        "养颜", "排毒", "消炎", "杀菌", "抑菌", "抗菌", "止痒", "去味",
        "增强免疫", "提高抵抗力", "延年益寿", "减肥", "瘦身", "燃脂", "降血糖",
        "降血脂", "降压", "抗癌", "防癌", "助眠", "安神", "补脑", "护肝",
        "修复敏感肌",
    ],
    "虚假承诺/无依据数据": [
        "假一赔十", "无效退款", "保险赔付", "包治包好", "绝对有效",
        "销量第一", "好评率第一", "转化率第一",
    ],
    "权威背书类": [
        "国家推荐", "国家机关推荐", "特供", "专供", "央视上榜", "cctv",
        "老字号", "驰名商标", "官方认证",
    ],
}


def check(text: str):
    hits = []
    for category, words in SENSITIVE_WORDS.items():
        for word in words:
            # 全角/半角、大小写归一化后做子串匹配
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            for m in pattern.finditer(text):
                hits.append({"word": m.group(0), "category": category, "pos": m.start()})
    return hits


def main():
    args = sys.argv[1:]
    if args and args[0] == "--list":
        for category, words in SENSITIVE_WORDS.items():
            print(f"[{category}] " + "、".join(words))
        return 0

    if args:
        with open(args[0], "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("错误: 未提供文案内容")
        return 2

    hits = check(text)
    if not hits:
        print("✓ 未命中敏感词")
        return 0

    print(f"✗ 命中 {len(hits)} 处敏感词:")
    for h in sorted(hits, key=lambda x: x["pos"]):
        print(f"  - 位置 {h['pos']}: 「{h['word']}」 类别: {h['category']}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
