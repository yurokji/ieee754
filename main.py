from ieee754 import *
# IEEE754 32비트 부동소수점 클래스, 
# 및 연산 에뮬레이션

# 내부 동작 구현
# computable number != real number(실수)
# 실수: 0-1사이에 무한한 밀도
# 계산가능한 수 : 무한한 밀도 X
# floating point number == computable number
# 범위 <---> 밀도 반비례 관계
# 32 bit, 64bit, 128bit (밀도)
# 실수: 0.1 != 000000.00010...(2)
n1 = "2346.8934"
# 실제 저장되는 수: 1694.5682373046875
# 0x44d3d22f
n2 = "8334.35425"
# 실제 저장되는 수: 438.98651123046875
# 0x43db7e46
n3 = n1 + n2
# 실제 계산되는 수: 2133.5547485351562
# 0x450558e0


f1 = IEEE754_Float32(n1)
print("부동소수표현(16진수):", f1.toHex())
f1.printFixedBinNum(f1.__str__())
print("실제 저장된 값(10진수):", f1)
print()

f2 = IEEE754_Float32(n2)
print("부동소수표현(16진수):", f2.toHex())
f2.printFixedBinNum(f2.__str__())
print("실제 저장된 값(10진수):", f2)
print()

f3 = f1 + f2
print("부동소수표현(16진수):", f3.toHex())
f3.printFixedBinNum(f3.__str__())
print("실제 저장된 값(10진수):", f3)
