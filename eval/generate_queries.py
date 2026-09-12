"""
Test Set Generator for ChatRecall Evaluation
============================================
Generates 40 curated evaluation queries in `eval/queries.json`:
- Exactly 40 queries mapped to ground-truth message IDs in data/chat.json
- At least 10 HARD queries with strictly ZERO WORD OVERLAP with target messages
- Balanced distribution across:
  * Meaning-based / Zero-word-overlap
  * Person-based (sender-filtered)
  * Time-based (timestamp window filtered)
  * Decision-seeking (resolution extraction)
"""

import json
import os
import re

STOPWORDS = {
    "a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "up", "about", "into", "over", "after", "is", "was", "were",
    "be", "been", "being", "have", "has", "had", "do", "does", "did", "what",
    "when", "where", "who", "which", "why", "how", "all", "any", "both", "each",
    "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only",
    "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just",
    "don", "should", "now", "i", "me", "my", "we", "our", "you", "your", "he",
    "him", "his", "she", "her", "it", "its", "they", "them", "their", "this", "that"
}

def extract_content_words(text: str) -> set:
    words = re.findall(r"\b[a-zA-Z]{2,}\b", text.lower())
    return set(w for w in words if w not in STOPWORDS)


def build_evaluation_set():
    with open("data/chat.json", "r", encoding="utf-8") as f:
        chat_msgs = json.load(f)

    id_to_msg = {m["id"]: m for m in chat_msgs}

    # Verify key target IDs
    # 1. Decision: Manali trip resolution
    t1_dec = next(m for m in chat_msgs if m["is_decision"] and "Manali" in m["message"])
    # 2. Decision: Koramangala 3BHK lease resolution
    t2_dec = next(m for m in chat_msgs if m["is_decision"] and "3BHK" in m["message"])
    # 3. Decision: Kindle farewell gift resolution
    t3_dec = next(m for m in chat_msgs if m["is_decision"] and "Kindle" in m["message"])

    # Find specific topic messages
    gym_rule = next(m for m in chat_msgs if "whoever misses workout" in m["message"])
    carpool_ecity = next(m for m in chat_msgs if "Electronic City" in m["message"])
    tax_elss = next(m for m in chat_msgs if "ELSS mutual fund" in m["message"])
    diwali_party = next(m for m in chat_msgs if "Diwali potluck party" in m["message"])
    ctr_coffee = next(m for m in chat_msgs if "CTR" in m["message"])
    smart_geyser = next(m for m in chat_msgs if "smart home plug" in m["message"])
    fairy_lights = next(m for m in chat_msgs if "fairy lights" in m["message"])

    # 40 Curated Queries
    query_specs = [
        # =========================================================================
        # 10 HARD QUERIES: STRICT ZERO-WORD OVERLAP BY DESIGN (is_hard: true)
        # =========================================================================
        {
            "id": "Q01",
            "query": "When did we decide on the mountain holiday?",
            "target_id": t1_dec["id"],
            "query_type": "semantic",
            "is_hard": True,
            "category": "Zero-Word Overlap (Decision)",
            "explanation": "Query asks about 'mountain holiday', target states 'Manali trip finalized... booked riverside cottage' (0 word overlap)."
        },
        {
            "id": "Q02",
            "query": "Surprise reading gadget ordered for our friend moving abroad",
            "target_id": t3_dec["id"],
            "query_type": "semantic",
            "is_hard": True,
            "category": "Zero-Word Overlap (Decision)",
            "explanation": "Query describes 'reading gadget for friend moving abroad', target mentions 'Kindle Paperwhite 32GB on Amazon... Toit Indiranagar' (0 word overlap)."
        },
        {
            "id": "Q03",
            "query": "What was the agreed upfront tenancy caution fund?",
            "target_id": t2_dec["id"],
            "query_type": "semantic",
            "is_hard": True,
            "category": "Zero-Word Overlap (Decision)",
            "explanation": "Query asks about 'agreed upfront tenancy caution fund', target mentions 'Agreement signed! 3BHK in Koramangala 4th block locked at 48k monthly rent with 2 lakh security deposit' (0 word overlap)."
        },
        {
            "id": "Q04",
            "query": "What is the penalty for skipping exercise streak?",
            "target_id": gym_rule["id"],
            "query_type": "semantic",
            "is_hard": True,
            "category": "Zero-Word Overlap (Rules)",
            "explanation": "Query asks about 'penalty for skipping exercise', target states 'whoever misses workout 3 days in a row pays for weekend breakfast' (0 word overlap)."
        },
        {
            "id": "Q05",
            "query": "Who is carpooling to the IT hub by automobile?",
            "target_id": carpool_ecity["id"],
            "query_type": "semantic",
            "is_hard": True,
            "category": "Zero-Word Overlap (Commute)",
            "explanation": "Query asks about 'carpooling to IT hub by automobile', target asks 'Anyone commuting towards Electronic City phase 1 today? Driving via elevated toll road.' (0 word overlap)."
        },
        {
            "id": "Q06",
            "query": "How to reduce income levy before fiscal close?",
            "target_id": tax_elss["id"],
            "query_type": "semantic",
            "is_hard": True,
            "category": "Zero-Word Overlap (Finance)",
            "explanation": "Query asks about 'reduce income levy before fiscal close', target says 'ELSS mutual fund me last minute invest karna padega tax bachane ke liye' (0 word overlap)."
        },
        {
            "id": "Q07",
            "query": "Traditional attire festive dinner gathering",
            "target_id": diwali_party["id"],
            "query_type": "semantic",
            "is_hard": True,
            "category": "Zero-Word Overlap (Events)",
            "explanation": "Query says 'Traditional attire festive dinner gathering', target says 'Diwali potluck party Saturday 7 PM at my place, dress code ethnic!' (0 word overlap)."
        },
        {
            "id": "Q08",
            "query": "Morning beverage preference after park jog",
            "target_id": ctr_coffee["id"],
            "query_type": "semantic",
            "is_hard": True,
            "category": "Zero-Word Overlap (Food & Routine)",
            "explanation": "Query says 'Morning beverage preference after park jog', target says 'I will come for post-run dosa and filter coffee at CTR' (0 word overlap)."
        },
        {
            "id": "Q09",
            "query": "Programmed residential water boiler countdown switch",
            "target_id": smart_geyser["id"],
            "query_type": "semantic",
            "is_hard": True,
            "category": "Zero-Word Overlap (Smart Home)",
            "explanation": "Query describes 'Programmed residential water boiler countdown switch', target states 'Updated the smart home plug schedule to turn off geyser automatically after 20 mins.' (0 word overlap)."
        },
        {
            "id": "Q10",
            "query": "Illuminations and audio equipment for celebration",
            "target_id": fairy_lights["id"],
            "query_type": "semantic",
            "is_hard": True,
            "category": "Zero-Word Overlap (Decor)",
            "explanation": "Query describes 'Illuminations and audio equipment', target says 'bhai main fairy lights and bluetooth speaker leke aaunga.' (0 word overlap)."
        },

        # =========================================================================
        # 10 PERSON-BASED QUERIES (Sender-filtered search)
        # =========================================================================
        {
            "id": "Q11",
            "query": "What did Priya say about the budget?",
            "target_id": next(m["id"] for m in chat_msgs if m["sender"] == "Priya Sharma" and "grocery expenditure" in m["message"]),
            "query_type": "person",
            "is_hard": False,
            "category": "Person Filter (Priya)",
            "explanation": "Searches for Priya's financial/budget tracking messages."
        },
        {
            "id": "Q12",
            "query": "Priya's advice on buying flight tickets",
            "target_id": next(m["id"] for m in chat_msgs if m["sender"] == "Priya Sharma" and "Tuesday afternoon" in m["message"]),
            "query_type": "person",
            "is_hard": False,
            "category": "Person Filter (Priya)",
            "explanation": "Priya's advice on booking flights on Tuesday afternoons."
        },
        {
            "id": "Q13",
            "query": "Did Vikram report an internet broadband outage ticket?",
            "target_id": next(m["id"] for m in chat_msgs if m["sender"] == "Vikram Malhotra" and "Airtel broadband" in m["message"]),
            "query_type": "person",
            "is_hard": False,
            "category": "Person Filter (Vikram)",
            "explanation": "Vikram raising an Airtel complaint ticket for fiber internet line."
        },
        {
            "id": "Q14",
            "query": "What did Vikram say about mechanical keyboard?",
            "target_id": next(m["id"] for m in chat_msgs if m["sender"] == "Vikram Malhotra" and "mechanical keyboard" in m["message"]),
            "query_type": "person",
            "is_hard": False,
            "category": "Person Filter (Vikram)",
            "explanation": "Vikram discussing tactile brown switches."
        },
        {
            "id": "Q15",
            "query": "Rohan's message about airport cab booking",
            "target_id": next(m["id"] for m in chat_msgs if m["sender"] == "Rohan Mehta" and "Airport taxi pre-booked" in m["message"]),
            "query_type": "person",
            "is_hard": False,
            "category": "Person Filter (Rohan)",
            "explanation": "Rohan confirming airport cab on MakeMyTrip."
        },
        {
            "id": "Q16",
            "query": "What did Rohan share for weekend trekking in Coorg?",
            "target_id": next(m["id"] for m in chat_msgs if m["sender"] == "Rohan Mehta" and "Coorg" in m["message"]),
            "query_type": "person",
            "is_hard": False,
            "category": "Person Filter (Rohan)",
            "explanation": "Rohan sharing Google sheet for Coorg trekking."
        },
        {
            "id": "Q17",
            "query": "Ananya's vintage denim jacket thrift store find",
            "target_id": next(m["id"] for m in chat_msgs if m["sender"] == "Ananya Iyer" and "vintage thrift store" in m["message"]),
            "query_type": "person",
            "is_hard": False,
            "category": "Person Filter (Ananya)",
            "explanation": "Ananya finding oversized denim jacket in Koramangala 5th block."
        },
        {
            "id": "Q18",
            "query": "What pottery workshop did Ananya mention?",
            "target_id": next(m["id"] for m in chat_msgs if m["sender"] == "Ananya Iyer" and "Pottery workshop" in m["message"]),
            "query_type": "person",
            "is_hard": False,
            "category": "Person Filter (Ananya)",
            "explanation": "Ananya mentioning Sunday ceramic center pottery workshop."
        },
        {
            "id": "Q19",
            "query": "Tanvi cab driver assignment details",
            "target_id": next(m["id"] for m in chat_msgs if m["sender"] == "Tanvi Desai" and "Swift Dzire" in m["message"]),
            "query_type": "person",
            "is_hard": False,
            "category": "Person Filter (Tanvi)",
            "explanation": "Tanvi sharing assigned cab plate number."
        },
        {
            "id": "Q20",
            "query": "Did Tanvi get confirmation from Airbnb host for early check-in?",
            "target_id": next(m["id"] for m in chat_msgs if m["sender"] == "Tanvi Desai" and "Airbnb host" in m["message"]),
            "query_type": "person",
            "is_hard": False,
            "category": "Person Filter (Tanvi)",
            "explanation": "Tanvi confirming 11 AM early check-in without extra charge."
        },

        # =========================================================================
        # 10 TIME-BASED QUERIES (Timestamp Window Filtered)
        # =========================================================================
        {
            "id": "Q21",
            "query": "What did we discuss in December regarding advance tax?",
            "target_id": next(m["id"] for m in chat_msgs if "advance tax" in m["message"] and "2023-12" in m["timestamp"]),
            "query_type": "time",
            "is_hard": False,
            "category": "Time Filter (December 2023)",
            "explanation": "December reminder on advance tax payment deadline."
        },
        {
            "id": "Q22",
            "query": "What did we discuss around Diwali?",
            "target_id": next(m["id"] for m in chat_msgs if "Diwali" in m["message"] and "potluck" in m["message"]),
            "query_type": "time",
            "is_hard": False,
            "category": "Time Filter (Diwali Nov 2023)",
            "explanation": "November discussions planning Diwali potluck party."
        },
        {
            "id": "Q23",
            "query": "What happened in January regarding gym and fitness resolutions?",
            "target_id": next(m["id"] for m in chat_msgs if "75 days fitness streak" in m["message"]),
            "query_type": "time",
            "is_hard": False,
            "category": "Time Filter (January 2024)",
            "explanation": "January New Year resolution streak challenge."
        },
        {
            "id": "Q24",
            "query": "What did we discuss in January about flat lease and rent negotiation?",
            "target_id": t2_dec["id"],
            "query_type": "time",
            "is_hard": False,
            "category": "Time Filter (January 2024)",
            "explanation": "January flat lease agreement and deposit split resolution."
        },
        {
            "id": "Q25",
            "query": "What did we discuss last month regarding carpool to office?",
            "target_id": carpool_ecity["id"],
            "query_type": "time",
            "is_hard": False,
            "category": "Time Filter (Last Month / Feb 2024)",
            "explanation": "February carpool coordination to Electronic City via elevated tollway."
        },
        {
            "id": "Q26",
            "query": "Discussions in March about Section 80C investment proofs",
            "target_id": next(m["id"] for m in chat_msgs if "80C investment proofs" in m["message"]),
            "query_type": "time",
            "is_hard": False,
            "category": "Time Filter (March 2024)",
            "explanation": "March financial year end 80C investment proofs reminder."
        },
        {
            "id": "Q27",
            "query": "Farewell planning in March for Siddharth",
            "target_id": next(m["id"] for m in chat_msgs if "Siddharth is moving to London" in m["message"]),
            "query_type": "time",
            "is_hard": False,
            "category": "Time Filter (March 2024)",
            "explanation": "March surprise farewell planning for Siddharth's move to London."
        },
        {
            "id": "Q28",
            "query": "Discussions in November about New Year vacation destinations",
            "target_id": next(m["id"] for m in chat_msgs if "where are we going for New Year trip" in m["message"]),
            "query_type": "time",
            "is_hard": False,
            "category": "Time Filter (November 2023)",
            "explanation": "November initial debate on year-end vacation destinations."
        },
        {
            "id": "Q29",
            "query": "What did we discuss in October about Bangalore Metro Purple line?",
            "target_id": next(m["id"] for m in chat_msgs if "Purple Line" in m["message"] and "2023-10" in m["timestamp"]),
            "query_type": "time",
            "is_hard": False,
            "category": "Time Filter (October 2023)",
            "explanation": "October news forward on Purple Line metro stretch opening."
        },
        {
            "id": "Q30",
            "query": "New Year trip dates discussion in November",
            "target_id": next(m["id"] for m in chat_msgs if "Dec 28 se Jan 2" in m["message"] and "Manali dates" in m["message"]),
            "query_type": "time",
            "is_hard": False,
            "category": "Time Filter (November 2023)",
            "explanation": "November proposal of Dec 28 - Jan 2 trip dates."
        },

        # =========================================================================
        # 10 GENERAL SEMANTIC & DECISION QUERIES (Baseline & Warmup)
        # =========================================================================
        {
            "id": "Q31",
            "query": "What was the final decision for the winter trip?",
            "target_id": t1_dec["id"],
            "query_type": "semantic",
            "is_hard": False,
            "category": "Decision Retrieval",
            "explanation": "Final destination, dates, and cottage booking decision."
        },
        {
            "id": "Q32",
            "query": "What was the finalized rent and security deposit for the 3BHK flat?",
            "target_id": t2_dec["id"],
            "query_type": "semantic",
            "is_hard": False,
            "category": "Decision Retrieval",
            "explanation": "Koramangala 3BHK 48k rent and 2L deposit resolution."
        },
        {
            "id": "Q33",
            "query": "What gift and dinner venue were finalized for Siddharth's farewell?",
            "target_id": t3_dec["id"],
            "query_type": "semantic",
            "is_hard": False,
            "category": "Decision Retrieval",
            "explanation": "Kindle Paperwhite purchase and Toit reservation decision."
        },
        {
            "id": "Q34",
            "query": "Who is going to the hospital emergency night shift duty?",
            "target_id": next(m["id"] for m in chat_msgs if "Night shift emergency casualty duty" in m["message"]),
            "query_type": "semantic",
            "is_hard": False,
            "category": "General Semantic",
            "explanation": "Doctor Neha mentioning emergency casualty duty."
        },
        {
            "id": "Q35",
            "query": "Who bought tickets for Friday night first day first show movie at PVR?",
            "target_id": next(m["id"] for m in chat_msgs if "PVR Forum" in m["message"]),
            "query_type": "semantic",
            "is_hard": False,
            "category": "General Semantic",
            "explanation": "Siddharth booking 4 movie tickets at PVR Forum."
        },
        {
            "id": "Q36",
            "query": "Who received a traffic police fine for unstrapped helmet?",
            "target_id": next(m["id"] for m in chat_msgs if "helmet strap" in m["message"]),
            "query_type": "semantic",
            "is_hard": False,
            "category": "General Semantic",
            "explanation": "Kabir getting 500 challan for unstrapped helmet."
        },
        {
            "id": "Q37",
            "query": "Who was stuck in heavy Silk Board traffic jam?",
            "target_id": next(m["id"] for m in chat_msgs if "Silk board" in m["message"]),
            "query_type": "semantic",
            "is_hard": False,
            "category": "General Semantic",
            "explanation": "Vikram stuck at Silk Board junction for 45 mins."
        },
        {
            "id": "Q38",
            "query": "Who makes authentic South Indian filter coffee with chicory blend?",
            "target_id": next(m["id"] for m in chat_msgs if "80:20 chicory blend" in m["message"]),
            "query_type": "semantic",
            "is_hard": False,
            "category": "General Semantic",
            "explanation": "Ananya preparing authentic chicory filter coffee."
        },
        {
            "id": "Q39",
            "query": "What board games were brought for the party?",
            "target_id": next(m["id"] for m in chat_msgs if "Secret Hitler" in m["message"]),
            "query_type": "semantic",
            "is_hard": False,
            "category": "General Semantic",
            "explanation": "Vikram bringing Catan and Secret Hitler board games."
        },
        {
            "id": "Q40",
            "query": "Who celebrated Swiggy Instamart delivery in 7 minutes?",
            "target_id": next(m["id"] for m in chat_msgs if "Instamart" in m["message"]),
            "query_type": "semantic",
            "is_hard": False,
            "category": "General Semantic",
            "explanation": "Kabir mentioning 7-minute ice cream delivery."
        }
    ]

    assert len(query_specs) == 40, f"Expected 40 queries, got {len(query_specs)}"
    hard_count = sum(1 for q in query_specs if q["is_hard"])
    assert hard_count >= 8, f"Expected >= 8 hard queries, got {hard_count}"

    # Verify all target messages exist and check zero-word overlap for hard queries
    verified_queries = []
    for spec in query_specs:
        tid = spec["target_id"]
        assert tid in id_to_msg, f"Target ID {tid} not found in chat dataset!"
        target_msg = id_to_msg[tid]

        q_words = extract_content_words(spec["query"])
        t_words = extract_content_words(target_msg["message"])
        overlap = q_words.intersection(t_words)

        if spec["is_hard"]:
            print(f"Hard Query {spec['id']}: overlap words={overlap}")
            assert len(overlap) == 0, f"Hard query {spec['id']} has word overlap: {overlap} with target: {target_msg['message']}"

        spec_obj = {
            "id": spec["id"],
            "query": spec["query"],
            "target_message_id": tid,
            "target_sender": target_msg["sender"],
            "target_timestamp": target_msg["timestamp"],
            "target_message": target_msg["message"],
            "query_type": spec["query_type"],
            "is_hard": spec["is_hard"],
            "category": spec["category"],
            "explanation": spec["explanation"],
            "word_overlap_count": len(overlap)
        }
        verified_queries.append(spec_obj)

    os.makedirs("eval", exist_ok=True)
    out_file = "eval/queries.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(verified_queries, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Generated {len(verified_queries)} verified evaluation queries.")
    print(f"✓ Hard (Zero-Word-Overlap) Queries: {hard_count}")
    print(f"✓ Saved to {out_file}")


if __name__ == "__main__":
    build_evaluation_set()
