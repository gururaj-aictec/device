import json

# JSON格式字符串
#json文本字符串
json_str = '{"name": "John Doe", "age": 30, "is_student": false}'
json_str = '{"name": {"first": "John","last": "Doe"},"age": 30,"city": "New York"}'
# 解析JSON字符串
data = json.loads(json_str)

# 输出Python对象
first_name = data["name"]
print(first_name)

first_name = data["name"]["first"]
print(first_name)