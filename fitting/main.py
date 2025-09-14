import pandas as pd
import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# 엑셀 파일 불러오기
df = pd.read_excel('./file/test.xlsx', sheet_name='0.8', usecols=['Freq', 'R', 'X'])
freq = df['Freq'].values                # 주파수 (Hz)
R_measured = df['R'].values             # 실수부 (Measured R)
X_measured = df['X'].values             # 허수부 (Measured X)

'''
print(df.head())

# 시각화 (Real)
df.plot(x='Freq', y='R', kind='line', title='Real Part', grid=True, logx=True)
plt.xlabel('Freq (Hz)')
plt.ylabel('R')
plt.show()
'''
# Rs L 직렬, Rd C 병렬
def impedance_model(freq, Rs, Rd, C, L):
    omega = 2 * np.pi * freq # w = 2 * pi * f
    Zc = 1 / (1j * omega * C) # 커패시터 임피던스
    Zl = 1j * omega * L # 인덕터 임피던스
    Z_parl = 1 / (1/Zc + 1/Rd) # 저항 커패시터 병렬처리
    return Rs + Zl + Z_parl # 직렬로 반환

def residuals(params, freq, R_meas, X_meas):
    Rs, Rd, C, L = params 
    Z = impedance_model(freq, Rs, Rd, C, L)
    return np.concatenate([(Z.real - R_meas), (Z.imag - X_meas)]) # 실수부 허수부 차로 배열 생성

# Rs, Rd, C, L 범위 설정
bounds = ([0, 0, 1e-12, 1e-12], [100, 1000, 1e-7, 1e-6]) # 실험적 결과로 나온 범위


# 초기 값 설정 
best_score = -np.inf
best_params = None


for i in range(20):
    init = np.random.uniform(low=[30, 500, 1e-10, 1e-10], high=[60, 600, 1e-8, 1e-7]) # 초기값 랜덤
    result = least_squares(residuals, init, args=(freq, R_measured, X_measured), bounds=bounds)

    Z_try = impedance_model(freq, *result.x)
    r2_r = r2_score(R_measured, Z_try.real) # 실수부 결정계수
    r2_x = r2_score(X_measured, Z_try.imag) # 허수부 결정계수
    r2_total = r2_r + r2_x

    if r2_total > best_score:
        best_score = r2_total
        best_params = result.x


print("최종 선택된 파라미터:")
print(f"Rs = {best_params[0]:.4f}, Rd = {best_params[1]:.4f}, C = {best_params[2]:.4e}, L = {best_params[3]:.4e}")
