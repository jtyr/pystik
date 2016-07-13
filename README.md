pystik
======

This is a simple software MIDI synthesizer for the Jamstik+ guitar MIDI
controller.


Usage
-----

Just connect the Jamstik+ to the PC via USB cable and run the `pystick.py`. The
program will ask to select the correct MIDI device and then it's ready to play.

Example of the graphical output:

```
$ ./pystick.py
List of all MIDI devices:
 1: ALSA - Midi Through Port-0
 3: ALSA - JS106B13 MIDI 1
Please select your device: 3



Message:   None
Pressed:   0, 0, 0, 0, 0, 0
Strumming: 0, 0, 0, 0, 0, 0
Chord:     ?
x e|-----|-----|-----|-----|-----|---------------------|
x B|-----|-----|-----|-----|-----|---------------------|
x G|-----|-----|-----|-----|-----|---------------------|
x D|-----|-----|-----|-----|-----|---------------------|
x A|-----|-----|-----|-----|-----|---------------------|
x E|-----|-----|-----|-----|-----|---------------------|


...


Message:   [144, 66, 43, 0]
Pressed:   2, 3, 2, 0, 0, 0
Strumming: 1, 1, 1, 1, 0, 0
Chord:     D
o e|-----|--X--|-----|-----|-----|----------X----------|
o B|-----|-----|--X--|-----|-----|----------X----------|
o G|-----|--X--|-----|-----|-----|----------X----------|
o D|-----|-----|-----|-----|-----|----------X----------|
x A|-----|-----|-----|-----|-----|---------------------|
x E|-----|-----|-----|-----|-----|---------------------|
```


Limitations
-----------

Current implementation can visualize and play only notes from the first 5
frets. The produced sound is not necessarily great but it's good enough for
testing purposes.


Sound samples
-------------

The sound samples used by this program were extracted from
[professional recodings](http://theremin.music.uiowa.edu/MISguitar.html) done
by the [University of Iowa Electronic Music Studios](http://theremin.music.uiowa.edu/MIS.html).
Only the `ff` (fortissimo) recordings was used because the other dynamics are
too silent.

Each file contains several sounds. For example the file
`Guitar.ff.sulE.E2B2.aif` covers sounds from the `E` note to the `B` note in
the second octave. The first 6 sounds from this file correspond with the guitar
notes `E0`-`E5` on the `E` string. Details for other sounds can be deducted
from the table bellow.

```
+----------+------------------------------------+------------------------------------+------------------------------------+
| Octave   | 2  2  2  2  2  2  2  2  2  2  2  2 | 3  3  3  3  3  3  3  3  3  3  3  3 | 4  4  4  4  4  4  4  4  4  4  4  4 |
+----------+------------------------------------+------------------------------------+------------------------------------+
| Note     | C  C# D  D# E  F  F# G  G# A  A# B | C  C# D  D# E  F  F# G  G# A  A# B | C  C# D  D# E  F  F# G  G# A  A# B |
+----------+------------------------------------+------------------------------------+------------------------------------+
| String e |                                    |                                    |             e0 e1 e2 e3 e4 e5 ...  |
| String B |                                    |                                  B0| B1 B2 B3 B4 B5 ...                 |
| String G |                                    |                      G0 G1 G2 G3 G4| G5 ...                             |
| String D |                                    |       D0 D1 D2 D3 D4 D5 ...        |                                    |
| String A |                            A0 A1 A2| A3 A4 A5 ...                       |                                    |
| String E |             E0 E1 E2 E3 E4 E5 ...  |                                    |                                    |
+----------+------------------------------------+------------------------------------+------------------------------------+


                Fret 1 Fret 2 Fret 3 Fret 4 Fret 5

  String e   e0|--e1--|--e2--|--e3--|--e4--|--e5--|
  String B   B0|--B1--|--B2--|--B3--|--B4--|--B5--|
  String G   G0|--G1--|--G2--|--G3--|--G4--|--G5--|
  String D   D0|--D1--|--D2--|--D3--|--D4--|--D5--|
  String A   A0|--A1--|--A2--|--A3--|--A4--|--A5--|
  String E   E0|--E1--|--E2--|--E3--|--E4--|--E5--|
```


Dependencies
------------

- `pygame` Python library


License
-------

MIT


Author
------

Jiri Tyr
