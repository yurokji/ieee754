from ieee754 import *
# IEEE754 32비트 부동소수점 클래스, 
# 및 연산 에뮬레이션

n1 = "12.062584"
n2 = "-438.009865"

##############32비트 부동소수 계산################
f1 = IEEE754_Float(n1, precision="single")
print(str(f1.size)+"비트 부동소수표현(16진수):", f1.toHex())
f1.printFixedBinNum(f1.__str__())
print("실제 저장된 값(10진수):", f1)
print("원본 수와 차이:", float(n1) - float(f1.__str__()))
print()
f2 = IEEE754_Float(n2,precision="single")
print(str(f1.size)+"비트 부동소수표현(16진수):", f2.toHex())
f2.printFixedBinNum(f2.__str__())
print("실제 저장된 값(10진수):", f2)
print("원본 수와 차이:", float(n2) - float(f2.__str__()))
print()
f3 = f1  - f2
print(str(f1.size)+"부동소수표현(16진수):", f3.toHex())
f3.printFixedBinNum(f3.__str__())
print("실제 저장된 값(10진수):", f3)
print("원본 수와 차이:", (float(n1)-float(n2)) - float(f3.__str__()))

print("=========================================================================")
# ##############64비트 부동소수 계산################
f1 = IEEE754_Float(n1, precision="double")
print(str(f1.size)+"비트 부동소수표현(16진수):", f1.toHex())
f1.printFixedBinNum(f1.__str__())
print("실제 저장된 값(10진수):", f1)
print("원본 수와 차이:", float(n1) - float(f1.__str__()))
print()
f2 = IEEE754_Float(n2,precision="double")
print(str(f1.size)+"비트 부동소수표현(16진수):", f2.toHex())
f2.printFixedBinNum(f2.__str__())
print("실제 저장된 값(10진수):", f2)
print("원본 수와 차이:", float(n2) - float(f2.__str__()))
print()
f3 = f1  - f2
print(str(f1.size)+"부동소수표현(16진수):", f3.toHex())
f3.printFixedBinNum(f3.__str__())
print("실제 저장된 값(10진수):", f3)
print("원본 수와 차이:", (float(n1)-float(n2)) - float(f3.__str__()))

print("=========================================================================")
# ##############128비트 부동소수 계산################
f1 = IEEE754_Float(n1, precision="quad")
print(str(f1.size)+"비트 부동소수표현(16진수):", f1.toHex())
f1.printFixedBinNum(f1.__str__())
print("실제 저장된 값(10진수):", f1)
print("원본 수와 차이:", float(n1) - float(f1.__str__()))
print()
f2 = IEEE754_Float(n2,precision="quad")
print(str(f1.size)+"비트 부동소수표현(16진수):", f2.toHex())
f2.printFixedBinNum(f2.__str__())
print("실제 저장된 값(10진수):", f2)
print("원본 수와 차이:", float(n2) - float(f2.__str__()))
print()
f3 = f1  - f2
print(str(f1.size)+"부동소수표현(16진수):", f3.toHex())
f3.printFixedBinNum(f3.__str__())
print("실제 저장된 값(10진수):", f3)
print("원본 수와 차이:", (float(n1)-float(n2)) - float(f3.__str__()))