WESTLINE CARRIERS – TPMS ASSESSMENT
Humaniti AI Build Challenge · Data Analyst Assessment
Submitted by: Ritika Raj Parekh
Submitted on: 6 November 2026
GitHub: https://github.com/RitikaRaj-1005/westline-tpms-assessment

----------------------------------------------------------------------
THE BRIEF
----------------------------------------------------------------------
"Find out what is happening with this fleet's tyres."

Six five-axle, fourteen-tyre trucks, two depots (Belagavi, Hubballi),
TyreSense TPMS exports for 1 June – 15 July 2026, plus the tyre
register, tread inspections, daily km log, inflation spec sheet, data
dictionary and a transcript with the fleet manager, Ramesh Vijayan.

----------------------------------------------------------------------
SHORT ANSWERS
----------------------------------------------------------------------
1. Karwar 5RI failure (11 July): not foreseeable a day ahead – the tyre
   was at spec the night before. On the day it pulled away from its
   twin from about 03:15; a 10 PSI twin gap at 03:40 came more than
   five hours before it fell below 70 PSI. (F12)

2. One alarm on one tyre: a twin comparison (inner vs outer on the
   same hub) is a candidate warning – 10 PSI to inspect, 20 PSI
   urgent, with a reset band. Tested on one failure only; does not
   cover axles 1–3. (F13)

3. Hubballi "roads eating tyres": not mainly. Hubballi fills hot tyres
   in the afternoon to the cold card value, so its trucks start every
   morning 10–12 PSI under spec; Belagavi adjusts at much lower tyre temperatures and starts on
   spec. Roads add 1–2 PSI per 30 days at most. (F14–F16)

4. Goa "nothing but alarms": the afternoon drops are all 14 tyres
   cooling together at the rate physics predicts, and pressure
   recovers. They happen on all six trucks. Rain is plausible, not
   proven (no weather data); actual alarms need the alert log. (F17)

----------------------------------------------------------------------
FOLDER CONTENTS
----------------------------------------------------------------------
In the submitted zip the files are grouped into the folders below. In
the GitHub repository the same files sit at the top level.

01_Findings/
  Westline Tyre Findings.pdf           Short deck, most critical
                                       findings (10 slides, built in
                                       Claude Slides).
  Westline_Findings_Full.html          All 18 findings, each with what
                                       I checked, evidence, what it
                                       tells us, confidence, what would
                                       change my mind. Opens offline in
                                       any browser.

02_Five_Questions/
  Westline_Five_Questions.pdf          Five ranked questions for Ramesh,
                                       each with why it matters and what
                                       I would do with the answer. (Also
                                       on slide 9 of the deck.)

03_Distrust_Memo/
  Westline_Distrust_Memo.pdf           One page: what in the pack should
                                       not be trusted, and what I did
                                       about each item.

04_Code/
  Westline_Analysis.ipynb              Google Colab notebook, Sections
                                       1–8, with all outputs.
  westline_analysis.py                 Plain-script copy of the notebook.
  build_html.py                        Builds the HTML findings file
                                       (run by Section 8).
  notes.json                           The Assessment Notes as structured
                                       text; read by build_html.py.

05_AI_Transcripts/
  Every AI conversation, complete, numbered in the order I had them:
  one Claude session (analysis, code, notes, deliverables) and the
  ChatGPT sessions I used to review each section independently.

06_Working_Notes/
  Westline – Assessment Notes.pdf      My working document: methodology,
                                       data-quality checks, hypotheses
                                       (H1–H8) and their status, all
                                       findings, limitations, transcript
                                       claim checks and an AI working
                                       log.

----------------------------------------------------------------------
HOW TO RUN THE CODE
----------------------------------------------------------------------
1. Put the 19 challenge-pack files in one Google Drive folder
   (I used MyDrive/Westline_Working/), with build_html.py and
   notes.json beside them.
2. Open Westline_Analysis.ipynb in Google Colab, set DATA in Section 1
   to that folder, and run all cells in order.
3. Section 8 writes Westline_Findings_Full.html to the same folder.
Python libraries: pandas, numpy, matplotlib, openpyxl, python-docx
(all available in Colab).

Notebook sections:
  1  Setup and file check            5   Hubballi vs Belagavi pressures,
  2  Load and first health check         cold readings, fills, leak rates
  3  Cleaning and validation         6   Goa afternoon cooling events
     (duplicates, IDs, codes, GPS)   7   Batteries, km log, transcript
  4  Karwar 5RI failure and twin         claims
     warning rule                    8   Build the HTML findings file
  Lettered cells (3B, 4H, 5D, 6I, 7V ...) are validation checks added
  after review.

----------------------------------------------------------------------
HOW I WORKED
----------------------------------------------------------------------
- Data quality first, so nothing later was built on a bad table:
  2,869 cross-file duplicates removed, truck identity taken from file
  names (one export has a wrong registration), side codes verified
  against tyre serials (the data dictionary is wrong).
- Physics before statistics: pressure moves about 0.6–0.7 PSI per °C,
  so I compared pressure with spec only on cold readings (parked at
  least 3 hours) and compared each tyre with its twin, which shares
  load, road and temperature.
- Every source checked against another: transcript claims against the
  register, GPS and km log; register against inspection sheets; GPS
  distance against the odometer.
- AI use: Claude (one long session) wrote and tested the analysis code
  and kept the notes; I ran every section myself in Colab and only
  accepted results that matched. I had ChatGPT review each section
  independently; its challenges led to real corrections (for example
  a GPS denominator, an alarm-episode gap rule, a loss-rate split,
  event timing and an unsupported "engine off" claim). The AI working
  log in 06_Working_Notes lists what was accepted and rejected.

----------------------------------------------------------------------
LIMITS
----------------------------------------------------------------------
One failure, six weeks of data, no alert log, no weather, load,
speed or ignition data, partial tread inspections. Each finding states
its confidence and what would change it.

----------------------------------------------------------------------
DATA NOTE
----------------------------------------------------------------------
The challenge-pack data belongs to the client and is not included in
the public GitHub repository. It is not redistributed with the code.
