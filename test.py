from pyo import *


# sf = SfPlayer("sounds/applause.wav", speed=1, loop=True).out()



def sine_wave():
	# Sine(self, freq=1000, phase=0, mul=1, add=0)
	# freq = frequency, phase = starting phase, mul = multiplier, add = dc offset
	a = Sine(freq=440).out()
	s.gui(locals())



def parallel_proc():

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
	# Creates a source (white noise)
	n = Noise()
	# Sends the bass frequencies (below 1000 Hz) to the left
	lp = ButLP(n).out()
	# Sends the high frequencies (above 1000 Hz) to the right
	hp = ButHP(n).out(1)
	s.gui(locals())



def fixed_control():
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




if __name__ == "__main__":
	s = Server().boot()
	s.start()

	#function here
	serial_proc()

	