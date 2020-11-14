# Sistem Lampu Ruangan Otomatis 
# Oleh :
# Jonathan Suara Patty 
# Ariel Jusuf Indrastata

# Menggunakan library scikit-fuzzy dan matplotlib
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Deklarasi variabel
intensitas = ctrl.Antecedent(np.arange(0, 250, 1), 'intensitas')
pwm = ctrl.Consequent(np.arange(0, 255, 1), 'kecerahan')

# Menentukan derajat keanggotaan intensitas cahaya dalam ruangan
intensitas['gelap'] = fuzz.trapmf(intensitas.universe, [0, 0, 25, 75])
intensitas['redup'] = fuzz.trimf(intensitas.universe, [25, 75, 125])
intensitas['agak_redup'] = fuzz.trimf(intensitas.universe, [75, 125, 175])
intensitas['agak_terang'] = fuzz.trimf(intensitas.universe, [125, 175, 225])
intensitas['terang'] = fuzz.trapmf(intensitas.universe, [175, 225, 250, 250])

# Menentukan derajat keanggotaan nilai PWM
pwm['mati'] = fuzz.trimf(pwm.universe, [0, 0, 63])
pwm['redup'] = fuzz.trimf(pwm.universe, [0, 63, 127])
pwm['agak_redup'] = fuzz.trimf(pwm.universe, [63, 127, 191])
pwm['agak_terang'] = fuzz.trimf(pwm.universe, [127, 191, 255])
pwm['terang'] = fuzz.trimf(pwm.universe, [191, 255, 255])

# Plot grafik derajat keanggotaan
intensitas.view()
pwm.view()

# Rules
rule1 = ctrl.Rule(intensitas['gelap'], pwm['terang'])
rule2 = ctrl.Rule(intensitas['redup'], pwm['agak_terang'])
rule3 = ctrl.Rule(intensitas['agak_redup'], pwm['agak_redup'])
rule4 = ctrl.Rule(intensitas['agak_terang'], pwm['redup'])
rule5 = ctrl.Rule(intensitas['terang'], pwm['mati'])

# Persiapan untuk defuzzifikasi
pwm_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
nilai_pwm = ctrl.ControlSystemSimulation(pwm_ctrl)

# Input data
input_jml_orang = input("Masukan jumlah orang dalam ruangan : ")
input_intensitas = input("Masukan intensitas cahaya dalam ruangan dalam lux (lx) : ")

# Jika ada orang di dalam ruangan
if (int(input_jml_orang) > 0) :

    # Defuzzifikasi
    nilai_pwm.input['intensitas'] = int(input_intensitas)
    nilai_pwm.compute()

    # Plot grafik
    intensitas.view(sim=nilai_pwm)
    pwm.view(sim=nilai_pwm)

    # Output
    print("Nilai PWM untuk kecerahan lampu : ", nilai_pwm.output['kecerahan'])
    a = input()

# Jika tidak ada orang di dalam ruangan
else :
    print("Nilai PWM untuk kecerahan lampu : 0")
    a = input()