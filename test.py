from pyo import *
import random




###
### following pyo tutorials from 0.9.1 documentation
###






###			   ###
### 01 - INTRO ###
###			   ###


def sine_wave():
	s = Server().boot()
	s.start()

	# Sine(self, freq=1000, phase=0, mul=1, add=0)
	# freq = frequency, phase = starting phase, mul = multiplier, add = dc offset
	a = Sine(freq=440).out()
	s.gui(locals())



def parallel_proc():
	s = Server().boot()
	s.start()

	# Creates a sine wave as the source to process.
	a = Sine()
	# Passes the sine wave through an harmonizer.
	hr = Harmonizer(a).out()
	# Also through a chorus.
	ch = Chorus(a).out()
	# And through a frequency shifter.
	sh = FreqShift(a).out()
	s.gui(locals())



def serial_proc():
	s = Server().boot()
	s.start()

	# Creates a sine wave as the source to process.
	a = Sine().out()
	# Passes the sine wave through an harmonizer.
	h1 = Harmonizer(a).out()
	# Then the harmonized sound through another harmonizer.
	h2 = Harmonizer(h1).out()
	# And again...
	h3 = Harmonizer(h2).out()
	# And again...
	h4 = Harmonizer(h3).out()
	sp = Scope(h1+h2+h3+h4)
	s.gui(locals())



def output_channels():
	s = Server().boot()
	s.start()

	# Creates a source (white noise)
	n = Noise()
	# Sends the bass frequencies (below 1000 Hz) to the left
	lp = ButLP(n).out()
	# Sends the high frequencies (above 1000 Hz) to the right
	hp = ButHP(n).out(1)
	s.gui(locals())


###				  ###
### 02 - CONTROLS ###
###				  ###


def fixed_control():
	s = Server().boot()
	s.start()

	# Sets fundamental frequency
	freq = 200

	# Approximates a triangle waveform by adding odd harmonics with
	# amplitude proportional to the inverse square of the harmonic number.
	h1 = Sine(freq=freq, mul=1).out()
	h2 = Sine(freq=freq*3, phase=0.5, mul=1./pow(3,2)).out()
	h3 = Sine(freq=freq*5, mul=1./pow(5,2)).out()
	h4 = Sine(freq=freq*7, phase=0.5, mul=1./pow(7,2)).out()
	h5 = Sine(freq=freq*9, mul=1./pow(9,2)).out()
	h6 = Sine(freq=freq*11, phase=0.5, mul=1./pow(11,2)).out()

	# Displays the final waveform
	sp = Scope(h1+h2+h3+h4+h5+h6)

	s.gui(locals())



def dynamic_control():
	s = Server().boot()
	s.start()

	# Creates two objects with cool parameters, one per channel.
	a = FM().out()
	b = FM().out(1)

	# Opens the controller windows.
	a.ctrl(title="Frequency modulation left channel")
	b.ctrl(title="Frequency modulation right channel")

	sc = Scope([a, b])

	s.gui(locals())



def output_range():
	s = Server().boot()
	s.start()

	# The `mul` attribute multiplies each sample by its value.
	a = Sine(freq=400, mul=0.1)

	# The `add` attribute adds an offset to each sample.
	# The multiplication is applied before the addition.
	b = Sine(freq=400, mul=0.5, add=0.5)

	# Using the range(min, max) method allows to automatically
	# compute both `mul` and `add` attributes.
	c = Sine(freq=400).range(-0.25, 0.5)

	# Displays the waveforms
	sc = Scope([a, b, c])

	s.gui(locals())



def building_lfo():
	s = Server().boot()
	s.start()

	# Creates a noise source
	n = Noise()

	# Creates an LFO oscillating +/- 500 around 1000 (filter's frequency)
	lfo1 = Sine(freq=.1, mul=500, add=1000)
	# Creates an LFO oscillating between 2 and 8 (filter's Q)
	lfo2 = Sine(freq=.4).range(2, 8)
	# Creates a dynamic bandpass filter applied to the noise source
	bp1 = ButBP(n, freq=lfo1, q=lfo2).out()

	# The LFO object provides more waveforms than just a sine wave

	# Creates a ramp oscillating +/- 1000 around 12000 (filter's frequency)
	lfo3 = LFO(freq=.25, type=1, mul=1000, add=1200)
	# Creates a square oscillating between 4 and 12 (filter's Q)
	lfo4 = LFO(freq=4, type=2).range(4, 12)
	# Creates a second dynamic bandpass filter applied to the noise source
	bp2 = ButBP(n, freq=lfo3, q=lfo4).out(1)

	s.gui(locals())



def math_ops():
	s = Server().boot()
	s.start()

	# Full scale sine wave
	a = Sine()

	# Creates a Dummy object `b` with `mul` attribute
	# set to 0.5 and leaves `a` unchanged.
	b = a * 0.5
	b.out()

	# Instance of Dummy class
	print(b)

	# Computes a ring modulation between two PyoObjects
	# and scales the amplitude of the resulting signal.
	c = Sine(300)
	d = a * c * 0.3
	d.out()

	# PyoObject can be used with Exponent operator.
	e = c ** 10 * 0.4
	e.out(1)

	# Displays the ringmod and the rectified signals.
	sp = Spectrum([d, e])
	sc = Scope([d, e])

	s.gui(locals())



def multichannel_expansion():
	### Using multichannel-expansion to create a square wave ###

	s = Server().boot()
	s.start()

	# Sets fundamental frequency.
	freq = 100
	# Sets the highest harmonic.
	high = 20

	# Generates the list of harmonic frequencies (odd only).
	harms = [freq * i for i in range(1, high) if i%2 == 1]
	# Generates the list of harmonic amplitudes (1 / n).
	amps = [0.33 / i for i in range(1, high) if i%2 == 1]

	# Creates all sine waves at once.
	a = Sine(freq=harms, mul=amps)
	# Prints the number of streams managed by "a".
	print(len(a))

	# The mix(voices) method (defined in PyoObject) mixes
	# the object streams into `voices` streams.
	b = a.mix(voices=1).out()

	# Displays the waveform.
	sc = Scope(b)

	s.gui(locals())


def extended_multichannel_expansion():
	# When using multichannel expansion with lists of different lengths, 
	# the longer list is used to set the number of streams and smaller lists will be wrap-around to fill the holes.

	s = Server().boot()
	s.start()

	# 12 streams with different combinations of `freq` and `ratio`.
	a = SumOsc(freq=[100, 150.2, 200.5, 250.7],
	           ratio=[0.501, 0.753, 1.255],
	           index=[.3, .4, .5, .6, .7, .4, .5, .3, .6, .7, .3, .5],
	           mul=.05)

	# Adds a stereo reverberation to the signal
	rev = Freeverb(a.mix(2), size=0.80, damp=0.70, bal=0.30).out()

	s.gui(locals())


# if a multi-streams object is given as an argument to another audio object, 
# the later will also be expanded in order to process all given streams. 
# This is really powerful to create polyphonic processes without copying long chunks of code but it can be very CPU expensive.

def handling_channels(): 
	# managing internal audio streams

	# The mix(voices) method of the PyoObject helps the handling of channels in order to save CPU cycles. 
	# Here, we down mix all streams to only two streams (to maintain the stereo) before processing the Chorus arguments.

	s = Server().boot()
	s.start()

	# Sets fundamental frequency and highest harmonic.
	freq = 100
	high = 20

	# Generates lists for frequencies and amplitudes
	harms = [freq * i for i in range(1, high) if i%2 == 1]
	amps = [0.33 / i for i in range(1, high) if i%2 == 1]

	# Creates a square wave by additive synthesis.
	a = Sine(freq=harms, mul=amps)
	print("Number of Sine streams: %d" % len(a))

	# Mix down the number of streams of "a" before computing the Chorus.
	b = Chorus(a.mix(2), feedback=0.5).out()
	print("Number of Chorus streams: %d" % len(b))

	s.gui(locals())



def handling_channels_2():
	# the out method and physical outputs

	# In a multichannel environment, we can carefully choose which stream goes to which output channel. 
	# To achieve this, we use the chnl and inc arguments of the out method.
	# chnl : Physical output assigned to the first audio stream of the object. inc : Output channel increment value.

	# Creates a Server with 8 channels
	s = Server(nchnls=8).boot() #i only have 2 channels on my output device :(

	# Generates a sine wave
	a = Sine(freq=500, mul=0.3)

	# Mixes it up to four streams
	b = a.mix(4)

	# Outputs to channels 0, 2, 4 and 6
	b.out(chnl=0, inc=2)

	s.gui(locals())



def handling_channels_3():
	# random multichannel outputs

	# If chnl is negative, streams begin at 0, increment the output number by inc and wrap around the global number of channels. 
	# Then, the list of streams is scrambled.

	# Creates a Server with 8 channels
	s = Server(nchnls=8).boot()

	amps = [.05,.1,.15,.2,.25,.3,.35,.4]

	# Generates 8 sine waves with
	# increasing amplitudes
	a = Sine(freq=500, mul=amps)

	# Shuffles physical output channels
	a.out(chnl=-1)

	s.gui(locals())



def handling_channels_4():
	# explicit control of physical outputs# Creates a Server with 8 channels
	s = Server(nchnls=8).boot()

	amps = [.05,.1,.15,.2,.25,.3,.35,.4]

	# Generates 8 sine waves with
	# increasing amplitudes
	a = Sine(freq=500, mul=amps)

	# Sets the output channels ordering
	a.out(chnl=[3,4,2,5,1,6,0,7])

	s.gui(locals())



###					###
### 03 - GENERATORS ###
###					###




def complex_oscs():
	# Blit: Impulse train generator with control over the number of harmonics.
	# RCOsc: Aproximation of a RC circuit (a capacitor and a resistor in series).
	# SineLoop: Sine wave oscillator with feedback.
	# SuperSaw: Roland JP-8000 Supersaw emulator.


	s = Server().boot()

	# Sets fundamental frequency.
	freq = 187.5

	# Impulse train generator.
	lfo1 = Sine(.1).range(1, 50)
	osc1 = Blit(freq=freq, harms=lfo1, mul=0.3)

	# RC circuit.
	lfo2 = Sine(.1, mul=0.5, add=0.5)
	osc2 = RCOsc(freq=freq, sharp=lfo2, mul=0.3)

	# Sine wave oscillator with feedback.
	lfo3 = Sine(.1).range(0, .18)
	osc3 = SineLoop(freq=freq, feedback=lfo3, mul=0.3)

	# Roland JP-8000 Supersaw emulator.
	lfo4 = Sine(.1).range(0.1, 0.75)
	osc4 = SuperSaw(freq=freq, detune=lfo4, mul=0.3)

	# Interpolates between input objects to produce a single output
	sel = Selector([osc1, osc2, osc3, osc4]).out()
	sel.ctrl(title="Input interpolator (0=Blit, 1=RCOsc, 2=SineLoop, 3=SuperSaw)")

	# Displays the waveform of the chosen source
	sc = Scope(sel)

	# Displays the spectrum contents of the chosen source
	sp = Spectrum(sel)

	s.gui(locals())



def band_limited_oscs():
	# Oscillators whose spectrum is kept under the Nyquist frequency.

	# LFO: can be used as a standard oscillators, at low freqs is a true LFO with various shapes:
	# 0 Saw up (default)
	# 1 Saw down
	# 2 Square
	# 3 Triangle
	# 4 Pulse
	# 5 Bipolar pulse
	# 6 Sample and hold
	# 7 Modulated Sine

	s = Server().boot()

	# Sets fundamental frequency.
	freq = 187.5

	# LFO applied to the `sharp` attribute
	lfo = Sine(.2, mul=0.5, add=0.5)

	# Various band-limited waveforms
	osc = LFO(freq=freq, sharp=lfo, mul=0.4).out()
	osc.ctrl()

	# Displays the waveform
	sc = Scope(osc)

	# Displays the spectrum contents
	sp = Spectrum(osc)

	s.gui(locals())



def fm_generators():
	# frequency modulation algorithm
	s = Server().boot()

	# FM implements the basic Chowning algorithm
	fm1 = FM(carrier=250, ratio=[1.5,1.49], index=10, mul=0.3)
	fm1.ctrl()

	# CrossFM implements a frequency modulation synthesis where the
	# output of both oscillators modulates the frequency of the other one.
	fm2 = CrossFM(carrier=250, ratio=[1.5,1.49], ind1=10, ind2=2, mul=0.3)
	fm2.ctrl()

	# Interpolates between input objects to produce a single output
	sel = Selector([fm1, fm2]).out()
	sel.ctrl(title="Input interpolator (0=FM, 1=CrossFM)")

	# Displays the spectrum contents of the chosen source
	sp = Spectrum(sel)

	s.gui(locals())



def noise_generators():
	# Noise: White noise generator, flat spectrum.
	# PinkNoise: Pink noise generator, 3dB rolloff per octave.
	# BrownNoise: Brown noise generator, 6dB rolloff per octave.
	s = Server().boot()

	# White noise
	n1 = Noise(0.3)

	# Pink noise
	n2 = PinkNoise(0.3)

	# Brown noise
	n3 = BrownNoise(0.3)

	# Interpolates between input objects to produce a single output
	sel = Selector([n1, n2, n3]).out()
	sel.ctrl(title="Input interpolator (0=White, 1=Pink, 2=Brown)")

	# Displays the spectrum contents of the chosen source
	sp = Spectrum(sel)

	s.gui(locals())



def strange_attractors():
	# A strange attractor is a system of three non-linear ordinary differential equations. 
	# These differential equations define a continuous-time dynamical system that exhibits chaotic dynamics 
	# associated with the fractal properties of the attractor.
	# bro what the fuck

	s = Server().boot()

	### Oscilloscope ###

	# LFO applied to the `chaos` attribute
	lfo = Sine(0.2).range(0, 1)

	# Rossler attractor
	n1 = Rossler(pitch=0.5, chaos=lfo, stereo=True)

	# Lorenz attractor
	n2 = Lorenz(pitch=0.5, chaos=lfo, stereo=True)

	# ChenLee attractor
	n3 = ChenLee(pitch=0.5, chaos=lfo, stereo=True)

	# Interpolates between input objects to produce a single output
	sel = Selector([n1, n2, n3])
	sel.ctrl(title="Input interpolator (0=Rossler, 1=Lorenz, 2=ChenLee)")

	# Displays the waveform of the chosen attractor
	sc = Scope(sel)

	### Audio ###

	# Lorenz with very low pitch value that acts as a LFO
	freq = Lorenz(0.005, chaos=0.7, stereo=True, mul=250, add=500)
	a = Sine(freq, mul=0.3).out()

	s.gui(locals())



def random_generators():
	s = Server().boot()

	# Two streams of midi pitches chosen randomly in a predefined list.
	# The argument `choice` of Choice object can be a list of lists to
	# list-expansion.
	mid = Choice(choice=[60,62,63,65,67,69,71,72], freq=[2,3])

	# Two small jitters applied on frequency streams.
	# Randi interpolates between old and new values.
	jit = Randi(min=0.993, max=1.007, freq=[4.3,3.5])

	# Converts midi pitches to frequencies and applies the jitters.
	fr = MToF(mid, mul=jit)

	# Chooses a new feedback value, between 0 and 0.15, every 4 seconds.
	fd = Randi(min=0, max=0.15, freq=0.25)

	# RandInt generates a pseudo-random integer number between 0 and `max`
	# values at a frequency specified by `freq` parameter. It holds the
	# value until the next generation.
	# Generates an new LFO frequency once per second.
	sp = RandInt(max=6, freq=1, add=8)
	# Creates an LFO oscillating between 0 and 0.4.
	amp = Sine(sp, mul=0.2, add=0.2)

	# A simple synth...
	a = SineLoop(freq=fr, feedback=fd, mul=amp).out()

	s.gui(locals())




###				 ###
### 06 - FILTERS ###
###				 ###

def lowpass_filters():
	# Tone : IIR first-order lowpass
	# ButLP : IIR second-order lowpass (Butterworth)
	# MoogLP : IIR fourth-order lowpass (+ resonance as an extra parameter)

	s = Server().boot()

	# White noise generator
	n = Noise(.5)

	# Common cutoff frequency control
	freq = Sig(1000)
	freq.ctrl([SLMap(50, 5000, "lin", "value", 1000)], title="Cutoff Frequency")

	# Three different lowpass filters
	tone = Tone(n, freq)
	butlp = ButLP(n, freq)
	mooglp = MoogLP(n, freq)

	# Interpolates between input objects to produce a single output
	sel = Selector([tone, butlp, mooglp]).out()
	sel.ctrl(title="Filter selector (0=Tone, 1=ButLP, 2=MoogLP)")

	# Displays the spectrum contents of the chosen source
	sp = Spectrum(sel)

	s.gui(locals())



def bandpass_filters():
	# This example illustrates the difference between a simple IIR second-order bandpass filter and a cascade of second-order bandpass filters. 
	# A cascade of four bandpass filters with a high Q can be used as a efficient resonator on the signal.

	s = Server().boot()

	# White noise generator
	n = Noise(.5)

	# Common cutoff frequency control
	freq = Sig(1000)
	freq.ctrl([SLMap(50, 5000, "lin", "value", 1000)], title="Cutoff Frequency")

	# Common filter's Q control
	q = Sig(5)
	q.ctrl([SLMap(0.7, 20, "log", "value", 5)], title="Filter's Q")

	# Second-order bandpass filter
	bp1 = Reson(n, freq, q=q)
	# Cascade of second-order bandpass filters
	bp2 = Resonx(n, freq, q=q, stages=4)

	# Interpolates between input objects to produce a single output
	sel = Selector([bp1, bp2]).out()
	sel.ctrl(title="Filter selector (0=Reson, 1=Resonx)")

	# Displays the spectrum contents of the chosen source
	sp = Spectrum(sel)

	s.gui(locals())



def complex_resonator():
	s = Server().boot()

	# Six random frequencies.
	freqs = [random.uniform(1000, 3000) for i in range(6)]

	# Six different plucking speeds.
	pluck = Metro([.9,.8,.6,.4,.3,.2]).play()

	# LFO applied to the decay of the resonator.
	decay = Sine(.1).range(.01, .15)

	# Six ComplexRes filters.
	rezos = ComplexRes(pluck, freqs, decay, mul=5).out()

	# Change chime frequencies every 7.2 seconds
	def new():
	    freqs = [random.uniform(1000, 3000) for i in range(6)]
	    rezos.freq = freqs
	pat = Pattern(new, 7.2).play()

	s.gui(locals())


def phasing():
	# A phaser is an electronic sound processor used to filter a signal by creating a series of peaks and troughs in the frequency spectrum. 
	# The position of the peaks and troughs of the waveform being affected is typically modulated so that they vary over time, 
	# creating a sweeping effect. For this purpose, phasers usually include a low-frequency oscillator.

	s = Server().boot()

	# Simple fadein.
	fade = Fader(fadein=.5, mul=.2).play()

	# Noisy source.
	a = PinkNoise(fade)

	# These LFOs modulate the `freq`, `spread` and `q` arguments of
	# the Phaser object. We give a list of two frequencies in order
	# to create two-streams LFOs, therefore a stereo phasing effect.
	lf1 = Sine(freq=[.1, .15], mul=100, add=250)
	lf2 = Sine(freq=[.18, .13], mul=.4, add=1.5)
	lf3 = Sine(freq=[.07, .09], mul=5, add=6)

	# Apply the phasing effect with 20 notches.
	b = Phaser(a, freq=lf1, spread=lf2, q=lf3, num=20, mul=.5).out()

	s.gui(locals())



















if __name__ == "__main__":
	#function here
	complex_oscs()

	