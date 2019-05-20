from pyo import *




###
### following pyo tutorials from 0.9.1 documentation
###


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













if __name__ == "__main__":
	#function here
	handling_channels_4()

	