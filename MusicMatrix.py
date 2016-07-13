import os
from music21 import midi, stream, note as mnote
import numpy

# The path holding all music files (midi, etc)
MUSIC_PATH = '/Users/ColeCanning/Documents/Git_Stuff/hackathon_2016/music/'

class MusicMatrix:
	def __init__(self, midi_file):
		fp = os.path.join(midi_file)
		mf = midi.MidiFile()
		mf.open(fp)
		mf.read()
		mf.close()
		# Properties
		self._notes = None
		self._value_lookup = None
		self._matrix = None
		self._stream = None
		self._matrix_probs = None
		# Initialize properties
		self._stream = midi.translate.midiFileToStream(mf)
		self._load_notes()
		self._load_value_lookup() 
		self._load_note_matrix()

	# Get all of the notes in a stream and their number of occurences.
	def _load_notes(self):
		self._notes = {}
		for note in self._stream.flat.notes:
			if type(note) is mnote.Note:
				if note.nameWithOctave in self._notes:
					self._notes[note.nameWithOctave]+= 1
				else:
					self._notes[note.nameWithOctave] = 0

	def _load_value_lookup(self):
		# build a marix out of the notes.
		# value_lookup holds the interger key that the note key relates to in the matrix.
		# just a layer of abstraction to make a matrix.
		self._value_lookup = {}
		i = -1
		for key in self._notes:
			i += 1
			self._value_lookup[key] = i

	def _load_note_matrix(self):
		self._matrix = [[0 for x in range(0,len(self._notes))] for i in range(0,len(self._notes))]
		self._matrix_probs = [[0 for x in range(0,len(self._notes))] for i in range(0,len(self._notes))]
		previousNoteName = None
		for note in self._stream.flat.notes:
			if type(note) is mnote.Note:
				noteName = note.nameWithOctave
				if previousNoteName:
					self._matrix[self._value_lookup[noteName]][self._value_lookup[previousNoteName]] += 1
				previousNoteName = noteName

	def build_prob_matrix(self):
		for i in range(0, len(self._matrix)):
			print i
			ssum = sum(self._matrix[i])
			for j in range(0, len(self._matrix[i])):
				self._matrix_probs[i][j] = float(self._matrix[i][j])/float(ssum)

	# def _reverse_lookup(self, value):
		# for key, val in self._notes.iteritems():
		# 	print key, val
		# 	if value == val:
		# 		return key

	def get_note_probs(self, note_index):
		return self._matrix_probs[note_index]

	def get_note_from_index(self, note_index):
		for key, val in self._value_lookup.iteritems():
			if note_index == val:
				return key


m = MusicMatrix(MUSIC_PATH + 'mary.mid')
print m._notes
print m._value_lookup
print m._matrix

m.build_prob_matrix()

print m._matrix_probs

NUM_NOTES = 100
DURATION = 100
SPACING = 100

print m.get_note_probs(0)

print m.get_note_from_index(0)

prev_note = 1 #D4
num_diff_notes = len(m._notes)
music_stream = stream.Stream()
for i in range(0, NUM_NOTES):
	# print 'i:', i
	probs = m.get_note_probs(prev_note)
	n = numpy.random.choice(numpy.arange(0, num_diff_notes), p=probs)
	# print n
	note = m.get_note_from_index(n)
	music_stream.append(mnote.Note(note, type='quarter'))
	prev_note = n

# Write the midi file!
fp = music_stream.write('midi', fp=MUSIC_PATH + 'my_song.midi')















