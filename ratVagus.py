import PyPN
import matplotlib.pyplot as plt
from PyPN.takeTime import *
import numpy as np

# import cPickle as pickle
# import os

calculationFlag = True # run simulation or load latest bundle with this parameters (not all taken into account for identification)

upstreamSpikingOn = False
electricalStimulusOn = True

# set simulation params
tStop=100
timeRes=0.0025#0.0025

# set length of bundle and number of axons
lengthOfBundle = 80000#0
numberOfAxons = 1 # 1000

# set the diameter distribution or fixed value
# see http://docs.scipy.org/doc/numpy/reference/routines.random.html
# 5.7, 7.3, 8.7, 10., 11.5, 12.8, 14., 15., 16.
myelinatedDiam =  {'distName' : 'normal', 'params' : (2.0, 0.7)}
unmyelinatedDiam = {'distName' : 'normal', 'params' : (0.7, 0.3)}


intraParameters = {     'amplitude': 3., # 0.005, # 0.016,#0.2,# .0001,#1.5, #0.2, # 0.004, # 10., #  # Pulse amplitude (mA)
                        'frequency': 20., # Frequency of the pulse (kHz)
                        'dutyCycle': .5, # 0.05, # Percentage stimulus is ON for one period (t_ON = duty_cyle*1/f)
                        'stimDur' : 0.05, # Stimulus duration (ms)
                        'waveform': 'MONOPHASIC', # Type of waveform either "MONOPHASIC" or "BIPHASIC" symmetric
                        'timeRes' : timeRes,
                        'delay': 5, # ms
                        # 'invert': True
}

# axon parameters
myelinatedParameters = {'fiberD': myelinatedDiam, # um Axon diameter (5.7, 7.3, 8.7, 10.0, 11.5, 12.8, 14.0, 15.0, 16.0)
}

# axon parameters
unmyelinatedParameters = {'fiberD': unmyelinatedDiam, # um Axon diameter
}

# set all properties of the bundle
bundleParameters = {    'radius': 150, #150, #um Radius of the bundle (typically 0.5-1.5mm)
                        'length': lengthOfBundle, # um Axon length
                        # 'bundleGuide' : bundleGuide,
                        'randomDirectionComponent' : 0,

                        'numberOfAxons': numberOfAxons, # Number of axons in the bundle
                        'pMyel': .01,#0.01, # Percentage of myelinated fiber type A
                        'pUnmyel': .99, #.99, #Percentage of unmyelinated fiber type C
                        'paramsMyel': myelinatedParameters, #parameters for fiber type A
                        'paramsUnmyel': unmyelinatedParameters, #parameters for fiber type C

                        'tStop' : tStop,
                        'timeRes' : timeRes,

                        'saveI':False,
                        'saveV':False
}


if calculationFlag:

    # create the bundle with all properties of axons and recording setup
    bundle = PyPN.Bundle(**bundleParameters)

    # spiking through a single electrical stimulation
    if electricalStimulusOn:
        # stimulusInstance = PyPN.Stimulus(**stimulusParameters)
        # plt.plot(stimulusInstance.t, stimulusInstance.stimulusSignal)
        # plt.title('stimulus signal without delay')
        # plt.show()
        # bundle.add_excitation_mechanism(PyPN.StimCuff(**cuffParameters))
        bundle.add_excitation_mechanism(PyPN.StimIntra(**intraParameters))
        # bundle.add_excitation_mechanism(PyPN.SimpleIClamp(**stimulusParameters))

    # bundle.add_recording_mechanism(PyPN.RecCuff3D(radius=500, positionMax=0.8, sigma=1., width=2000, distanceOfRings=100, pointsPerRing=20))
    # bundle.add_recording_mechanism(PyPN.RecCuff3D(radius=500, positionMax=0.1, sigma=1., width=2000, distanceOfRings=100, pointsPerRing=20))
    # bundle.add_recording_mechanism(PyPN.RecCuff2D(radius=500, positionMax=0.2, sigma=5.))
    bundle.add_recording_mechanism(PyPN.RecBipolarPoint(radius=500, numberOfElectrodes=10 ,poleDistance=100, sigma=1., positionMax=1))


    # run the simulation
    bundle.simulate()

    # save the bundle to disk
    PyPN.save_bundle(bundle)
else:

    # try to open a bundle with the parameters set above
    # bundle = PyPN.open_recent_bundle(bundleParameters)
    bundle = PyPN.open_bundle_from_location('/media/carl/4ECC-1C44/PyPN/dt=0.0025 tStop=50 pMyel=0.000100999899 pUnmyel=0.999899000101 L=2000 nAxons=1000/bundle00000')

# bundle.clear_all_recording_mechanisms()
# # bundle.add_recording_mechanism(PyPN.RecCuff2D(radius=200, positionMax=0.2, sigma=1.))
# # investigate effect of bipolar electrode distance
# for poleDistance in np.arange(10, 1000, 20):
#     bundle.add_recording_mechanism(PyPN.RecCuff2D(radius=200, numberOfPoles=2, poleDistance=poleDistance, positionMax=0.2, sigma=1.))
#
# bundle.compute_CAPs_from_imem_files()
#
# # save the bundle to disk
# PyPN.save_bundle(bundle)
#
#
# # for i in range(len(bundle.recordingMechanisms)):
# for i in range(len(bundle.recordingMechanisms)): # -10,len(bundle.recordingMechanisms)):
#     PyPN.plot.CAP1D(bundle, recMechIndex=i)
#     # PyPN.plot.CAP1D_singleAxon(bundle, recMechIndex=i)

#
# PyPN.plot.geometry_definition(bundle)
# PyPN.plot.voltage(bundle)
PyPN.plot.CAP1D(bundle)
# PyPN.plot.voltage_one_myelinated_axon(bundle)
PyPN.plot.diameterHistogram(bundle)
# conVelDict = bundle.conduction_velocities(saveToFile=True) # (plot=False)
# pickle.dump(conVelDict,open( os.path.join(bundle.basePath, 'conductionVelocities.dict'), "wb" ))


# import matplotlib2tikz as mtz
# mtz.save('CAP.tex')

plt.show()

bundle = None