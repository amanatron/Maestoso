""" THIS FILE CONTAINS THE NOTE, INSTRUMENT AND TRACKLIST CLASSES"""


import pretty_midi
import mido 

#the note class assigned to each onset 
class Note:
    def __init__(self,pitch,start_time,end_time,velocity,ts,note_length,start_ticks,end_ticks):
        self.pitch = pitch
        self.start_time = start_time
        self.end_time = end_time
        self.velocity = velocity #intensity of the note 
        self.ts = ts #time signature 
        self.note_length = note_length #note length in integers - 1 = quarternote, etc 
        self.start_ticks = start_ticks 
        self.end_ticks = end_ticks


    def return_duration(self):
        return round(self.end_time - self.start_time,3)

    def return_numerator(self):
        return self.ts[0]
    
    def return_denominator(self):
        return self.ts[1]

#instrument class built from notes 
class Instrument:
    def __init__(self,notes,name,category,duration,specialcode, isdrum = False):
        self.notes = notes #all notes within the instrument 
        self.name = name 
        self.isdrum = isdrum #if instrument is a drum type 
        self.category = category #the category assigned to the instrument from MIDI information 
        self.duration = duration #the total duration of the instrument 
        self.colour = 'colour' #colour assigned to the instrument from  initialize_colours func in utility.py 
        self.active = True #True if instrument is active 
        self.specialcode = specialcode #a special code assigned to each instrument and all notes within it 

    def change_shape(self):
        pass 

    def change_colour(self):
        pass


class TrackList:
    def __init__(self,filedir):
        self.number_of_instruments = 0
        self.midifile = pretty_midi.PrettyMIDI(filedir) #create a midi file object 
        self.track_list = []
        self.PPQN = self.determine_ppqn(filedir)
        self.pulse = self.midifile.get_beats() #all the pulses retrieved using the midifile.get_beats() method 
        self.ts_changes = self.midifile.time_signature_changes #list of all time_signature changes 
        self.drum_count = 0 #how many drum tracks exist in a given tracklist 
        self.construct_tracklist()
        self.tempo_changes = self.midifile.get_tempo_changes() #retrieve all tempo changes 
        self.accented_beats = self.midifile.get_downbeats() #find all downbeats 
        self.selected_animation = ''
        
    #determine the PPQN of the tracklist 
    def determine_ppqn(self,filedir): 
        ppqn_mid = mido.MidiFile(filedir)
        return ppqn_mid.ticks_per_beat 

    def construct_tracklist(self):
        instrument_name = 'No Name'
        for i in self.midifile.instruments:
            self.number_of_instruments += 1
            instrument = []
            i.remove_invalid_notes()
            if i.name == 'No Name' and i.is_drum == False:
                instrument_name = "Instrument {}".format(self.number_of_instruments)
            elif i.name == 'No Name' and i.is_drum == True:
                self.drum_count += 1
                instrument_name = "Drum Instrument {}".format(self.drum_count)
            else:
                instrument_name = i.name 

            if len(self.ts_changes) == 1:
                for j in i.notes:
                    note_length = self.midifile.time_to_tick(j.duration)/self.PPQN
                    start_tick = self.midifile.time_to_tick(j.start)
                    end_tick = self.midifile.time_to_tick(j.end)
                    instrument.append(Note(j.pitch,j.start,j.end,j.velocity,(self.ts_changes[0].numerator,self.ts_changes[0].denominator),note_length,start_tick,end_tick))

            elif len(self.ts_changes) > 1: #add time signature information for each note 
                for j in range(len(self.ts_changes)):
                    if j != len(self.ts_changes) - 1:
                        for k in i.notes:
                            if k.start >= self.ts_changes[j].time and k.start < self.ts_changes[j+1].time:
                                note_length = self.midifile.time_to_tick(k.duration)/self.PPQN
                                start_tick = self.midifile.time_to_tick(k.start)
                                end_tick = self.midifile.time_to_tick(k.end)
                                if k.start < self.ts_changes[-1].time:
                                    instrument.append(Note(k.pitch,k.start,k.end,k.velocity,(self.ts_changes[j].numerator,self.ts_changes[j].denominator),note_length,start_tick,end_tick))
                                elif k.start >= self.ts_changes[-1].time:
                                    instrument.append(Note(k.pitch,k.start,k.end,k.velocity,(self.ts_changes[-1].numerator,self.ts_changes[-1].denominator),note_length,start_tick,end_tick))

            self.track_list.append(Instrument(instrument,instrument_name,i.program,i.get_end_time(),self.number_of_instruments,i.is_drum))



            






        






