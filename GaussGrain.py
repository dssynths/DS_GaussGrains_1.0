''' This generatates a GaussGrain.
    @cf - center frequency
    @nocts - number of octaves to traverse over externally specificied durtation
    @comps - numbrer of harmonics (including fundamental)
    @amp - [0,1]
If the cf=100 and nocts = 1, then the range is 100*2^(-.5) to 100*2^(.5).
The duration must be set in the call to generate. 
'''
import numpy as np
#import seaborn as sns
from scipy import signal
import math
#import sys

from genericsynth import synthInterface as SI

class GaussGrain(SI.MySoundModel) :
	'''
		@cf - center frequency
		@nocts - number of octaves to traverse over externally specificied durtation
		@comps - numbrer of harmonics (including fundamental)
		@amp    - in [0,1]
	'''
	def __init__(self, cf=440, nocts=0, comps=1, amp=1) :
		SI.MySoundModel.__init__(self)
		#create a dictionary of the parameters this synth will use
		self.__addParam__("cf", 40, 2000, cf, 
                          synth_doc="center frequency in Hz")
		self.__addParam__("nocts", -3, 3, nocts,
                         synth_doc="frequency sweep in octaves centered around cf")
		self.__addParam__("comps", 1, 10, comps,
                         synth_doc="number of harmonic components including fundamental")
		self.__addParam__("amp", 0, 1, amp,
                         synth_doc="[0,1] amplitude")

	'''
		Override of base model method
	'''
	def generate(self, sigLenSecs, amp=None) :
		if amp==None : amp=self.getParam("amp")

		cf=self.getParam("cf")
		nocts=self.getParam("nocts")
		comps=self.getParam("comps")

		# envelope 
		length = int(round(sigLenSecs*self.sr))# in samples
		if length <=1 :
			print(f'warning: requesting window length of {length}, returning [0]')
			return np.zeros(1)

		ampenv=SI.gwindow(length)

		# The frequency sweep in units of octaves
		octs=np.linspace(-nocts/2., nocts/2., length, True)

		# Now generate each component with its different cf, and add them together
		signal = np.zeros(length)
		h = np.zeros(length)

        # the cumsum method is to acomodate constant frequency sweeps
		for harm in range(1,comps+1) :
			freqs=harm*cf*np.power(2.,octs)  #changes on every sample
			periods=freqs/self.sr  #portion of a period per (at each) sample
			cumstep=np.cumsum(periods)   #accumulated so we can pass it to sin
			h=np.array(np.sin(2*np.pi*cumstep))
			signal=signal+h  #add up the harmonics

		return amp*np.array(ampenv)*signal



