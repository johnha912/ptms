================================================================================
                       PASSIVE TIME MANAGEMENT SYSTEM FLOW
================================================================================

                                [ START ]
                                    |
                                    v
                            +----------------+
                            |    main.py     |
                            | (Entry Point)  |
                            +----------------+
                                    |
        +---------------------------+---------------------------+
        | 1. DATA COLLECTION                                    |
        v                                                       |
+--------------------------+                                    |
| io_handler.py            |                                    |
| - Prompt User for Task   |<-------(Loop until "done")         |
| - Parse Time/Duration    |                                    |
|   (uses utils.py)        |                                    |
+--------------------------+                                    |
        |                                                       |
        v                                                       |
   [ List of Tasks ]                                            |
        |                                                       |
        +---------------------------+---------------------------+
                                    |
        +---------------------------+---------------------------+
        | 2. DATA PREPARATION                                   |
        v                                                       |
+--------------------------+                                    |
| scheduler.py             |                                    |
| - assign_tasks_to_days() |                                    |
| - Calculate Recurring    |                                    |
|   (uses utils.py)        |                                    |
+--------------------------+                                    |
        |                                                       |
        v                                                       |
 [ 7 Lists (Mon...Sun) ]                                        |
        |                                                       |
        +---------------------------+---------------------------+
                                    |
        +---------------------------+---------------------------+
        | 3. SCHEDULING ENGINE (The Core Loop)                  |
        v                                                       |
    FOR EACH DAY (Mon->Sun):                                    |
        |                                                       |
        +-> Initialize Time Grid: [False, False, ... False]     |
        |                                                       |
        +-> SORT TASKS:                                         |
        |   1. Priority (S -> A -> B...)                        |
        |   2. Flexibility (Tightest window first)              |
        |                                                       |
        +-> FOR EACH TASK:                                      |
              |                                                 |
              v                                                 |
      +-----------------------------+                           |
      | scheduler.try_schedule_task |                           |
      +-----------------------------+                           |
              |                                                 |
              v                                                 |
         Is there space?                                        |
         /             \                                        |
      (YES)           (NO)                                      |
        |               |                                       |
        v               v                                       |
  [ Update Grid ]   [ Run Recommender ]                         |
  [ Save Entry  ]   [ Save Error Msg  ]                         |
        |               |                                       |
        +-------+-------+                                       |
                |                                               |
           (Next Task)                                          |
                |                                               |
           (Next Day)                                           |
                |                                               |
                v                                               |
      [ Final Weekly Schedule ]                                 |
                                                                |
        +---------------------------+---------------------------+
                                    |
        +---------------------------+---------------------------+
        | 4. OUTPUT & VISUALIZATION                             |
        v                                                       |
+--------------------------+                                    |
| io_handler.py            |                                    |
| - visualize_schedule()   |--> [ PRINT ASCII BAR CHART ]       |
| - export_to_csv()        |--> [ SAVE .CSV FILE ]              |
+--------------------------+                                    |
                                                                |
                                    v                           |
                                 [ END ]                        |
                                                                |
================================================================================