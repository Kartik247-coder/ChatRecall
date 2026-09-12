"""
Sample synthetic group chat generator (scaled-down demo version).
Produces:
  - sample_chat.txt   (WhatsApp-export-style .txt file)
  - questions.json    (test queries with ground-truth message IDs)

This is a SMALL DEMO SET (not the full 4,000+ message corpus) meant to
show the format and eval methodology. Scale up participants/timeframe/
message count for the full submission.
"""

import json

# Each message: (id, date, time, sender, text)
messages = [
    (1,  "01/03/26", "09:12", "Aarav",   "guys where are we going for the trip this year"),
    (2,  "01/03/26", "09:13", "Meera",   "ooh trip planning already? excited"),
    (3,  "01/03/26", "09:15", "Rohan",   "kahi bhi chalega bas thoda relaxing ho"),
    (4,  "01/03/26", "09:16", "Priya",   "beach ya mountains?"),
    (5,  "01/03/26", "09:20", "Aarav",   "mountains > beach always"),
    (6,  "01/03/26", "09:21", "Sana",    "lol ok"),
    (7,  "01/03/26", "09:45", "Kabir",   "<Media omitted>"),
    (8,  "01/03/26", "09:46", "Kabir",   "found this resort, looks decent"),
    (9,  "01/03/26", "09:50", "Meera",   "how much though"),
    (10, "01/03/26", "09:52", "Kabir",   "around 4k per night for the room"),
    (11, "01/03/26", "10:05", "Priya",   "thoda mehenga hai na for a group trip"),
    (12, "01/03/26", "10:06", "Rohan",   "split ho jayega if we're 8 people"),
    (13, "01/03/26", "10:10", "Sana",    "ok"),
    (14, "01/03/26", "10:11", "Aarav",   "fine"),
    (15, "01/03/26", "10:12", "Meera",   "k"),
    (16, "01/03/26", "18:30", "Priya",   "anyone free this weekend to finalize"),
    (17, "01/03/26", "18:31", "Rohan",   "yes"),
    (18, "01/03/26", "18:31", "Sana",    "yes"),
    (19, "01/03/26", "18:45", "Kabir",   "cool i'll block the dates then"),

    (20, "04/03/26", "20:10", "Rohan",   "so did we decide anything on the weekend call"),
    (21, "04/03/26", "20:12", "Aarav",   "haan chalo Manali fix hai, first week of June"),
    (22, "04/03/26", "20:12", "Meera",   "yayyy"),
    (23, "04/03/26", "20:13", "Priya",   "finally"),
    (24, "04/03/26", "20:15", "Kabir",   "i'll message the resort guy tomorrow to lock rooms"),
    (25, "04/03/26", "20:16", "Sana",    "great, someone make a group for packing list"),
    (26, "04/03/26", "20:20", "Priya",   "on it"),

    (27, "05/03/26", "08:00", "Priya",   "made the packing group, added everyone"),
    (28, "05/03/26", "08:05", "Aarav",   "thanks"),
    (29, "05/03/26", "08:06", "Rohan",   "np"),
    (30, "05/03/26", "11:30", "Sana",    "does anyone know if it rains there in june"),
    (31, "05/03/26", "11:35", "Kabir",   "not really, thats why we picked early june"),
    (32, "05/03/26", "11:36", "Meera",   "smart"),

    (33, "10/03/26", "14:00", "Rohan",   "ok budget talk. how much are we each putting in"),
    (34, "10/03/26", "14:02", "Aarav",   "for travel + stay i think 8k per head is fair"),
    (35, "10/03/26", "14:03", "Priya",   "food alag rakhte hai usse"),
    (36, "10/03/26", "14:05", "Meera",   "agreed, food on the spot is easier"),
    (37, "10/03/26", "14:06", "Sana",    "so final number is 8k for travel and stay, food separate on the trip itself"),
    (38, "10/03/26", "14:07", "Kabir",   "yep locking that"),
    (39, "10/03/26", "14:08", "Rohan",   "sending payment link tomorrow then"),
    (40, "10/03/26", "14:08", "Aarav",   "ok"),

    (41, "11/03/26", "09:00", "Rohan",   "https://pay.example.com/trip-june -- send 8k here by 20th"),
    (42, "11/03/26", "09:10", "Meera",   "paid"),
    (43, "11/03/26", "09:20", "Sana",    "paid"),
    (44, "11/03/26", "09:45", "Priya",   "will pay tonight, salary day"),
    (45, "11/03/26", "10:00", "Kabir",   "paid"),
    (46, "11/03/26", "12:00", "Aarav",   "paid"),

    (47, "15/03/26", "19:00", "Meera",   "someone tell me what shoes to pack, first time trekking"),
    (48, "15/03/26", "19:05", "Rohan",   "proper trekking shoes yaar, not sneakers"),
    (49, "15/03/26", "19:06", "Meera",   "ok noted"),
    (50, "15/03/26", "19:10", "Priya",   "<Media omitted>"),
    (51, "15/03/26", "19:11", "Priya",   "found a good packing checklist, sharing here"),

    (52, "20/03/26", "10:00", "Sana",    "reminder deadline for payment is today"),
    (53, "20/03/26", "10:05", "Priya",   "paid, sorry for the delay"),
    (54, "20/03/26", "10:06", "Rohan",   "all good, everyone's in now"),

    # thread 2: workation instead of vacation debated, resolved to keep original plan
    (55, "25/03/26", "16:00", "Aarav",   "random thought, what if we make it a workation instead, i have deadlines that week"),
    (56, "25/03/26", "16:02", "Kabir",   "bro no, this is a proper break"),
    (57, "25/03/26", "16:03", "Sana",    "same, i need to actually disconnect"),
    (58, "25/03/26", "16:05", "Rohan",   "let's just keep it a normal vacation, no laptops rule"),
    (59, "25/03/26", "16:06", "Aarav",   "fine fine, no laptops, i'll manage my deadline before"),
    (60, "25/03/26", "16:07", "Meera",   "good, decided then, pure vacation no work"),
    (61, "25/03/26", "16:08", "Priya",   "phew ok"),

    (62, "02/04/26", "08:30", "Kabir",   "resort confirmed rooms, 3 rooms for 8 people, sharing arrangement inside"),
    (63, "02/04/26", "08:35", "Rohan",   "who's rooming with who"),
    (64, "02/04/26", "08:40", "Priya",   "girls one room, we'll sort the guys rooms"),
    (65, "02/04/26", "08:41", "Sana",    "works"),
    (66, "02/04/26", "08:45", "Aarav",   "me and Rohan in one, Kabir with the other two guys"),
    (67, "02/04/26", "08:46", "Rohan",   "sure"),

    (68, "10/04/26", "12:00", "Meera",   "can we do a bonfire night there"),
    (69, "10/04/26", "12:02", "Kabir",   "resort allows it, need to book in advance"),
    (70, "10/04/26", "12:03", "Meera",   "book it please"),
    (71, "10/04/26", "12:10", "Kabir",   "booked"),

    (72, "18/04/26", "21:00", "Sana",    "flight or train for this one"),
    (73, "18/04/26", "21:02", "Priya",   "train is cheaper honestly"),
    (74, "18/04/26", "21:03", "Aarav",   "but flight saves like 6 hours"),
    (75, "18/04/26", "21:05", "Rohan",   "let's fly, time saved is worth it for a short trip"),
    (76, "18/04/26", "21:06", "Meera",   "agreed, flight it is, i'll check tickets"),
    (77, "18/04/26", "21:20", "Meera",   "found decent morning flights, booking for everyone tonight"),
    (78, "18/04/26", "23:00", "Meera",   "done, tickets booked for all 8, boarding pass pdfs incoming"),
    (79, "18/04/26", "23:01", "Meera",   "<Media omitted>"),

    (80, "01/05/26", "17:00", "Rohan",   "one month to go!!"),
    (81, "01/05/26", "17:01", "Kabir",   "🔥"),
    (82, "01/05/26", "17:02", "Sana",    "cant wait"),
    (83, "01/05/26", "17:03", "Priya",   "same"),

    (84, "10/05/26", "09:00", "Aarav",   "forgot to ask, are pets allowed at the resort, my cousin might tag along with her dog"),
    (85, "10/05/26", "09:05", "Kabir",   "checking with them, will confirm"),
    (86, "10/05/26", "09:40", "Kabir",   "no pets allowed unfortunately"),
    (87, "10/05/26", "09:41", "Aarav",   "ah ok i'll tell her"),

    (88, "20/05/26", "20:00", "Priya",   "anyone have a spare power bank i can borrow for the trip"),
    (89, "20/05/26", "20:05", "Sana",    "i have one, i'll bring it"),
    (90, "20/05/26", "20:06", "Priya",   "thankss"),

    (91, "25/05/26", "13:00", "Meera",   "this message was deleted"),
    (92, "25/05/26", "13:01", "Rohan",   "lol what happened"),
    (93, "25/05/26", "13:02", "Meera",   "wrong group oops"),

    (94, "28/05/26", "11:00", "Kabir",   "final headcount check, still 8 people right"),
    (95, "28/05/26", "11:02", "Aarav",   "yes"),
    (96, "28/05/26", "11:02", "Priya",   "yes"),
    (97, "28/05/26", "11:03", "Sana",    "yes"),
    (98, "28/05/26", "11:03", "Rohan",   "yes"),
    (99, "28/05/26", "11:04", "Meera",   "yes obviously lol"),

    (100, "01/06/26", "06:00", "Aarav",  "at the airport, where's everyone"),
    (101, "01/06/26", "06:02", "Rohan",  "5 mins away"),
    (102, "01/06/26", "06:05", "Sana",   "here"),
    (103, "01/06/26", "06:10", "Meera",  "landed at the gate area, come here"),
    (104, "01/06/26", "06:15", "Priya",  "on my way"),
    (105, "01/06/26", "06:20", "Kabir",  "here too, let's check in together"),

    # thread 3: fee/expense sheet decision (mirrors table-style requirement conceptually)
    (106, "03/06/26", "19:00", "Sana",   "someone should track expenses on the trip, splitwise?"),
    (107, "03/06/26", "19:02", "Meera",  "yes let's use splitwise, i'll create the group"),
    (108, "03/06/26", "19:05", "Meera",  "created, added everyone, add expenses as we go"),
    (109, "03/06/26", "19:06", "Kabir",  "noted"),
    (110, "03/06/26", "19:07", "Priya",  "ok"),

    (111, "05/06/26", "10:00", "Rohan",  "back home, that trip was amazing"),
    (112, "05/06/26", "10:01", "Aarav",  "best one yet honestly"),
    (113, "05/06/26", "10:02", "Meera",  "settling splitwise tonight, will send final numbers"),
    (114, "05/06/26", "10:05", "Sana",   "sounds good"),
    (115, "05/06/26", "10:06", "Priya",  "already missing the mountains"),
]

# --- Write WhatsApp-export style .txt file ---
lines = []
for _id, date, time, sender, text in messages:
    lines.append(f"{date}, {time} - {sender}: {text}")

with open("sample_chat.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

# --- Build ID -> message lookup for question construction ---
by_id = {m[0]: m for m in messages}

STOPWORDS = {
    "a", "an", "the", "is", "was", "are", "were", "do", "did", "does",
    "to", "in", "on", "of", "that", "this", "these", "those", "we",
    "i", "they", "it", "for", "and", "or", "but", "with", "at", "by",
    "be", "has", "have", "had", "will", "would", "can", "could",
}

def words(text):
    import re
    tokens = set(re.findall(r"[a-zA-Z']+", text.lower()))
    return tokens - STOPWORDS

questions = [
    # --- Warm-up (some word overlap expected) ---
    {"id": "q1",  "query": "where did we decide to go for the trip",              "answer_id": 21,  "type": "semantic"},
    {"id": "q2",  "query": "how much is the resort per night",                    "answer_id": 10,  "type": "semantic"},
    {"id": "q3",  "query": "what did Kabir say about the resort rooms",           "answer_id": 62,  "type": "person"},
    {"id": "q4",  "query": "what did Meera say about flight tickets",             "answer_id": 78,  "type": "person"},
    {"id": "q5",  "query": "what did Sana say about the payment deadline",        "answer_id": 52,  "type": "person"},
    {"id": "q6",  "query": "what did we discuss in early March",                  "answer_id": 21,  "type": "time"},
    {"id": "q7",  "query": "what happened in the chat during the third week of May", "answer_id": 88, "type": "time"},
    {"id": "q8",  "query": "who is bringing a power bank",                        "answer_id": 89,  "type": "semantic"},
    {"id": "q9",  "query": "are pets allowed at the resort",                      "answer_id": 86,  "type": "semantic"},
    {"id": "q10", "query": "who is rooming with Aarav",                          "answer_id": 66,  "type": "semantic"},
    {"id": "q11", "query": "did we book a bonfire night",                        "answer_id": 71,  "type": "semantic"},
    {"id": "q12", "query": "what is the budget per person for travel and stay",   "answer_id": 37,  "type": "semantic"},
    {"id": "q13", "query": "what app are we using to track trip expenses",        "answer_id": 107, "type": "semantic"},
    {"id": "q14", "query": "did everyone pay on time",                           "answer_id": 53,  "type": "semantic"},
    {"id": "q15", "query": "what did Priya say about packing",                   "answer_id": 51,  "type": "person"},

    # --- Hard: zero word-overlap between query and the answer message text ---
    {"id": "q16", "query": "was the destination ever finalized",
     "answer_id": 21, "type": "semantic_hard",
     "note": "answer text: 'haan chalo Manali fix hai, first week of June' shares no words with the query"},
    {"id": "q17", "query": "did anyone suggest turning this into a work trip",
     "answer_id": 55, "type": "semantic_hard",
     "note": "answer text: 'random thought, what if we make it a workation instead, i have deadlines that week' shares no words with the query"},
    {"id": "q18", "query": "how are they splitting up the sleeping arrangements",
     "answer_id": 64, "type": "semantic_hard",
     "note": "answer text: 'girls one room, we'll sort the guys rooms' shares no words with the query"},
    {"id": "q19", "query": "why did they choose air travel over the train",
     "answer_id": 75, "type": "semantic_hard",
     "note": "answer text: 'let's fly, time saved is worth it for a short trip' shares no words with the query"},
    {"id": "q20", "query": "is there a rule against bringing animals to the property",
     "answer_id": 86, "type": "semantic_hard",
     "note": "answer text: 'no pets allowed unfortunately' shares no words with the query"},
]

with open("questions.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2)

if __name__ == "__main__":
    print("Zero-overlap check for hard questions:")
    for q in questions:
        if q["type"] == "semantic_hard":
            qw = words(q["query"])
            aw = words(by_id[q["answer_id"]][4])
            overlap = qw & aw
            print(f"  {q['id']}: overlap={overlap if overlap else 'NONE'}")

    print(f"\nGenerated {len(messages)} messages -> sample_chat.txt")
    print(f"Generated {len(questions)} questions -> questions.json")
