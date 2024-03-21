from sympy import Eq, symbols, solve

a, b,c,d,e = symbols('a,b,c,d,e')

eq1 = Eq(a + 33.33*b - 103.99*c + -3465.9867*d + 1110.8889*e, -16.778)
eq2 = Eq(a-38.37*b - 103.99*c + 3990.0963*d + 1472.2569*e, -26.856)
eq3= Eq(a - 42.41*b + 1798.6081*e, -42.696)
eq4=Eq(a - 48.47*b + 93.89*c - 4550.8483*d+2349.3409*e, -15.742)
eq5=Eq(a + 36.35*b + 87.84*c + 3192.984*d + 1321.3225*e, -8.85)

solution = solve((eq1,eq2,eq3,eq4,eq5), (a,b,c,d,e))

print(solution)