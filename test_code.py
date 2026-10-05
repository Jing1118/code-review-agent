def calculate_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    return total / len(numbers)  # 如果numbers为空会报错

API_KEY = "sk-1234567890"  # 硬编码敏感信息

result = calculate_average([1, 2, 3])
print(result)