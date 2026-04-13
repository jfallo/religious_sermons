import pandas as pd
from tqdm import tqdm
import csv, os, json, time
import openai
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


COMPLEXITY_EXAMPLES = """
"complex language" examples:
- Perhaps God's predilection for those words grew out of His acute sense of the thinly veiled fear that grips all who approach the living God.
- It appears that John reserves the most intimate abiding, that is, mutual indwelling, for the Eucharistic presence of Christ. Here, however, he connects it with the Holy Spirit whom he gives to his Church as the alternative way he will abide with us until the End.
- This distinction can help us understand why some remarkable, erudite people are in such quandaries and why some relatively ignorant people have peace of mind and demonstrate integrated living.

"simple language" examples:
- One gentleman did that and he wrote a greeting card. It was 1943 and a bitter season. American troops were fully engaged in World War II.
- So, Jesus is in a house. People were roaming in and out. He's doing a lot of teaching and he's doing some healing along the way.
- One of my favorite things to do as a child was to read the Sunday comics (or the funnies as we called them). Of all the comics I read, the one that I never missed was the Peanuts strip. In one of those cartoons, Lucy demands that Linus change the channel on the TV and then threatens him with her fist if he doesn't.
"""

POLARIZATION_EXAMPLES = """
"polarized langauge" examples:
- America is divided as never before. This is one of the darkest periods of our national history. We have lost the last few generations to drugs, sex and self-gratifying pleasures.
- We need statesmen, not politicians, who are men and women of prayer and who passionately seek God's wisdom through the written Word of God. The courts, media and special interest groups have convinced the American people that we must have freedom from religion in the public square. Nothing is further from the truth. As a nation, we have been increasing the judicial and public approval and practice of shedding innocent blood of the littlest human beings, flaunting all sorts of abominations and sexual sins, forsaking our marriage covenants, calling good evil and evil good, and now pushing even the mention of God's Holy Name out of public life under the false guise of “Separation of Church and State.”
- God has always raised up possible rulers: 1.) Those who serve themselves, taking from the people of God or 2.) Rulers who rule in the true fear of the Lord. Which one will you vote for?

"inclusive language" examples: 
- Everyone, regardless of nationality, language, or economic status, have all marveled at the display of God's glory at one time or another.
- There are many people in the world who would become Christian if only they had the opportunity to do so. Their lives are graced because they cooperate with the grace of God, even though they either never heard of Christ.
- yes her husband could be a deacon - and so could she from that very moment! In fact - every active participant in FirstFamily gets to be a deacon!
"""

CONFIDENCE_EXAMPLES = """
"confident language" examples:
- This brings to bear an important truth: if you can't worship here (heart), then you can't worship here (church building). Because worship is an issue of the heart, not an issue of the building.
- We, on the other hand, worship what we know. Not only because we have the Scriptures that point to Christ, but also because Jesus Himself gives us insight into worship through His words and example.
- It comes from a perfect source, so everything about it is perfect. 
- It is impossible to rightly govern the world without God and the Bible.

"uncertain language" examples:
- He may not have thought of Jesus in the same terms of pre-existence found in the Prologue or in 8:58 or 17:7. More likely, he thought of him in terms of Elijah.
- In all likelihood the Baptist thought of Jesus as this conquering lamb raised up to destroy the world. There is no hint that the Baptist thought of a Messiah in the sense of number four.
- Even though it may seem to be a bit of theological hairsplitting, it appears John wants to protect the flightiness, the mobility, come down like a dove from the sky, of the Spirit.
"""

SCOPE_EXAMPLES = """
"universalist language" examples:
- The Savior of the world would bring good news of great joy for all people. God is all encompassing. His presence permeates and penetrates everything and everyone.
- There are many people in the world who would become Christian if only they had the opportunity to do so. Their lives are graced because they cooperate with the grace of God, even though they either never heard of Christ.
- If you are seeing a barrier in your church that is preventing people from coming into worship, it is your obligation as a follower of Jesus Christ to stop it. Jesus came to the world for all people, and no one should shun anyone from entering a church to worship Him.

"communal language" examples:
- Are you facing a trial right now, dear brother or sister?
- Our theme for the next four weeks is seasoning our season so that the flavor of Christ comes out in our Christmas traditions.
- Say something encouraging to the check-out person. Serve the people who serve you such as the mail carrier or the trash collector.
"""

EMOTION_EXAMPLES = """
"emotional language" examples:
- Me: I grew up going to church pretty regularly, most of the time. I grew up Catholic, as most of you know, and church was an important part of our lives, if for no other reason than we were afraid that missing church might get us sent to hell. Really. And you know what? It's really hard to focus on God and loving Him when you're stuck in church because you're scared of Him. That's not worship, folks. That's fear-filled duty.
- Ouch. But think about it. Please don't raise your hand when I ask this, but how many of you, truly, in your heart, leave "worship" behind when you walk out the door on Sunday? Let me tell you, I do sometimes. I'm wiped out after church, and sometimes all I can think about is my afternoon nap!
- People would stand at their door and sob. One woman had just lost her mother when we arrived and told us that she knew God cared about her after listening to us sing.

"apathetic language" examples:
- Psychology studies the individual, sociology studies groups and societies.
- John the Baptist identifies Jesus as the Lamb of God in verse twenty-nine, as the pre-existent one in verse thirty, and as the transmitter of the Spirit in verses thirty-two to thirty-three and Son of God in verse thirty-four. John begins his work with a poem, called the "Prologue" by scholars, verse one to eighteen, interspersed with prose at verses six to eight and verse fifteen. These latter verses stitch the poem onto the main work. The ideas in the "Prologue," are not found in the gospel proper.
- Sin of the world: In the singular "sin," means "sinful condition,' what Christians mean by "original sin". In the plural it would mean "sinful acts."
"""

REASONING_EXAMPLES = """
"evidentiary language" examples:
- The phrase "church service" doesn't appear anywhere in the Bible. I searched two dozen translations and paraphrases, and found only two instances of that term, one discussing a church service held in a person's home, and the other talking about letting godly men pray.
- In a cascade of testimonials, John the Baptist identifies Jesus as the Lamb of God in verse twenty-nine, as the pre-existent one in verse thirty, and as the transmitter of the Spirit in verses thirty-two to thirty-three.
- Business Week says that total household debt in the US was more than 100 of our disposable annual income last year. IRS tells us that 85 of those reaching age 65 do not have 200 in the bank.

"intuitive language" examples:
- It is humbling to find out that more often than not that person, indeed that "pair," is a divine match, but a human mismatch, a most unlikely combination. Many husbands and wife's will testify to that, if you but listen. Yet God, in His infinite Wisdom, paired you to your spouse, to accomplish His Holy task here on earth.
- Oppressed people throughout history have always turned to God.
- God is all encompassing. His presence permeates and penetrates everything and everyone.
"""

metrics = [
    {
        'name': 'complexity',
        'labels': [
            "complex academic or theological language, abstract concepts, dense sentence structure, sophisticated vocabulary",
            "simple plain language, narrative storytelling, conversational tone, easy-to-follow sentences"
        ],
        'examples': COMPLEXITY_EXAMPLES
    },
    {
        'name': 'polarization',
        'labels': [
            "polarized us-vs-them language, condemning outsiders, culture-war framing, moral blame",
            "inclusive language, welcoming, emphasizing unity, shared dignity, openness to all people"
        ],
        'examples': POLARIZATION_EXAMPLES
    },
    {
        'name': 'confidence',
        'labels': [
            "high-confidence language, moral certainty, definitive truth claims, authoritative tone",
            "low-confidence language, hedging and uncertainty, cautious speculation, tentative interpretation"
        ],
        'examples': CONFIDENCE_EXAMPLES
    },
    {
        'name': 'scope',
        'labels': [
            "universalist language emphasizing all people, global inclusion, everyone belongs",
            "communal language addressing a local group, congregation-focused, shared community identity"
        ],
        'examples': SCOPE_EXAMPLES
    },
    {
        'name': 'emotion',
        'labels': [
            "emotional language, engaging, relatable storytelling, expressing fear, grief, joy, pain, personal vulnerability",
            "emotionally neutral analytical language, detached explanation, academic or informational tone"
        ],
        'examples': EMOTION_EXAMPLES
    },
    {
        'name': 'reasoning',
        'labels': [
            "evidence-based reasoning citing scripture, facts, history, statistics, or textual proof",
            "intuitive reasoning based on personal experience, spiritual feeling, impression, or common sense"
        ],
        'examples': REASONING_EXAMPLES
    }
]


client = openai.OpenAI()
tqdm.pandas()

CHUNK_SIZE = 3000
INPUT_COST  = 2.50 / 1_000_000
OUTPUT_COST = 15.00 / 1_000_000
total_input_tokens = 0
total_output_tokens = 0
cost_lock = threading.Lock()


def get_score(text, labels, examples):
    chunks = [text[i : i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
    scores = []

    def score_chunk(chunk):
        prompt = f"""
You are a text classifier and an expert at analyzing religious sermon texts. Given the text below, determine which of the following better describes the text.

Label A: {labels[0]}
Label B: {labels[1]}

Here are some examples for each label to guide your classification:
{examples}

Text:
\"\"\"
{chunk}
\"\"\"

Respond with ONLY a JSON object in this exact format (no explanation):
{{"score": <float between 0.0 and 1.0>}}
where 1.0 means the passage perfectly matches Label A, 0.0 means it perfectly matches Label B, and 0.5 means it is neutral or equally describes both.
"""
        for attempt in range(3):
            try:
                response = client.chat.completions.create(
                    model= 'gpt-5.4',
                    messages= [{'role': 'user', 'content': prompt}],
                    temperature= 0,
                    response_format= {'type': 'json_object'},
                )

                with cost_lock:
                    global total_input_tokens, total_output_tokens
                    total_input_tokens += response.usage.prompt_tokens
                    total_output_tokens += response.usage.completion_tokens

                return float(json.loads(response.choices[0].message.content)['score'])
            except openai.BadRequestError:
                return 0.5
            except openai.RateLimitError:
                time.sleep(2 ** attempt)
            
        return 0.5

    with ThreadPoolExecutor(max_workers= 8) as executor:
        scores = list(executor.map(score_chunk, chunks))

    return sum(scores) / len(scores)


if not os.path.exists("output/sermons_gpt.csv"):
    df = pd.read_csv("input/sermons.csv")
    df = df.dropna(subset= ['sermontext']).reset_index(drop= True)
    df = df[df['sermontext'].str.len() >= 1500].reset_index(drop= True)
    
    samples = (
        df.groupby('year')
        .apply(lambda x : x.sample(min(len(x), 200), random_state= 42))
        .index.get_level_values(1)
    )
    df_sample = df.loc[samples].reset_index(drop= True)

    for metric in metrics:
        if metric['name'] == 'polarization':
            print(f"Running {metric['name']} classification...")
            with ThreadPoolExecutor(max_workers= 16) as executor:
                futures = {
                    executor.submit(get_score, row['sermontext'], metric['labels'], metric['examples']): i
                    for i, row in df_sample.iterrows()
                }
                results = {}

                for future in tqdm(as_completed(futures), total= len(futures)):
                    i = futures[future]
                    results[i] = future.result()


            df_sample[metric['name'] + '_score'] = pd.Series(results)
            df_sample.to_csv("output/sermons_gpt.csv", index= False, quoting= csv.QUOTE_ALL)

            total_cost = (total_input_tokens * INPUT_COST) + (total_output_tokens * OUTPUT_COST)
            print(f"Input tokens:  {total_input_tokens:,}")
            print(f"Output tokens: {total_output_tokens:,}")
            print(f"Total cost:    ${total_cost:.4f}")
