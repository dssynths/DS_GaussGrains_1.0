import numpy as np
import math

from genericsynth import synthInterface as SI
from GaussGrain import GaussGrain  # This is "event" synthesizer this pattern synth will use



#################################################################################### 
class GaussGrains_0001(SI.MySoundModel) :

    def __init__(self, cf_exp=0, nocts=0, rate_exp=0, irreg_exp=1, durdutyexp=.25, cfrangeocts=0, comps=1, evamp=.5, rngseed=18005551212) :

        SI.MySoundModel.__init__(self, rngseed=rngseed)
        
        #create a dictionary of the parameters this synth will use
        #cf_exp is number of octaves relative to 440 cps
        self.__addParam__("cf_exp", -2, 2, cf_exp,
                lambda v :
                    self.evSynth.setParam('cf', SI.oct2freq(v)),
                synth_doc="[-1,1]-> 440*2^(n) Hz")

        self.__addParam__("rate_exp", -1, 4, rate_exp,
                synth_doc="[-1,4]-> 2^(n) events per second")
        
        self.__addParam__("irreg_exp", 0, 1, irreg_exp,
                synth_doc="[0,1]-> [0-1]/event-per-second] standard deviation of gaussian")

        self.__addParam__("durdutyexp", -3, 3, durdutyexp,
                synth_doc="[-1,0]-> 2^(n) event duration as a portion of computed inter-onset interval")
        
        self.__addParam__("cfrangeocts", 0, 3, cfrangeocts,
                synth_doc="[0,2]-> range in octaves of event frequencies around center frequency")

        self.__addParam__('comps', 1, 10, comps,
                synth_doc="[1, 10]-> number of sine wave components")

        self.__addParam__("nocts", -3,3,nocts,
                lambda v :
                    self.evSynth.setParam('nocts', v),
                synth_doc="[-3, 3]-> number of octaves for frequency sweep around cf")
        
        #create the sub synth
        self.evSynth=GaussGrain(SI.oct2freq(self.getParam("cf_exp")), self.getParam("nocts"), self.getParam("comps"))             
        self.evSynth.setParam('amp', .75) #should be smaller for overlapping events...

    #-----------
    # Override of base model method
    def generate(self,  durationSecs) :
        elist=SI.noisySpacingTimeList(self.getParam("rate_exp"), self.getParam("irreg_exp"), durationSecs, self.rng.integers(2**32))
        return self.elist2signal(elist, durationSecs)

    
    #-----------
    def elist2signal(self, elist, sigLenSecs) :
        ''' 
            Take a list of event times, and return our signal of gaussian grains
        '''
        numSamples=self.sr*sigLenSecs
        sig=np.zeros(sigLenSecs*self.sr)
        cfrangeocts=self.getParam("cfrangeocts")

        hi=lo=SI.oct2freq(self.getParam("cf_exp"))
        
        numevents=len(elist)
        for i in range(numevents) :
            nf=elist[i]
            if (i+1)==numevents :
                nextnf=sigLenSecs
            else :
                nextnf=elist[i+1]
 

            # create some deviation in center frequency
            perturbedCf = SI.oct2freq(self.getParam("cf_exp")+cfrangeocts*(self.rng.random()-.5))
            if perturbedCf > hi : hi= perturbedCf
            if perturbedCf < lo : lo= perturbedCf
                
            self.evSynth.setParam("cf", perturbedCf)

            # use durdutyexp as random interval dependent durdutyexp cycle
            siglength = (2**self.getParam("durdutyexp"))*(nextnf-nf)
            if 2 > siglength*self.sr :
                print(f':: elist2signal: warning, reqesting event length of {siglength}, -> {siglength*self.sr} samples - skipping')
                print(f'   self.getParam("durdutyexp") = {self.getParam("durdutyexp")}')
                print(f'   nf = {nf}, nextnf = {nextnf}, sigLenSecs = {sigLenSecs}')
                return np.zeros(1)
            gensig = self.evSynth.generate(siglength)
            
            startsamp=int(round(nf*self.sr))%numSamples
            sig = SI.addin(gensig, sig, startsamp)

        print(f' seq hi freq = {hi}, and lo = {lo}')
        return sig
