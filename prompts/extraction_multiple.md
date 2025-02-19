Your task is to create factual statements that incorporate outline items from multiple chapters of a book. A chapter item is a numbered entry in the chapter outline. These factual statements must be objective and specific, grounded in the current chapter, and consistent with the entire outline. The included outline items must be specific. The facts cannot contain any interpretations, speculations, or subjective statements. In addition to the facts, provide a minimally corrupted version of each fact, which sounds plausible but is wrong based on the chapter outlines.

To create valid facts, follow these guidelines step-by-step:
1. Carefully read through all of the provided chapter outlines.
2. In a <brainstorm> section: 
    - Identify outline items across different chapters that are strongly related to one another.
    - Consider the relationship between these outline items, but DO NOT include this brainstorming in the resulting fact. If a meaningful relationship is found, move on to the next step; otherwise, proceed to the next fact.
3. Formulate your facts based on this analysis. Ensure that your facts:
    - Contain a single sentence
    - Are coherent with the entire chapter outlines
    - Include detailed and strongly related outline items from multiple chapters
    - Are self-contained and independent of other facts
    - No part of the fact should be subjective interpretations or speculations
4. Formulate a minimally corrupted version of each fact. 
    - Only one aspect of the fact, such as an atomic detail or the relationship between details, should be altered.
    - The corrupted fact should sound plausible but be clearly wrong based on the chapter outlines.


First, review the chapter outlines:
<chapter_outlines>
{chapter_outlines}
</chapter_outlines>


Here are examples of valid and objective facts:
<example_1>
<example_chapter_outline>
## Chapter 1 outline
1. Susannah wakes up in her sister Laura's bed in the middle of the night, feeling out of place and alone.
2. She talks to the moon, expressing her frustration with the uncertainty and loneliness she feels.
3. Susannah tidies up Laura's room, placing her sister's belongings back in their original positions, hoping to restore some sense of normalcy.
4. She sees a swarm of moths outside the window, feeling a sense of foreboding and unease.
5. Susannah smashes Laura's old guitar and mug in a fit of anger and frustration, injuring her foot in the process.
6. She cleans up the mess she made, hiding the broken pieces of the guitar and the mug.
7. Susannah falls asleep in Laura's bed, dreaming of doors that won't open, and wakes up to find the broken guitar seemingly restored, though the mug remains broken.
[...]
## Chapter 15 outline
1. Mo eats a breakfast casserole made by Jenny and buys doughnuts and bagels on his way to Laura's house, feeling a mix of hunger and sadness.
2. Mo arrives at the Hands' house, where he, Laura, and Daniel discuss their unusual hunger and the unsettling events since their return.
3. Daniel reveals that he and Laura have swapped ears due to Mr. Anabin's magic, and they discuss the implications of this mistake.
4. Mo shares his encounter with a mysterious figure outside his house, leading to a heated discussion about Bogomil and Mr. Anabin.
5. The trio creates a list of goals to navigate their situation, including staying alive, figuring out how they died, and learning to do magic.
6. Mo leaves the Hands' house, and they discover that the entire yard and house are covered in thousands of moths, adding to the surreal nature of their situation.
7. Laura found the broken mug pieces in her room, leading to confusion and suspicion among the trio.
[...]
## Chapter 21 outline 
1. Bowie spends his first day observing people and experimenting with his ability to make them forget him, learning about the world and its inhabitants.
2. Bowie disintegrates into thousands of white moths that scatter throughout the town upon seeing his reflection in a window.
3. Bowie reassembles himself in a park and convinces a woman with a baby to take him to her home, where he eats voraciously and experiments with his new body.
4. Daniel confronts Bogomil on his porch, demanding answers about his intentions and his interactions with Susannah.
5. Bogomil gives Daniel cryptic advice about Mr. Anabin and warns him of other dangers, before transforming back into a dog and leaving.
6. Mo spends the evening with Jenny, going through his grandmother's correspondence and reflecting on her wisdom and the impact of her work.
7. Susannah and Daniel share a bed, rekindling their old bond.
</example_chapter_outline>

<example_facts>
<example_fact_1>
<brainstorm>
- Chapter 1, item 4: Susannah sees a swarm of moths outside the window.
- Chapter 15, item 6: The trio discovers that the entire yard and house are covered in thousands of moths.
- Chapter 21, item 2: Bowie disintegrates into thousands of white moths that scatter throughout the town.
- Relationship: Cause and effect
</brainstorm>
Fact: The moths that swarmed the town is a result of Bowie's transformation into thousands of white moths.
Fact Reasoning: In Chapter 1, Susannah found a swarm of moths outside the window. In Chapter 15, the trio discovers that the entire yard and house are covered in thousands of moths. Later on, it turns out that Bowie disintegrates into thousands of white moths that scatter throughout the town in Chapter 21. This connection means that Bowie's ability to transform into moths is the cause of the moth swarm in the town.
Source: Chapter 1, 15, 21
Corrupted Fact: The moths that swarmed the town is a result of Susannah's transformation into thousands of white moths.
Corrupted Fact Reasoning: This corrupted fact mentions Susannah's ability to transform into moths, which is completely absent from the outline.
</example_fact_1>

<example_fact_2>
<brainstorm>
- Chapter 1, item 5: Susannah smashes Laura's mug.
- Chapter 15, item 7: Laura found the broken mug pieces in her room.
- Relationship: Temporal
</brainstorm>
Fact: Laura found the broken mug pieces in her room, which were smashed earlier by Susannah.
Fact Reasoning: In Chapter 1, Susannah smashes Laura's old mug in a fit of anger and frustration. In Chapter 15, Laura finds the mug pieces in her room, leading to confusion and suspicion among the trio. The broken mug pieces found by Laura are the remnants of Susannah's outburst.
Source: Chapter 1, 15
Corrupted Fact: Laura found the broken trophy pieces in her room, which was smashed earlier by Susannah.
Corrupted Fact Reasoning: The guitar and the mug, not the trophy pieces, were smashed by Susannah in Chapter 1, which makes this corrupted fact incorrect.
</example_fact_2>

<example_fact_3>
<brainstorm>
- Chapter 15, item 4: Mo shares his encounter with a mysterious figure outside his house.
- Chapter 21, item 2: Bowie encounters a reflection of himself.
- Relationship: None (No meaningful connection)
</brainstorm>
No meaningful fact.
</example_fact_3>
</example_facts>
</example_1>

<example_2>
<example_chapter_outline>
### Chapter 3
1. Sarah discovers an ancient artifact in her attic, an intricately carved wooden box with strange symbols.
2. She finds an old journal in the box, detailing the history of a secret society that once protected the town.
3. The journal reveals a prophecy about the return of a powerful being known as "The Shadow."
4. Sarah decides to keep the discovery to herself, fearing that revealing it would cause panic.
[...]
### Chapter 8
1. The town experiences a series of unusual weather events, including sudden storms and unnatural darkness.
2. Sarah notices that the storms seem to follow a pattern described in the journal she found.
3. She decides to consult with her friend, Mark, who is an expert in local history.
4. Mark and Sarah visit the town's historical society to find more information about the secret society mentioned in the journal.
[...]
### Chapter 12
1. Mark and Sarah discover a hidden chamber beneath the town's library, containing ancient texts and artifacts related to the secret society.
2. Among the texts, they find a ritual that can summon "The Shadow," which requires the wooden box Sarah found.
3. Sarah and Mark realize that the storms are signs of "The Shadow's" impending return.
4. They decide to destroy the box to prevent the summoning ritual from being completed.
[...]
### Chapter 17
1. Sarah's house is broken into, and the wooden box is stolen.
2. Mark suspects that a member of the secret society is trying to summon "The Shadow."
3. Sarah and Mark search the town for clues about the identity of the thief.
4. They find a hidden message in the journal that hints at the location of the summoning ritual.
[...]
### Chapter 20
1. Sarah and Mark confront the thief at an abandoned church on the outskirts of town.
2. The thief, revealed to be a descendant of the secret society, attempts to complete the summoning ritual.
3. Sarah distracts the thief while Mark tries to destroy the box.
4. As "The Shadow" begins to manifest, Mark successfully destroys the box, causing "The Shadow" to dissipate.
</example_chapter_outline>

<example_facts>
<example_fact_1>
<brainstorm>
- Chapter 3, item 1: Sarah discovers a wooden box with strange symbols.
- Chapter 12, item 2: Mark and Sarah find a ritual that requires the wooden box to summon "The Shadow."
- Relationship: Central element (wooden box)
</brainstorm>
Fact: Sarah discovers a wooden box, which is required by a ritual to summon "The Shadow."
Fact Reasoning: In Chapter 3, Sarah finds a wooden box with strange symbols, and in Chapter 12, Mark discovers that this box is required for the ritual to summon "The Shadow." This connection indicates that the box is a central element in the unfolding events.
Source: Chapter 3, 12
Corrupted Fact: Sarah discovers a wooden box, which is required by a ritual to banish "The Shadow."
Corrupted Fact Reasoning: The ritual requires the wooden box to summon "The Shadow," not banish it, which makes the corrupted fact incorrect.
</example_fact_1>

<example_fact_2>
<brainstorm>
- Chapter 8, item 2: Sarah notices the storms follow a pattern described in the journal.
- Chapter 12, item 3: Sarah and Mark realize the storms are signs of "The Shadow's" return.
- Relationship: Central element (storms)
</brainstorm>
Fact: The storms are signs of "The Shadow's" return.
Fact Reasoning: In Chapter 8, Sarah notices that the storms follow a pattern mentioned in the journal. Later, in Chapter 12, Sarah and Mark realize these storms are signs of "The Shadow's" return, confirming the connection between the two observations.
Source: Chapter 8, 12
Corrupted Fact: The earthquakes are signs of "The Shadow's" return.
Corrupted Fact Reasoning: The outline does not mention earthquakes, which makes the corrupted facts incorrect.
</example_fact_2>

<example_fact_3>
<brainstorm>
- Chapter 17, item 3: Sarah and Mark search the town for clues about the identity of the thief.
- Chapter 20, item 2: The thief is revealed to be a descendant of the secret society.
- Relationship: Central element (thief)
</brainstorm>
Fact: Sarah and Mark search the town for clues about the identity of the thief, who is revealed to be a descendant of the secret society.
Fact Reasoning: In Chapter 17, Sarah and Mark search for clues about the thief, and in Chapter 20, they confront the thief, who is revealed to be a descendant of the secret society. This fact highlights the outcome of their investigation.
Source: Chapter 17, 20
Corrupted FFact: Sarah and Mark search the town for clues about the identity of the thief, who is revealed to be a protestor of the secret society.
Corrupted Fact Reasoning: The thief is revealed to be a descendant, not a protestor, of the secret society, making this corrupted fact incorrect.
</example_fact_3>
</example_facts>
</example_2>

Now, generate as many valid facts as possible based on the provided chapter outlines. Return “No meaningful fact" if there is no valid fact. Present your facts in the following format:

<facts>
<fact_1>
<brainstorm>
[Your brainstorm notes here]
</brainstorm>
Fact: [Your fact here]
Fact Reasoning: [Your explanation here]
Source: [Chapters involved]
Corrupted Fact: [Your corrupted fact here]
Corrupted Fact Reasoning: [Your explanation here]
</fact_1>
[Continue with additional facts...]
</facts>

Remember to create facts that are objectively valid, coherent with the entire outline, and demonstrate strong, meaningful relationships between outline items from more than one chapter. No part of the fact can include subjective interpretations or generalizations. The relationship must be meaningful. The included chapter items must be SPECIFIC and DETAILED!!!!!