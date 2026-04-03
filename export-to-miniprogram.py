#!/usr/bin/env python3
"""
从网页端题库导出小程序格式数据
"""

import json
import os

# 读取网页端题库
web_quiz_path = '/workspace/quiz-app/src/data/quizData.js'

with open(web_quiz_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 提取 quizData 数组
start = content.find('export const quizData = [')
end = content.find('\n];', start) + 2
array_content = content[start:end].replace('export const quizData = ', '')

# 解析JSON
quiz_data = json.loads(array_content.rstrip(';'))

# 生成小程序格式
output = f"""// 题库数据 - 自动生成
// 共 {len(quiz_data)} 道题目

const quizData = {json.dumps(quiz_data, ensure_ascii=False, indent=2)};

module.exports = quizData;
"""

# 写入小程序目录
output_path = '/workspace/quiz-miniprogram/data/quizData.js'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(output)

print(f'成功导出 {len(quiz_data)} 道题目到 {output_path}')

# 更新小程序的quizData.js引用
print('\n请在小程序的 app.js 中添加以下代码来加载数据:')
print("""
const quizData = require('./data/quizData')

// 初始化题库数据
if (!wx.getStorageSync('quizData') || wx.getStorageSync('quizData').length === 0) {
  wx.setStorageSync('quizData', quizData)
}
""")
