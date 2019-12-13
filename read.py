import os
def read_midi(file_path):
    midi_file = os.popen("xxd " + file_path)
    track_num = file_path.split("/")[len(file_path.split("/"))-1].split(".")[0]
    midi = ""
    for i in midi_file.read().split("\n"):
        midi += i.split("  ")[len(i.split("  "))-1]
    print(midi)
def read_xml(file_path):#division=480
    note = []
    i = 0
    midi_file = open(file_path,"r")
    track_num = file_path.split("/")[len(file_path.split("/"))-1].split(".")[0]
    midi = midi_file.read().split("MIDI Out #" + track_num + "</part-name>\n      <score-instrument id=\"P1-I1\">\n        <instrument-name>MIDI Out #2</instrument-name>\n      </score-instrument>\n      <midi-instrument id=\"P1-I1\">\n        <midi-channel>1</midi-channel>\n        <midi-program>1</midi-program>\n        <volume>78</volume>\n        <pan>90</pan>\n      </midi-instrument>\n    </score-part>\n  </part-list>")[1].split("<!--=======================================================-->")
    for n in midi[2:]:
        i += 1
        for s in n.split("<note>"):
            temp = []
            if "<duration>" in s and "<octave>" in s and "<step>" in s:
                temp.append(int(s.split("<duration>")[1].split("</duration>")[0]))
                temp.append(s.split("<octave>")[1].split("</octave>")[0] + s.split("<step>")[1].split("</step>")[0])
                temp.append(i)
                note.append(temp)
    temp = note
    note = []
    for n in temp:
        note_sum = 1
        while temp.count(n) > 1:                
            temp.pop(temp.index(n))
            note_sum += 1
        n.append(note_sum)
        note.append(n)
    return note
#print(read_xml("./tracks/xml/2.musicxml"))