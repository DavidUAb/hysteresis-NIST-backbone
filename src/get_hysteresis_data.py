"""
Created on 5 April 2024
@author: David Chan
Reference: Copyright Silvia Mazzoni, silviamazzoni@yahoo.com 2021
https://opensees.github.io/OpenSeesDocumentation/user/manual/material/uniaxialMaterials/HystereticSM.html
"""
import csv
import openseespy.opensees as ops
import matplotlib.pyplot as plt
# ------------------
#  initialize
# ------------------
import numpy as np
import matplotlib.pyplot as plt
import hysteresis as hys

strainMap = {}


def defineStrainHistory(peaksArray, scaleFactor, nSteps, nCycles):
    strain = []
    for thisPeak in peaksArray:
        for i in range(nCycles):
            strain = np.append(strain, np.linspace(
                0, thisPeak*scaleFactor, nSteps))
            strain = np.append(strain, np.linspace(
                thisPeak*scaleFactor, -thisPeak*scaleFactor, nSteps))
            strain = np.append(
                strain, np.linspace(-thisPeak*scaleFactor, 0, nSteps))

    return strain


peaksArray = np.array([.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5,
                      5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10])/10
# peaksArray=[1,10]
scaleFactor = 0.3
# scaleFactor = 0.3
nSteps = 60
nCycles = 2
strain = defineStrainHistory(peaksArray, scaleFactor, nSteps, nCycles)
plt.plot(strain)
strainMap['symmCycles'] = strain

plt.savefig("strain.png")


def formatAx(axModel, Title, xLabel, yLabel, titleFontSize=12, otherFontSize=12, legendLocation='best', backgroundColor='', legendFontSize=0, ncol=1):
    # Reference: Copyright Silvia Mazzoni, silviamazzoni@yahoo.com 2021
    plt.rc('font', size=3)
    plt.rc('font', size=3)
    if legendFontSize == 0:
        legendFontSize = otherFontSize
    axModel.grid(True, color='grey', linewidth=0.25)
    handles, labels = axModel.get_legend_handles_labels()
    if len(handles) > 0:
        axModel.legend(fontsize=legendFontSize, loc=legendLocation, ncol=ncol)
    axModel.set_title(Title, fontsize=titleFontSize)
    axModel.set_xlabel(xLabel, fontsize=otherFontSize)
    axModel.set_ylabel(yLabel, fontsize=otherFontSize)
    axModel.tick_params('x', labelsize=otherFontSize, rotation=0)
    axModel.tick_params('y', labelsize=otherFontSize, rotation=0)
    axModel.yaxis.set_ticks_position('left')
    axModel.xaxis.set_ticks_position('bottom')

    if not backgroundColor == '':
        axModel.set_facecolor(backgroundColor)


OpenSeesMaterialBaseValues = {}
OpenSeesMaterialDefaultValues = {}
M1 = 1784.2104208416836
M2 = round(1.12*M1, 1)
M3 = round(0.6*M1, 1)
M4 = M3
M5 = round(0.1*M1, 1)
M6 = M5
M7 = 0.01*M1
eps1 = 0.1
eps2 = 2.*eps1
eps3 = 4.*eps1
eps4 = 6.*eps1
eps5 = 8.*eps1
eps6 = 10.*eps1
eps7 = 12.*eps1


limitStateInput = ['-defoLimitStates', eps1, -eps1,
                   eps2, -eps2, '-forceLimitStates', M1, -M1, M2, -M2]
positiveEnvelope = [M1, eps1, M2, eps2, M3, eps3,
                    M4, eps4, M5, eps5, 100., eps6, 0, eps7]
negativeEnvelope = [-M1, -eps1, -M2, -eps2, -M3, -eps3]

OpenSeesMaterialBaseValues[f'HystereticSM'] = [
    'HystereticSM', '-posEnv', *positiveEnvelope, '-negEnv', *negativeEnvelope]
OpenSeesMaterialBaseValues[f'HystereticSMsymm'] = [
    'HystereticSM', '-posEnv', *positiveEnvelope]

for thisPinch in [[1, 1], [.2, .8], [.8, .2]]:
    OpenSeesMaterialDefaultValues[f'HystereticSM_pinch={thisPinch}'] = [
        'HystereticSM', '-posEnv', *positiveEnvelope, '-negEnv', *negativeEnvelope, '-pinch', *thisPinch]
for thisDamage1 in [0, 0.01, 0.1]:
    OpenSeesMaterialDefaultValues[f'HystereticSM_damage1={thisDamage1}'] = [
        'HystereticSM', '-posEnv', *positiveEnvelope, '-negEnv', *negativeEnvelope, '-damage', thisDamage1, 0]
for thisDamage2 in [0, 0.01, 0.1]:
    OpenSeesMaterialDefaultValues[f'HystereticSM_damage2={thisDamage2}'] = [
        'HystereticSM', '-posEnv', *positiveEnvelope, '-negEnv', *negativeEnvelope, '-damage', 0, thisDamage2]
for thisBeta in [0, 0.5, 1]:
    OpenSeesMaterialDefaultValues[f'HystereticSM_beta={thisBeta}'] = [
        'HystereticSM', '-posEnv', *positiveEnvelope, '-negEnv', *negativeEnvelope, '-beta', thisBeta]
dmg1a = 0.005
dmg2a = 0.002
for thisDegEnv in [0, 1, 5]:
    OpenSeesMaterialDefaultValues[f'HystereticSM_degEnv={thisDegEnv}'] = [
        'HystereticSM', '-posEnv', *positiveEnvelope, '-negEnv', *negativeEnvelope, '-damage', dmg1a, dmg2a, '-degEnv', thisDegEnv, -thisDegEnv]


AllStressStrain = {}

Nmaterials = len(OpenSeesMaterialDefaultValues.keys())
Ncols = 2
Nrows = int(Nmaterials/Ncols)
Nrows = 2

figSizeH = 2*Ncols
figSizeV = 2*Nrows
DPI = 200

thisCount = 0
allStrainArray = ['symmCycles']
iStrain = 0
for thisStrainLabel in allStrainArray:
    thisStrain = strainMap[thisStrainLabel]
    iStrain += 1
    iplt = 1
    for thisMaterial in [list(OpenSeesMaterialDefaultValues.keys())[0]]:
        print('--------------------------------------------')
        # print(thisMaterial)
        if iplt == 1:
            figEach = plt.figure(f'Material Response Each {thisMaterial} {thisStrainLabel}', figsize=(
                figSizeH, figSizeV), dpi=DPI, facecolor='w', edgecolor='k')
        iplt += 1
        axEach = figEach.add_subplot(Nrows, Ncols, iplt)

        counter = thisCount + 1
        ops.wipe()
        materialTag = 99

        inputArray = OpenSeesMaterialDefaultValues[thisMaterial]

        MaterialInput = inputArray[0], materialTag, *inputArray[1:]
        # print(f'ops.uniaxialMaterial{MaterialInput}')
        MaterialInputTcl = str(MaterialInput).replace(
            ',', ' ').replace('(', '').replace(')', '').replace("'", '')
        # print(f'uniaxialMaterial {MaterialInputTcl}')
        ops.uniaxialMaterial(*MaterialInput)

        ops.testUniaxialMaterial(materialTag)
        stress = []
        MUy = []
        for eps in thisStrain:
            ops.setStrain(eps)
            stress.append(ops.getStress())
            tangent = ops.getTangent()  # Not used

        thisCount = len(list(AllStressStrain.keys()))
        thisKey = 'Run' + str(thisCount+1) + ' ' + thisMaterial
        AllStressStrain[thisKey] = {}
        AllStressStrain[thisKey]['strain'] = thisStrain
        AllStressStrain[thisKey]['stress'] = stress

        with open("hysteresis.csv", "w", newline='') as f:
            write = csv.writer(f)
            write.writerow(["strain", "stress"])
            for x, y in zip(thisStrain, stress):
                write.writerow([x, y])

        backbone_file = "SPC1.csv"
        hysteresis_data = np.loadtxt(backbone_file, delimiter=',', skiprows=2)

        # Sort the data into a xy curve
        x = hysteresis_data[:, 1]*(1/280)
        y = hysteresis_data[:, 0]*40
        xy = np.column_stack([x, y])

        # Make a hysteresis object
        myHys = hys.Hysteresis(xy)

        # Plot the object to see if cycles are tested properly
        fig, ax = plt.subplots()
        myHys.plot(label='Experiment Hysteresis')

        MaterialInputStr = str(MaterialInput).replace(',', ',\n')
        line, = ax.plot(AllStressStrain[thisKey]['strain'], AllStressStrain[thisKey]
                        ['stress'], linewidth='1', label=MaterialInputStr, marker='', color="red")
        formatAx(ax, thisMaterial, 'Strain,Rotation,Curvature, or Deformation',
                 'Stress,Moment,Moment, or Force', 4, 4, 'best', 'lightgrey', 2)
        plt.savefig("FINAL_Steel01_opensees_hysteresis.png")
