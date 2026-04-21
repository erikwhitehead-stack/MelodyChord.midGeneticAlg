import random
import math
from midiutil import MIDIFile
from datetime import datetime
from operator import attrgetter

# # Sort by a single attribute
# objects.sort(key=attrgetter('attribute_name'))

POPULATION = 100
GENERATIONS = 200

notesInKey = [60, 62, 64, 65, 67, 69, 71, 72, 74, 74, 76, 77, 79, 81, 83, 84]
TRACK = 0
TEMPO = 120
VOLUME = 100
CHORD_DURATION = 4
currentGeneration = 0


class NoteObject:
    def __init__(self, channel, note, time, duration):
        self.channel = channel
        self.note = note
        self.time = time
        self.duration = duration
    def setNote(self, note):
        self.note = note
    def setTime(self, time):
        self.time = time

class MelodyChordPair:
    def __init__(self, melody=None, chords=None, fitness=0):
        self.melody = melody
        if self.melody == None:
            self.melody = generateMelody()
        self.chords = chords
        if self.chords == None:
            self.chords = generateChords()
        self.fitness = fitness


    # evaluates the fitness for the melody + chord pair
    def evaluateFitness(self):
        fitness = 0     

        # Chord Fitness
        chord1 = []
        chord2 = []
        chord3 = []
        chord4 = []
        chord5 = []

        for item in self.chords:
            if item.time < 4:
                chord1.append(item.note)
            elif item.time < 8:
                chord2.append(item.note)
            elif item.time < 12:
                chord3.append(item.note)
            elif item.time < 16:
                chord4.append(item.note)
            else:
                chord5.append(item.note)
        allChords = [chord1, chord2, chord3, chord4, chord5]

        # check for well known chord structures
        for thisChord in allChords:
            # check for thirds intervals:
            #   C                                                           E
            if (60 in thisChord or 72 in thisChord or 84 in thisChord) and (64 in thisChord or 76 in thisChord):
                fitness = fitness + 1
            #   D                                       F
            if (62 in thisChord or 74 in thisChord) and (65 in thisChord or 77 in thisChord):
                fitness = fitness + 0.5
            #   E                                       G
            if (64 in thisChord or 76 in thisChord) and (67 in thisChord or 79 in thisChord):
                fitness = fitness + 0.5
            #   F                                       A
            if (65 in thisChord or 77 in thisChord) and (69 in thisChord or 81 in thisChord):
                fitness = fitness + 0.5
            #   G                                       B
            if (67 in thisChord or 79 in thisChord) and (71 in thisChord or 83 in thisChord):
                fitness = fitness + 1
            #   A                                       C
            if (69 in thisChord or 81 in thisChord) and (60 in thisChord or 72 in thisChord or 84 in thisChord):
                fitness = fitness + 0.5
            #   B                                       D
            if (71 in thisChord or 83 in thisChord) and (62 in thisChord or 74 in thisChord):
                fitness = fitness + 0.5
            
            # check for fifths intervals:
            #   C                                                           G
            if (60 in thisChord or 72 in thisChord or 84 in thisChord) and (67 in thisChord or 79 in thisChord):
                fitness = fitness + 1
            #   D                                       A
            if (62 in thisChord or 74 in thisChord) and (69 in thisChord or 81 in thisChord):
                fitness = fitness + 0.5
            #   E                                       B
            if (64 in thisChord or 76 in thisChord) and (71 in thisChord or 83 in thisChord):
                fitness = fitness + 0.5
            #   F                                       C
            if (65 in thisChord or 77 in thisChord) and (60 in thisChord or 72 in thisChord or 84 in thisChord):
                fitness = fitness + 0.5
            #   G                                       D
            if (67 in thisChord or 79 in thisChord) and (62 in thisChord or 74 in thisChord):
                fitness = fitness + 1
            #   A                                       E
            if (69 in thisChord or 81 in thisChord) and (64 in thisChord or 76 in thisChord):
                fitness = fitness + 0.5
            #   B                                       F
            if (71 in thisChord or 83 in thisChord) and (65 in thisChord or 77 in thisChord):
                fitness = fitness + 0.5

            # Major and minor chords
            # C Major C E G
            if (60 in thisChord or 72 in thisChord or 84 in thisChord) and (64 in thisChord or 76 in thisChord) and (67 in thisChord or 79 in thisChord):
                fitness = fitness + 3
            # D minor D F A
            if (62 in thisChord or 74 in thisChord) and (65 in thisChord or 77 in thisChord) and (69 in thisChord or 81 in thisChord):
                fitness = fitness + 3
            # E minor E G B
            if (64 in thisChord or 76 in thisChord) and (67 in thisChord or 79 in thisChord) and (71 in thisChord or 83 in thisChord):
                fitness = fitness + 3
            # F Major F A C
            if (65 in thisChord or 77 in thisChord) and (69 in thisChord or 81 in thisChord) and (60 in thisChord or 72 in thisChord or 84 in thisChord):
                fitness = fitness + 3
            # G Major G B D
            if (67 in thisChord or 79 in thisChord) and (71 in thisChord or 83 in thisChord) and (62 in thisChord or 74 in thisChord):
                fitness = fitness + 3
            # A Minor A C E
            if (69 in thisChord or 81 in thisChord) and (60 in thisChord or 72 in thisChord or 84 in thisChord) and (64 in thisChord or 76 in thisChord):
                fitness = fitness + 3
            # B dim B D F
            if (71 in thisChord or 83 in thisChord) and (62 in thisChord or 74 in thisChord) and (65 in thisChord or 77 in thisChord):
                fitness = fitness + 3

            # Major and minor 7th chords
            # C Major7 C E G B
            if (60 in thisChord or 72 in thisChord or 84 in thisChord) and (64 in thisChord or 76 in thisChord) and (67 in thisChord or 79 in thisChord) and (71 in thisChord or 83 in thisChord):
                fitness = fitness + 4
            # D minor7 D F A C
            if (62 in thisChord or 74 in thisChord) and (65 in thisChord or 77 in thisChord) and (69 in thisChord or 81 in thisChord) and (60 in thisChord or 72 in thisChord or 84 in thisChord):
                fitness = fitness + 4
            # E minor7 E G B D
            if (64 in thisChord or 76 in thisChord) and (67 in thisChord or 79 in thisChord) and (71 in thisChord or 83 in thisChord) and (62 in thisChord or 74 in thisChord):
                fitness = fitness + 4
            # F Major7 F A C E
            if (65 in thisChord or 77 in thisChord) and (69 in thisChord or 81 in thisChord) and (60 in thisChord or 72 in thisChord or 84 in thisChord) and (64 in thisChord or 76 in thisChord):
                fitness = fitness + 4
            # G Major7 G B D F
            if (67 in thisChord or 79 in thisChord) and (71 in thisChord or 83 in thisChord) and (62 in thisChord or 74 in thisChord) and (65 in thisChord or 77 in thisChord):
                fitness = fitness + 4
            # A Minor7 A C E G
            if (69 in thisChord or 81 in thisChord) and (60 in thisChord or 72 in thisChord or 84 in thisChord) and (64 in thisChord or 76 in thisChord) and (67 in thisChord or 79 in thisChord):
                fitness = fitness + 4
            # B dim7b5 B D F A
            if (71 in thisChord or 83 in thisChord) and (62 in thisChord or 74 in thisChord) and (65 in thisChord or 77 in thisChord) and (69 in thisChord or 81 in thisChord):
                fitness = fitness + 4

            # the 4th and 5th bar should be similar
            if chord5[0] in chord4:
                fitness = fitness + 1
            if chord5[0] in chord4 and chord5[1] in chord4:
                fitness = fitness + 2
            if chord5[0] in chord4 and chord5[1] in chord4 and chord5[2] in chord4:
                fitness = fitness + 3
            if chord5[0] in chord4 and chord5[1] in chord4 and chord5[2] in chord4 and chord5[3] in chord4:
                fitness = fitness - 5
            

        # melody fitness
        sixteenthNotes = 0
        eighthNotes = 0
        quarterNotes = 0
        halfNotes = 0
        time = 0
        prevItem = None
        melodyChord1Notes = []
        melodyChord2Notes = []
        melodyChord3Notes = []
        melodyChord4Notes = []
        melodyChord5Notes = []
        

        for item in self.melody:

            # tracks the notes used in each section of the melody
            if item.time < 4 and item.note not in melodyChord1Notes:
                melodyChord1Notes.append(item.note)
            elif item.time < 8 and item.note not in melodyChord2Notes:
                melodyChord2Notes.append(item.note)
            elif item.time < 12 and item.note not in melodyChord3Notes:
                melodyChord3Notes.append(item.note)
            elif item.time < 16 and item.note not in melodyChord4Notes:
                melodyChord4Notes.append(item.note)
            elif item.time < 20 and item.note not in melodyChord5Notes:
                melodyChord5Notes.append(item.note)

            if prevItem is not None:
                noteDifferential = abs(item.note - prevItem.note)
                if noteDifferential == 0:
                    fitness -= 2
            else:
                noteDifferential = 0
            
            # the melody should follow the notes of the chord
            if time < 4:
                if item.note in chord1:
                    if item.duration == 0.25:
                        fitness += 1
                    elif item.duration == 0.5:
                        fitness += 2
                    elif item.duration == 1:
                        fitness += 4
                    elif item.duration == 2:
                        fitness += 4
            elif time < 8:
                if item.note in chord2:
                    if item.duration == 0.25:
                        fitness += 1
                    elif item.duration == 0.5:
                        fitness += 2
                    elif item.duration == 1:
                        fitness += 4
                    elif item.duration == 2:
                        fitness += 4
            elif time < 12:
                if item.note in chord3:
                    if item.duration == 0.25:
                        fitness += 1
                    elif item.duration == 0.5:
                        fitness += 2
                    elif item.duration == 1:
                        fitness += 4
                    elif item.duration == 2:
                        fitness += 4
            elif time < 16:
                if item.note in chord4:
                    if item.duration == 0.25:
                        fitness += 1
                    elif item.duration == 0.5:
                        fitness += 2
                    elif item.duration == 1:
                        fitness += 4
                    elif item.duration == 2:
                        fitness += 4
            
            # there should be a similar amount of each note type 
            # the pitch gap between notes should not be too large
            if item.duration == 0.25:
                sixteenthNotes += 0.25
                if noteDifferential < 4:
                    fitness += 1
                elif noteDifferential > 8:
                    fitness -= 2
            elif item.duration == 0.5:
                eighthNotes += 0.5
                if noteDifferential < 8:
                    fitness += 2
            elif item.duration == 1:
                quarterNotes += 1
                if noteDifferential < 10:
                    fitness += 4
            elif item.duration == 2:
                halfNotes += 2
                if noteDifferential < 14:
                    fitness += 5
            prevItem = item
        
        
        allMelodyNotes = [melodyChord1Notes, melodyChord2Notes, melodyChord3Notes, melodyChord4Notes, melodyChord5Notes]
        # if the melody only contain chord notes or not enough, punish it
        for index in range(len(allMelodyNotes)):
            chordNotes = 0
            totalNotes = 0
            for note in allMelodyNotes[index]:
                if note in allChords[index]:
                    chordNotes += 1
                    totalNotes += 1
                else:
                    totalNotes += 1
            if chordNotes / totalNotes < .6:
                fitness -= 5
            elif chordNotes / totalNotes > .8:
                fitness -= 5


        # there should be a similar amount of each note type
        mean = (sixteenthNotes + eighthNotes + quarterNotes + halfNotes) / 4
        stdDev = math.sqrt( (((sixteenthNotes-mean)**2) + ((eighthNotes-mean)**2) + ((quarterNotes-mean)**2) + ((halfNotes-mean)**2)) / 3 )
        if stdDev < 1:
            fitness += 8
        elif stdDev < 3:
            fitness += 2
        else:
            fitness -= 5

        self.fitness = fitness
        return self.fitness

    # 8% mutation rate per note in the melody/chord
    def mutate(self):
        melodyDurations = [0.25, 0.5, 1, 2]
        melodyDurationsLess = [0.25, 0.5, 1]
        mutatedMelody = []
        time = 0
        mutatedTime = 0
        for item in self.melody:
            # Change the note of the melody
            if mutatedTime == time:
                if random.randint(1,100) <= 5:
                    mutatedMelody.append(NoteObject(0,random.choice(notesInKey),item.time, item.duration))
                    mutatedTime += item.duration
                # change the type of note with new one and new pitch
                elif (random.randint(1,100) <= 3) and time%1 == 0:
                    newNoteType = random.choice(melodyDurations)
                    if newNoteType == 2 and mutatedTime<19:
                        note = random.choice(notesInKey)
                        mutatedMelody.append(NoteObject(0, note, mutatedTime, newNoteType))
                        mutatedTime += newNoteType
                    elif newNoteType == 0.25:
                        for notes in range(4):
                            note = random.choice(notesInKey)
                            mutatedMelody.append(NoteObject(0, note, mutatedTime, newNoteType))
                            mutatedTime += newNoteType
                    elif newNoteType == 0.5:
                        for notes in range(2):
                            note = random.choice(notesInKey)
                            mutatedMelody.append(NoteObject(0, note, mutatedTime, newNoteType))
                            mutatedTime += newNoteType
                    elif newNoteType == 1:
                        note = random.choice(notesInKey)
                        mutatedMelody.append(NoteObject(0, note, mutatedTime, newNoteType))
                        mutatedTime += newNoteType
                else:
                    mutatedMelody.append(item)
                    mutatedTime += item.duration
            
            elif mutatedTime < time:
                newNoteType = random.choice(melodyDurationsLess)
                if newNoteType == 0.25:
                    for notes in range(4):
                        note = random.choice(notesInKey)
                        mutatedMelody.append(NoteObject(0, note, mutatedTime, newNoteType))
                        mutatedTime += newNoteType
                elif newNoteType == 0.5:
                    for notes in range(2):
                        note = random.choice(notesInKey)
                        mutatedMelody.append(NoteObject(0, note, mutatedTime, newNoteType))
                        mutatedTime += newNoteType
                elif newNoteType == 1:
                    note = random.choice(notesInKey)
                    mutatedMelody.append(NoteObject(0, note, mutatedTime, newNoteType))
                    mutatedTime += newNoteType
            elif mutatedTime > time:
                prevItem = item
            
            time += item.duration
            prevItem = item
            if mutatedTime >= 20:
                break
        while mutatedTime<20:
            newNoteType = random.choice(melodyDurationsLess)
            if newNoteType == 0.25:
                for notes in range(4):
                    note = random.choice(notesInKey)
                    mutatedMelody.append(NoteObject(0, note, mutatedTime, newNoteType))
                    mutatedTime += newNoteType
            elif newNoteType == 0.5:
                for notes in range(2):
                    note = random.choice(notesInKey)
                    mutatedMelody.append(NoteObject(0, note, mutatedTime, newNoteType))
                    mutatedTime += newNoteType
            elif newNoteType == 1:
                note = random.choice(notesInKey)
                mutatedMelody.append(NoteObject(0, note, mutatedTime, newNoteType))
                mutatedTime += newNoteType
            

        # chord mutation, 7% chance per note to mutate
        mutatedChords = []
        for item in self.chords:
            if random.randint(1,100) < 8:
                mutatedChords.append(NoteObject(0,random.choice(notesInKey),item.time, item.duration))
            else:
                mutatedChords.append(item)
        
        self.chords = mutatedChords
        self.melody = mutatedMelody
        return

    def createMidi(self):
        melodyFile = MIDIFile(1) 
        chordFile = MIDIFile(1)

        for item in self.melody:
            melodyFile.addNote(TRACK, item.channel, item.note, item.time, item.duration, VOLUME)
        for item in self.chords:
            chordFile.addNote(TRACK, item.channel, item.note, item.time, item.duration, VOLUME)

        now = datetime.now()
        currentTime = now.strftime("%Y-%m-%d %H-%M-%S ")
        fileMelodyName =  currentTime + "Melody.mid"
        fileChordName = currentTime + "Chords.mid"

        with open(fileChordName, "wb") as output_file2:
            chordFile.writeFile(output_file2)
        with open(fileMelodyName, "wb") as output_file1:
            melodyFile.writeFile(output_file1)



def generateChords():
    newChords = []
    time = 0
    for bars in range(5):
        for channel in range(4):
            note = random.choice(notesInKey)
            newChords.append(NoteObject(channel, note, time, CHORD_DURATION))
        time = time + 4
    return newChords


def generateMelody():
    melodyDurations = [0.25, 0.5, 1, 2]
    melodyDurationsLess = [0.25, 0.5, 1]
    time = 0
    newMelody = []
    while time < 20:
        if time == 19:
            noteType = random.choice(melodyDurationsLess)
        else:
            noteType = random.choice(melodyDurations)
        match noteType:
            case 0.25:
                for notes in range(4):
                    note = random.choice(notesInKey)
                    newMelody.append(NoteObject(0, note, time, noteType))
                    time = time + noteType
            case 0.5:
                for notes in range(2):
                    note = random.choice(notesInKey)
                    newMelody.append(NoteObject(0, note, time, noteType))
                    time = time + noteType
            case 1:
                note = random.choice(notesInKey)
                newMelody.append(NoteObject(0, note, time, noteType))
                time = time + noteType
            case 2:
                note = random.choice(notesInKey)
                newMelody.append(NoteObject(0, note, time, noteType))
                time = time + noteType
            case _:
                print("melody generation failed selecting duration")
                return 
    return newMelody
        

def crossoverRoulette(population):
    survivorPopulation = []
    newPopulation = []
    index = 0
    # keep the top 25% of the population in the new population
    while index < POPULATION/4:
        survivorPopulation.append(population[index])
        newPopulation.append(population[index])
        index = index + 1
    while index < POPULATION:
        survivorPopulation.append(population[index])
        index = index + 1
    
    # take each of the top 50% of population, and breed them with anyone in the population
    for survivorIndex in range(len(survivorPopulation)):
        parent1 = survivorPopulation[survivorIndex]
        parent2 = random.choice(survivorPopulation)
        childMelody = []
        childChords = []
        if survivorIndex > POPULATION/2:
            break

        # loop through the notes in the parent melody and append to child melody
        # take first 3 bars of parent1 and last 2 bars of parent 2
        for item in parent1.melody:
            if item.time < 12:
                childMelody.append(item)
            else: break
        for item in parent2.melody:
            if item.time >= 12 and item.time < 20:
                childMelody.append(item)
        
        # take first 3 bars of parent1 and last 2 bars of parent 2
        for item in parent1.chords:
            if item.time < 12:
                childChords.append(item)
            else: break
        for item in parent2.chords:
            if item.time >= 12 and item.time < 20:
                childChords.append(item)


        child = MelodyChordPair(childMelody, childChords)
        # the 50 children made will be added to the new population
        newPopulation.append(child)

# class MelodyChordPair:
#     def __init__(self, melody=None, chords=None, fitness=0):

    # the 25 now vacant slots in the population will be randomly generated
    while len(newPopulation) < POPULATION:
        newPopulation.append(MelodyChordPair())
    while len(newPopulation) > POPULATION:
        print("Population generated by crossover is too big" + str(len(newPopulation)))
        newPopulation.pop()

    return newPopulation

def generatePopulation():
    newPopulation = []
    for i in range(POPULATION):
        newPopulation.append(MelodyChordPair())
    return newPopulation

def sortPopulation(population):
    population.sort(key=attrgetter('fitness'))
    population.reverse()
    return




currentGenerationFitness = 0
currentGenerationFitnessImprovement = 0

population = generatePopulation()
for melodyChordPair in population:
        melodyChordPair.evaluateFitness()
sortPopulation(population)

for i in range(GENERATIONS):
    
    population = crossoverRoulette(population)

    keepTopFive=0    
    for melodyChordPair in population:
        if keepTopFive>5:
            melodyChordPair.mutate()
            melodyChordPair.evaluateFitness()
        else: 
            keepTopFive +=1
            melodyChordPair.evaluateFitness()

    sortPopulation(population)
    currentGeneration = currentGeneration + 1
    


    if currentGeneration%20 == 0:
        print("Current Generation: " + str(currentGeneration) + "    Current Best Fitness: " + str(population[0].fitness))

    if currentGenerationFitness < population[0].fitness:
        currentGenerationFitness = population[0].fitness
        currentGenerationFitnessImprovement = 0
    elif currentGenerationFitness == population[0]:
        currentGenerationFitnessImprovement += 1
    
    if currentGenerationFitnessImprovement > 100:
        break
    


population[0].createMidi()


