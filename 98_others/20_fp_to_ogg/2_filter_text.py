import re


def find_non_matching_kovs_flexible(file_path, pattern_line1="00'", pattern_line2="b'KOVS"):
  """
  找出不符合 pattern_line1 + pattern_line2 模式的 pattern_line2 行
  """
  non_matching = []

  with open(file_path, 'r', encoding='utf-8') as f:
    lines = [line.rstrip('\n') for line in f]  # 去除换行符

  for i in range(1, len(lines)):
    # 检查当前行是否匹配第二个模式
    if re.search(pattern_line2, lines[i]):
      # 检查前一行是否匹配第一个模式
      if not re.search(pattern_line1, lines[i - 1]):
        non_matching.append({
            'line_number': i + 1,
            'content': lines[i],
            'previous_line': lines[i - 1]
        })

  return non_matching


# 使用示例
if __name__ == "__main__":
  file_path = "list_output.txt"

  # 使用默认模式：前一行是 00'，当前行是 b'KOVS
  results = find_non_matching_kovs_flexible(file_path)

  if results:
    print("不符合 '00'\\n'b'KOVS' 模式的 b'KOVS 行：")
    for item in results:
      print(f"行 {item['line_number']}: {item['content']}")
      print(f"  前一行: {item['previous_line']}")
  else:
    print("所有 b'KOVS 行都符合模式")
