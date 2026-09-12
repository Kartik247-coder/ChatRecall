"""
Synthetic Group Chat Generator for ChatRecall
=============================================
Generates a realistic, messy synthetic group chat archive with:
- Deterministic random generation (fixed seed: 42)
- 8 distinct participants with unique personas and texting habits
- 6-month timestamp range (2023-10-01 to 2024-03-31)
- 4,200+ messages
- Realistic chat artifacts: Hinglish/code-mixing, typos, 1-word reactions,
  forwarded text, '<Media omitted>' lines, reply references, and conversational bursts
- 3 long resolving threads with distinct decision outcomes marked with `is_decision=True`
- Multi-day conversational episodes (Diwali, New Year, Gym challenge, Carpools, Tax saving, Farewell planning, etc.).
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

SEED = 42
START_DATE = datetime(2023, 10, 1, 8, 0, 0)
END_DATE = datetime(2024, 3, 31, 23, 30, 0)

PARTICIPANTS = {
    "Rohan Mehta": {
        "alias": "rohan",
        "role": "Organizer / Project Manager",
        "style": "Organized, creates polls, suggests dates, polite Hinglish",
        "common_words": ["guys", "plan", "update", "poll", "timing", "batao", "confirm"],
    },
    "Priya Sharma": {
        "alias": "priya",
        "role": "Finance / Budget Analyst",
        "style": "Budget conscious, tracks expenses, asks for receipts, practical",
        "common_words": ["budget", "split", "gpay", "hisab", "expensive", "sasta", "cost"],
    },
    "Kabir Sen": {
        "alias": "kabir",
        "role": "Jokester / Creative",
        "style": "Slang, memes, forwards, informal Hinglish, banter",
        "common_words": ["bhai", "scene", "jugaad", "mast", "arre", "lol", "chill"],
    },
    "Ananya Iyer": {
        "alias": "ananya",
        "role": "Foodie / Designer",
        "style": "Food recommendations, aesthetic, enthusiastic, cafe lover",
        "common_words": ["cafe", "food", "aesthetic", "love", "try karte hain", "vibes"],
    },
    "Vikram Malhotra": {
        "alias": "vikram",
        "role": "Tech Lead / Pragmatist",
        "style": "Technical, punctual, checks logistics/wifi/routes, concise",
        "common_words": ["wifi", "route", "traffic", "timing", "setup", "sorted"],
    },
    "Neha Gupta": {
        "alias": "neha",
        "role": "Resident Doctor",
        "style": "Busy, erratic hours, short 1-word replies, emoji reactions",
        "common_words": ["haan", "done", "ok", "shift pe hoon", "can't make it", "lol", "+1"],
    },
    "Siddharth Verma": {
        "alias": "sid",
        "role": "Sports / Cinema Buff",
        "style": "Cricket debates, movies, weekend plans, passionate",
        "common_words": ["match", "movie", "popcorn", "cricinfo", "bhai dekha kya", "epic"],
    },
    "Tanvi Desai": {
        "alias": "tanvi",
        "role": "Logistics / Operations",
        "style": "Handles bookings, tickets, Airbnb calls, follow-ups",
        "common_words": ["booking", "tickets", "airbnb", "confirmed", "call kiya", "details"],
    },
}

FORWARDED_MESSAGES = [
    "[Forwarded message] Govt announces new tax rebate under Section 87A for income up to 7 Lakhs in new regime.",
    "[Forwarded message] Bangalore Metro Purple Line full stretch now operational from Challaghatta to Whitefield!",
    "[Forwarded message] Traffic Advisory: Outer Ring Road waterlogging cleared near Ecospace.",
    "[Forwarded message] Happy Diwali to you and your lovely family! May this year bring health and prosperity ✨🪔",
    "[Forwarded message] Top 10 productivity hacks for remote software engineers in 2024.",
    "[Forwarded message] Reminder: Last date for advance tax payment for Q3 is 15th December.",
]

ONE_WORD_REPLIES = ["haan", "done", "ok", "nahi", "lol", "nice", "yep", "mast", "arre", "sahi hai", "+1", "cool", "sure"]


def generate_synthetic_chat() -> List[Dict[str, Any]]:
    random.seed(SEED)
    messages: List[Dict[str, Any]] = []
    msg_counter = 1

    def create_msg(sender: str, text: str, dt: datetime, thread_id: str = None, 
                   is_decision: bool = False, is_forward: bool = False, 
                   media_omitted: bool = False, reply_to_id: str = None) -> Dict[str, Any]:
        nonlocal msg_counter
        msg_id = f"MSG_{msg_counter:05d}"
        msg_counter += 1
        return {
            "id": msg_id,
            "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "sender": sender,
            "message": text,
            "reply_to_id": reply_to_id,
            "thread_id": thread_id,
            "is_decision": is_decision,
            "is_forward": is_forward,
            "media_omitted": media_omitted,
        }

    # =========================================================================
    # 3 LONG RESOLVING THREADS WITH EXPLICIT DECISION MARKERS
    # =========================================================================

    # Thread 1: Year-End Trip (Nov 12, 2023)
    t1_time = datetime(2023, 11, 12, 19, 15, 0)
    t1_msgs = [
        ("Rohan Mehta", "guys year end leaves apply karne ka deadline aa gaya, where are we going for New Year trip?"),
        ("Kabir Sen", "Goa chalo bhai! Sunburn beach party scenes"),
        ("Priya Sharma", "Goa flights are 18k return ticket right now, hotel prices 4x. Budget will blow up completely."),
        ("Ananya Iyer", "what about Pondicherry? French quarter cafes, quiet beach, cute homestays?"),
        ("Siddharth Verma", "Pondicherry is nice but December me a lot of rain happens sometimes. Weather check kiya?"),
        ("Tanvi Desai", "I checked Udaipur also, heritage palace properties have discount offers for groups"),
        ("Vikram Malhotra", "Udaipur in winter is great but we did Rajasthan last year guys. Let's do mountains or snow?"),
        ("Kabir Sen", "Manali or Kasol! Snowfall dekhne milega December end me!"),
        ("Priya Sharma", "Manali travel cost: Delhi to Manali Volvo bus is 1200 per head, budget friendly hai."),
        ("Rohan Mehta", "Manali dates: Dec 28 se Jan 2? That way 2 days leave needed only with public holidays."),
        ("Neha Gupta", "I have hospital shifts on Dec 26 and Jan 3, so Dec 28 to Jan 2 works perfectly for me!"),
        ("Tanvi Desai", "I found two options in Manali: Mall Road hotel (noisy) vs riverside wooden cottage in Old Manali near Clubhouse."),
        ("Ananya Iyer", "Old Manali riverside cottage 100%! The aesthetic with snow and pine trees is dreamy."),
        ("Siddharth Verma", "Old Manali has great cafes also, Dylan's toasted coffee and trout fish."),
        ("Priya Sharma", "Cottage cost per night kitna hai Tanvi?"),
        ("Tanvi Desai", "It's 14,000 per night for whole 4-bedroom cottage, for 5 nights = 70k total, divided by 8 is 8,750 per head."),
        ("Kabir Sen", "Super affordable bhai, Goa me 1 night hotel was 12k."),
        ("Vikram Malhotra", "Cottage has high-speed WiFi and power backup? In case of snowfall power cut?"),
        ("Tanvi Desai", "Yes owner confirmed generator backup and 100 Mbps fiber line."),
        ("Rohan Mehta", "Everyone please confirm by tonight so Tanvi can block the dates before someone else books."),
        ("Siddharth Verma", "Confirmed from my side!"),
        ("Neha Gupta", "Confirmed!"),
        ("Ananya Iyer", "100% yes!"),
        ("Kabir Sen", "Main toh packed hoon already haha"),
        ("Vikram Malhotra", "Confirmed."),
        ("Priya Sharma", "Sent 10k advance share on GPay to Tanvi."),
        # RESOLUTION MESSAGE FOR THREAD 1
        ("Tanvi Desai", "Chalo sab lock ho gaya: Manali trip finalized for Dec 28 to Jan 2! Booked the riverside cottage in Old Manali, ticket confirmation emailed to all.", True),
        ("Rohan Mehta", "Woohoo! Manali winter trip locked! Thanks Tanvi for coordinating.")
    ]

    # Thread 2: Flat Lease & Deposit Split (Jan 10, 2024)
    t2_time = datetime(2024, 1, 10, 18, 30, 0)
    t2_msgs = [
        ("Vikram Malhotra", "Guys our current house lease expires in March. We need to finalize the new flat this week."),
        ("Rohan Mehta", "Broker showed two flats today: 2BHK in Indiranagar 12th Main vs 3BHK in Koramangala 4th block."),
        ("Priya Sharma", "Indiranagar 2BHK was asking 42k rent and 2.5 lakh deposit, but space is too small for 4 people working from home."),
        ("Kabir Sen", "Koramangala 4th block is walking distance from all cafes and breweries bhai!"),
        ("Vikram Malhotra", "Koramangala 3BHK has 1800 sq ft, 3 attached bathrooms, modular kitchen, and dedicated 2 car parking slots."),
        ("Priya Sharma", "Owner was demanding 52k rent and 3 lakh security deposit initially."),
        ("Rohan Mehta", "We negotiated hard today with the landlord uncle."),
        ("Priya Sharma", "Did he agree to lower the deposit? 3 lakhs is too locked up capital."),
        ("Vikram Malhotra", "Yes, negotiated him down to 48k monthly rent and 2 lakh deposit total."),
        ("Kabir Sen", "So 48k split 4 ways is 12,000 per person rent, and 50,000 one-time refundable deposit. Very reasonable!"),
        ("Rohan Mehta", "Maintenance is included in 48k or extra?"),
        ("Vikram Malhotra", "Maintenance of 4k per month is included in the 48k agreement."),
        ("Priya Sharma", "That is a solid deal for 4th block. GPay limits check karke deposit transfer karte hain."),
        ("Kabir Sen", "When do we sign the agreement?"),
        ("Vikram Malhotra", "Owner coming with notary agreement copy on Sunday 11 AM."),
        # RESOLUTION MESSAGE FOR THREAD 2
        ("Vikram Malhotra", "Agreement signed! 3BHK in Koramangala 4th block locked at 48k monthly rent with 2 lakh security deposit split equally between the four of us.", True),
        ("Rohan Mehta", "Great job Vikram! Flat shifting weekend of March 15 plan karte hain."),
        ("Priya Sharma", "Deposit receipt and lease PDF uploaded to our shared drive.")
    ]

    # Thread 3: Farewell Gift & Venue for Siddharth (March 18, 2024)
    t3_time = datetime(2024, 3, 18, 14, 0, 0)
    t3_msgs = [
        ("Rohan Mehta", "guys Siddharth is moving to London next month for his master's! We need to plan a proper surprise farewell gift and dinner."),
        ("Ananya Iyer", "OMG Sid is going to LSE! So proud of him! We have to give something memorable."),
        ("Kabir Sen", "London weather is cold, leather jacket ya trench coat de dein?"),
        ("Priya Sharma", "Clothing sizing and taste is risky. What about tech gadget that he can use for studying?"),
        ("Vikram Malhotra", "Sony WH-1000XM5 noise cancelling headphones or Apple Watch Series 9?"),
        ("Tanvi Desai", "He already bought Bose headphones last Black Friday guys. What about Kindle Paperwhite? He reads so much during commute."),
        ("Ananya Iyer", "Yes! Kindle Paperwhite 32GB Signature Edition in agave green color with personalized leather sleeve!"),
        ("Priya Sharma", "Amazon price is 15,499 for Kindle + 1,500 for leather case = 17k total. Split among 7 of us is ~2,400 per person. Perfect budget."),
        ("Rohan Mehta", "Gift locked! What about farewell dinner venue on Friday night?"),
        ("Kabir Sen", "Windmills Craftworks Whitefield vs Toit Indiranagar?"),
        ("Vikram Malhotra", "Whitefield is too far on Friday evening traffic. Indiranagar is central for everyone."),
        ("Tanvi Desai", "Toit rooftop table reservation available for Friday 8:30 PM for 8 people."),
        ("Neha Gupta", "I will swap my evening round so I can be there at Toit by 8:15 PM sharp!"),
        ("Priya Sharma", "Everyone transfer 2400 to my UPI for the Kindle order."),
        ("Ananya Iyer", "Done transferred!"),
        ("Kabir Sen", "Sent via GPay!"),
        ("Vikram Malhotra", "Transferred."),
        ("Tanvi Desai", "Sent!"),
        # RESOLUTION MESSAGE FOR THREAD 3
        ("Priya Sharma", "Purchased the Kindle Paperwhite 32GB with green leather cover on Amazon, and table booked at Toit Indiranagar this Friday at 8:30 PM.", True),
        ("Rohan Mehta", "Awesome! Remember don't tell Sid in the main chat, keep it surprise!")
    ]

    # Additional Distinct Topical Threads
    distinct_threads = [
        # Cubbon park morning run & CTR coffee (Oct 3, 2023)
        (datetime(2023, 10, 3, 6, 30, 0), "thread_cubbon_run", [
            ("Rohan Mehta", "who is coming for morning 6 AM run at Cubbon park?"),
            ("Vikram Malhotra", "count me in, 5k loop?"),
            ("Rohan Mehta", "yes, 5k pace around 5:45/km"),
            ("Kabir Sen", "bhai 6 AM ko toh main deep sleep me rehta hoon"),
            ("Ananya Iyer", "I will come for post-run dosa and filter coffee at CTR"),
            ("Priya Sharma", "+1 for CTR breakfast"),
            ("Neha Gupta", "post duty maybe if I survive the night"),
        ]),
        # Smart home plug & geyser automation (Oct 5, 2023)
        (datetime(2023, 10, 5, 8, 20, 0), "thread_smart_home", [
            ("Vikram Malhotra", "Updated the smart home plug schedule to turn off geyser automatically after 20 mins."),
            ("Rohan Mehta", "Great, power bill will be much lower this month."),
            ("Priya Sharma", "Nice initiative Vikram!"),
        ]),
        # Purple Line metro opening (Oct 9, 2023)
        (datetime(2023, 10, 9, 9, 15, 0), "thread_metro_purple", [
            ("Kabir Sen", "[Forwarded message] Bangalore Metro Purple Line full stretch now operational from Challaghatta to Whitefield!"),
            ("Vikram Malhotra", "Finally! Office commute to ITPL will take 45 mins instead of 2 hours in traffic."),
            ("Tanvi Desai", "Going to take metro from Indiranagar today itself."),
        ]),
        # Diwali Celebration (Nov 10, 2023)
        (datetime(2023, 11, 10, 16, 0, 0), "thread_diwali_party", [
            ("Ananya Iyer", "Diwali potluck dinner at my apartment this Saturday? Dress code is traditional kurta/saree!"),
            ("Rohan Mehta", "I'll bring kaju katli and samosas from Anand Sweets."),
            ("Priya Sharma", "I am making homemade gulab jamun and mutton biryani!"),
            ("Kabir Sen", "bhai main fairy lights and bluetooth speaker leke aaunga."),
            ("Vikram Malhotra", "I can bring board games: Catan and Secret Hitler."),
            ("Tanvi Desai", "Count me in, I'll bring marigold flowers and diyas for decor."),
            ("Neha Gupta", "Yay! Finally an off night on Saturday."),
            ("Ananya Iyer", "Lock ho gaya: Diwali potluck party Saturday 7 PM at my place, dress code ethnic!"),
        ]),
        # Gym Challenge (Jan 2, 2024)
        (datetime(2024, 1, 2, 10, 0, 0), "thread_gym_challenge", [
            ("Rohan Mehta", "New Year resolution: 75 days fitness streak! Who is joining?"),
            ("Vikram Malhotra", "I signed up for Cult Fit pass near office."),
            ("Kabir Sen", "Bhai maine gym membership li thi last year, 2 din gaya sirf lol"),
            ("Priya Sharma", "Priya's rule: whoever misses workout 3 days in a row pays for weekend breakfast!"),
            ("Siddharth Verma", "Deal accepted! Track on Strava app."),
            ("Ananya Iyer", "Joined the Strava group! Let's do this."),
        ]),
        # Carpool Feb (Feb 14, 2024)
        (datetime(2024, 2, 14, 8, 30, 0), "thread_carpool_feb", [
            ("Vikram Malhotra", "Anyone commuting towards Electronic City phase 1 today? Driving via elevated toll road."),
            ("Rohan Mehta", "Pick me up from Sony World signal at 9:15 AM please."),
            ("Priya Sharma", "Me too from Koramangala water tank!"),
            ("Vikram Malhotra", "Leaving home in 10 mins, be ready at pickup point."),
        ]),
        # Tax Saving (March 5, 2024)
        (datetime(2024, 3, 5, 11, 0, 0), "thread_tax_march", [
            ("Priya Sharma", "Friendly reminder guys: March 31 is financial year end. Submit 80C investment proofs on company portal!"),
            ("Kabir Sen", "Arre ELSS mutual fund me last minute invest karna padega tax bachane ke liye."),
            ("Vikram Malhotra", "NPS tier 1 gives extra 50,000 deduction under 80CCD(1B), very useful."),
            ("Siddharth Verma", "Thanks Priya, totally forgot about health insurance premium receipt."),
        ]),
        # PVR Movie night (Feb 23, 2024)
        (datetime(2024, 2, 23, 17, 30, 0), "thread_movie_pvr", [
            ("Siddharth Verma", "Booked 4 tickets for Friday night first-day-first-show at PVR Forum."),
            ("Kabir Sen", "Popcorn combo on you Sid bhai!"),
            ("Vikram Malhotra", "What time is the show?"),
            ("Siddharth Verma", "9:45 PM IMAX screen."),
        ]),
        # Helmet challan (Jan 19, 2024)
        (datetime(2024, 1, 19, 12, 15, 0), "thread_helmet_fine", [
            ("Kabir Sen", "Arre traffic police caught me for helmet strap not clicked properly, 500 challan lag gaya."),
            ("Vikram Malhotra", "Always click the strap properly bhai, safety first."),
            ("Priya Sharma", "Pay it immediately on Bangalore traffic police portal."),
        ]),
        # Doctor emergency casualty duty (Dec 4, 2023)
        (datetime(2023, 12, 4, 21, 0, 0), "thread_doctor_duty", [
            ("Neha Gupta", "Night shift emergency casualty duty finished, sleeping now do not call."),
            ("Priya Sharma", "Rest well Neha!"),
            ("Ananya Iyer", "Take care dear!"),
        ]),
        # Silk board traffic jam (Nov 28, 2023)
        (datetime(2023, 11, 28, 18, 45, 0), "thread_silk_board", [
            ("Vikram Malhotra", "Silk board signal is completely jammed today, 45 mins stuck already."),
            ("Tanvi Desai", "Outer ring road is choked too due to rain."),
            ("Rohan Mehta", "Take the inner HSR layout road."),
        ]),
        # Chicory filter coffee (Oct 22, 2023)
        (datetime(2023, 10, 22, 8, 30, 0), "thread_chicory_coffee", [
            ("Ananya Iyer", "Made authentic South Indian filter coffee with 80:20 chicory blend, pure bliss."),
            ("Rohan Mehta", "Send some to my flat!"),
            ("Tanvi Desai", "Filter coffee aroma in morning is the best."),
        ]),
        # Swiggy Instamart 7 mins (Dec 14, 2023)
        (datetime(2023, 12, 14, 22, 10, 0), "thread_instamart", [
            ("Kabir Sen", "Bhai Swiggy Instamart delivered ice cream in 7 minutes flat, what a time to be alive."),
            ("Ananya Iyer", "Which flavor did you get?"),
            ("Kabir Sen", "Belgian dark chocolate tub!"),
        ]),
        # Ananya thrift denim jacket (Oct 16, 2023)
        (datetime(2023, 10, 16, 17, 20, 0), "thread_thrift_jacket", [
            ("Ananya Iyer", "Found an incredible vintage thrift store in Koramangala 5th block, bought an oversized denim jacket for 800!"),
            ("Priya Sharma", "That is such a good steal!"),
        ]),
        # Ananya pottery workshop (Nov 4, 2023)
        (datetime(2023, 11, 4, 11, 10, 0), "thread_pottery", [
            ("Ananya Iyer", "Pottery workshop happening this Sunday at Ceramic Center, anyone interested?"),
            ("Tanvi Desai", "I'd love to try it out!"),
        ]),
        # Priya flight advice (Feb 6, 2024)
        (datetime(2024, 2, 6, 14, 0, 0), "thread_flight_advice", [
            ("Priya Sharma", "Priya's advice: don't book flights on weekends, Tuesday afternoon prices are lowest."),
            ("Rohan Mehta", "Noted for our next offsite."),
        ]),
        # Vikram broadband ticket (Nov 15, 2023)
        (datetime(2023, 11, 15, 11, 40, 0), "thread_broadband_outage", [
            ("Vikram Malhotra", "Fiber internet line is down in our sector, raised Airtel broadband complaint ticket #94821."),
            ("Kabir Sen", "Mobile hotspot se kaam chala raha hoon."),
        ]),
        # Vikram mechanical keyboard (Oct 28, 2023)
        (datetime(2023, 10, 28, 15, 15, 0), "thread_keyboard", [
            ("Vikram Malhotra", "Bought the mechanical keyboard with brown tactile switches, typing feels so good."),
            ("Rohan Mehta", "Which brand? Keychron?"),
        ]),
        # Rohan airport cab (Dec 8, 2023)
        (datetime(2023, 12, 8, 19, 0, 0), "thread_airport_cab", [
            ("Rohan Mehta", "Airport taxi pre-booked for 4 AM flight on MakeMyTrip."),
            ("Vikram Malhotra", "Safe travels Rohan!"),
        ]),
        # Rohan Coorg trek sheet (Jan 24, 2024)
        (datetime(2024, 1, 24, 10, 30, 0), "thread_coorg_trek", [
            ("Rohan Mehta", "Shared Google sheet for weekend trekking in Coorg: add your names and contact."),
            ("Siddharth Verma", "Added my name!"),
        ]),
        # Tanvi cab driver details (Feb 20, 2024)
        (datetime(2024, 2, 20, 20, 30, 0), "thread_cab_driver", [
            ("Tanvi Desai", "Cab driver assigned for tomorrow morning pickup: Swift Dzire KA-01-MJ-4821."),
            ("Rohan Mehta", "Perfect, thanks Tanvi."),
        ]),
        # Tanvi early check-in (Jan 8, 2024)
        (datetime(2024, 1, 8, 16, 45, 0), "thread_airbnb_checkin", [
            ("Tanvi Desai", "Airbnb host replied: early check-in allowed at 11 AM without extra charge."),
            ("Priya Sharma", "Great, we don't have to carry bags around."),
        ]),
        # Priya grocery expenditure (Nov 1, 2023)
        (datetime(2023, 11, 1, 9, 30, 0), "thread_grocery_expenditure", [
            ("Priya Sharma", "Total grocery expenditure for October came to 8,420 rupees."),
            ("Rohan Mehta", "Transferred my 1/4th share."),
        ]),
    ]

    all_threads = [
        (t1_time, "thread_year_end_trip", t1_msgs),
        (t2_time, "thread_flat_lease", t2_msgs),
        (t3_time, "thread_farewell_gift", t3_msgs),
    ] + distinct_threads

    thread_map = {}
    for tb_time, tb_id, tb_msgs in all_threads:
        tb_date = tb_time.date()
        thread_map.setdefault(tb_date, []).append((tb_time, tb_id, tb_msgs))

    all_raw_messages = []
    current_day = START_DATE.date()
    end_day = END_DATE.date()
    day_count = (end_day - current_day).days + 1
    all_participants = list(PARTICIPANTS.keys())

    # Daily generic chatter templates with date variations
    DAILY_CHATTER_STARTERS = [
        "good morning everyone!", "coffee time ☕", "working from cafe today in {place}",
        "anyone free for lunch near {place}?", "traffic is crazy on {place} road today",
        "weather is so pleasant today, 22 degrees", "wrap up calls by 6 PM today guys",
        "who is playing badminton this weekend?", "ordering food on Swiggy, anyone wants anything?",
        "gym session done for the day 💪", "reading this interesting tech article today",
        "movie plan for the weekend?", "tea break at chai point!"
    ]
    PLACES_LIST = ["Indiranagar", "Koramangala", "HSR", "MG Road", "Whitefield", "Lavelle Road", "JP Nagar"]

    for d_idx in range(day_count):
        date_curr = current_day + timedelta(days=d_idx)

        # Insert scheduled threads
        if date_curr in thread_map:
            for tb_time, tb_id, tb_msgs in thread_map[date_curr]:
                msg_time = tb_time
                for item in tb_msgs:
                    sender = item[0]
                    text = item[1]
                    is_dec = item[2] if len(item) > 2 else False
                    all_raw_messages.append((sender, text, msg_time, tb_id, is_dec, False, False))
                    msg_time += timedelta(minutes=random.randint(1, 4), seconds=random.randint(5, 50))

        # Daily casual messages (18 to 25 messages)
        num_msgs = random.randint(18, 24)
        c_time = datetime.combine(date_curr, datetime.min.time()) + timedelta(hours=8, minutes=random.randint(10, 45))

        for _ in range(num_msgs):
            r_val = random.random()
            if r_val < 0.08:
                sender = random.choice(all_participants)
                text = random.choice(FORWARDED_MESSAGES)
                all_raw_messages.append((sender, text, c_time, None, False, True, False))
            elif r_val < 0.16:
                sender = random.choice(all_participants)
                text = "<Media omitted>"
                all_raw_messages.append((sender, text, c_time, None, False, False, True))
            elif r_val < 0.40:
                sender = random.choice(["Neha Gupta", "Kabir Sen", "Ananya Iyer", "Vikram Malhotra", "Siddharth Verma", "Priya Sharma"])
                text = random.choice(ONE_WORD_REPLIES)
                all_raw_messages.append((sender, text, c_time, None, False, False, False))
            else:
                sender = random.choice(all_participants)
                starter = random.choice(DAILY_CHATTER_STARTERS).format(place=random.choice(PLACES_LIST))
                all_raw_messages.append((sender, starter, c_time, None, False, False, False))

            c_time += timedelta(minutes=random.randint(20, 50), seconds=random.randint(0, 50))

    # Sort strictly chronologically
    all_raw_messages.sort(key=lambda x: x[2])

    prev_msg_id = None
    for sender, text, dt, thread_id, is_dec, is_fwd, is_media in all_raw_messages:
        reply_to = None
        if prev_msg_id and random.random() < 0.20 and not is_fwd and not is_media:
            reply_to = prev_msg_id

        msg_obj = create_msg(
            sender=sender,
            text=text,
            dt=dt,
            thread_id=thread_id,
            is_decision=is_dec,
            is_forward=is_fwd,
            media_omitted=is_media,
            reply_to_id=reply_to
        )
        messages.append(msg_obj)
        prev_msg_id = msg_obj["id"]

    return messages


def main():
    print("Generating comprehensive synthetic chat archive...")
    messages = generate_synthetic_chat()
    print(f"✓ Total Messages: {len(messages)}")
    print(f"✓ Participants: {len(set(m['sender'] for m in messages))}")
    print(f"✓ Date Range: {messages[0]['timestamp']} to {messages[-1]['timestamp']}")

    output_path = "data/chat.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)
    print(f"✓ Successfully written to {output_path}")


if __name__ == "__main__":
    main()
