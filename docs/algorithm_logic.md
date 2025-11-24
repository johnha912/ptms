Detailed Flow: DATA INPUT & CLEANING
====================================

[ USER STARTS APP ]
       |
       v
   Initialize empty list: tasks = []
       |
       v
+-->[ PROMPT: "Task Name or 'done'" ]
|      |
|      v
|   < Is input 'done'? >-------(YES)-------> [ RETURN tasks list ]
|      |                                            |
|    (NO)                                           |
|      |                                            v
|   [ PROMPT: "Duration" (str) ]           (To Scheduler Logic)
|      |
|      +--- Call utils.parse_duration() --> [ Returns Int (mins) ]
|      |
|   [ PROMPT: "Earliest Start" (str) ]
|      |
|      +--- Call utils.parse_time() ------> [ Returns Int (mins from 0) ]
|      |
|   [ PROMPT: "Frequency" ]
|      |
|      +--- Convert to Int ---------------> [ Handle ValueError = 1 ]
|      |
|   [ PROMPT: "Priority (S,A,B,C)" ]
|      |
|      +--- Normalize --------------------> [ Default to 'C' if invalid ]
|      |
|   [ CONSTRUCT DICTIONARY ]
|   { 'name': ..., 'duration': 90, ... }
|      |
|   [ APPEND to tasks list ]
|      |
+------+ (Loop back to start)

Detailed Flow: WEEKLY LOOP & SORTING
====================================

(From Input Phase)
       |
       v
[ assign_tasks_to_days() ]
Determine specific day (Mon-Sun) for every task
       |
       v
   [ 7 Buckets Created ]
   [Mon_Tasks], [Tue_Tasks] ... [Sun_Tasks]
       |
       v
   INIT Outer Loop: For Day_Index in 0..6:
       |
       +---> [ Create Boolean Grid ]
       |     occupied = [False, False, ... (96 times)]
       |
       |     < Are there tasks today? > --(NO)--> (Skip to Next Day)
       |           |
       |         (YES)
       |           |
       |     [ SORTING ALGORITHM ]
       |     1. Sort by Priority Value (0=S, 1=A...)
       |     2. Sort by Flexibility (Tightest window first)
       |           |
       |           v
       |     INIT Inner Loop: For Task in Sorted_Tasks:
       |           |
       |           +---> Call try_schedule_task()
       |           |           |
       |           |     < Success? >
       |           |     /          \
       |           |   (YES)        (NO)
       |           |     |            |
       |           |   [Save Data]  [Save Error & Suggestion]
       |           |     |            |
       |           +<----+            |
       |           |                  |
       |     (Next Task) <------------+
       |
       v
 (Next Day)
       |
       v
[ RETURN ALL DATA TO MAIN ]

Detailed Flow: COLLISION DETECTION & RECOMMENDER
================================================

[ Start try_schedule_task ]
       |
       v
[ CALC: Slots Needed ]
(Duration / 15) = N slots
       |
[ CALC: Search Range ]
Start_Index to End_Index based on user constraints
       |
       v
LOOP: Check every possible start slot (i) in Range
       |
       v
   < Is occupied[i] to occupied[i+N] all False? >
       |
     (NO) --------------------------------------+
       |                                        |
     (YES: We found a spot!)                    |
       |                                        |
   [ MARK occupied[i...i+N] = True ]      (Try Next i)
       |                                        |
   < Task > 2 Hours? >                          |
       |          |                             |
     (NO)       (YES)                           |
       |          |                             |
       |      < Is Next Slot Free? >            |
       |       /                  \             |
       |     (Yes)               (No)           |
       |       |                   |            |
       |   [Mark Break]        (Skip Break)     |
       |       |                   |            |
       v       v                   v            v
   [ RETURN SUCCESS ] <-------------------- [ LOOP ENDS ]
                                           (No spot found)
                                                |
                                                v
                                    [ RUN RECOMMENDER ]
                                    (Call find_alternatives)
                                                |
                                                v
                                    Loop through ENTIRE day (0..95)
                                    Count consecutive 'False' slots
                                                |
                                                v
                                    < Gap >= N slots? >
                                    /                 \
                                  (YES)              (NO)
                                    |                  |
                           [ Add to Suggestions ]   (Keep searching)
                                    |                  |
                                    v                  v
                             [ RETURN FAILURE + SUGGESTIONS ]
