Your task is to create factual statements that incorporate outline items from a single chapter of a book. A chapter item is a numbered entry in the chapter outline. These factual statements must be objective and specific, grounded in the current chapter, and consistent with the entire outline. The included outline items must be specific. The facts cannot contain any interpretations, speculations, or subjective statements. In addition to each fact, provide a minimally corrupted version of the facts, which sounds plausible but is wrong based on the chapter outlines and book summary.

To create valid facts, follow these guidelines step-by-step:
1. Carefully read through the book summary and the provided chapter outline.
2. In a <brainstorm> section: 
    - Identify different outline items that are strongly related to one another.
    - Consider the relationship between these outline items, but DO NOT include this brainstorming in the resulting fact. If a meaningful relationship is found, move on to the next step; otherwise, proceed to the next fact.
3. Formulate your facts based on this analysis. Ensure that your facts:
    - Contain a single sentence
    - Are coherent with the book summary and chapter outline
    - Include multiple detailed and strongly related outline items from the provided chapter
    - Are self-contained and independent of other facts
    - No part of the fact should be subjective interpretations or speculations
    - Do not contradict or duplicate existing facts
4. Formulate a minimally corrupted version of each fact. 
    - Only one aspect of the fact, such as an atomic detail or the relationship between details, should be altered.
    - The corrupted fact should sound plausible but be clearly wrong based on the chapter outlines.

First, read the book summary for an overview:
<summary>
{book_summary}
</summary>

Next, review the chapter outline:
<chapter_outlines>
{chapter_outline}
</chapter_outlines>

Finally, review the existing facts:
<existing_facts>
{existing_facts}
</existing_facts>

Here are two examples of good, objective facts:
<example_1>
<example_summary>
Laura Hand, Daniel Knowe, and Mo Gorch mysteriously return from a realm of death with altered memories, orchestrated by their enigmatic music teacher, Mr. Anabin, and the sinister Bogomil. As they grapple with their new realities, including Mo’s discovery of his grandmother's death and Daniel’s complex feelings for Laura's sister, Susannah, they face trials set by Anabin and Bogomil to remain in the living world. Alongside Bowie, another returned soul, they uncover the truth about their deaths while dealing with eerie supernatural encounters. Laura's newfound magical abilities strain her relationship with Susannah, leading to increasing tensions as Susannah begins to remember the truth.

As the trio navigates their altered lives, they become entangled in a larger, dangerous game orchestrated by Malo Mogge, Anabin, and Bogomil, who guard the door between life and death. Mo and Susannah discover that a Harmony guitar, hidden by Susannah, is the key sought by Malo Mogge, a powerful entity seeking immense power. The story culminates in a chaotic battle in Lovesend, where Laura, consumed by grief, vows to kill Malo Mogge. After absorbing Mogge's magic and becoming a powerful goddess, Laura faces the challenge of balancing her divine powers with her passion for music, while the other characters embrace their new roles. 
</example_summary>

<example_chapter_outline>
## Chapter 15 outline
1. Susannah gets frustrated about Laura and Daniel being close to each other and smashes Laura's old guitar in a fit of anger and frustration.
2. Mo eats a breakfast casserole made by Jenny and buys doughnuts and bagels on his way to Laura's house, feeling a mix of hunger and sadness.
3. Daniel reveals that he and Laura have swapped ears due to Mr. Anabin's magic, and they discuss the implications of this mistake.
4. Laura and Daniel eat ramen to satisfy their unusual hunger. 
5. Mo shares his encounter with a mysterious figure outside his house, leading to a heated discussion about Bogomil and Mr. Anabin.
6. They attempt to perform magic by trying to transform a saltshaker into a hairless cat but fail, leading to further frustration.
7. The trio creates a list of goals to navigate their situation, including staying alive, figuring out how they died, and learning to do magic.
8. Mo leaves the Hands' house, and they discover that the entire yard and house are covered in thousands of moths, adding to the surreal nature of their situation.
9. Laura finds the broken guitar pieces in her room, causing confusion and suspicion among the trio.
</example_chapter_outline>

<example_existing_facts>
- Fact 1: Susannah and Laura are sisters with different personalities and interests, with Susannah being more rebellious and impulsive, while Laura is more reserved and thoughtful.
- Fact 2: Laura, Daniel, and Mo return from a realm of death, contradicting Susannah's belief that they were in Ireland.
</example_existing_facts>

<example_facts>
<example_fact_1>
<brainstorm>
- Chapter 15, item 1: Susannah smashes Laura's old guitar in a fit of anger and frustration.
- Chapter 15, item 9: Laura finds the broken guitar pieces in her room.
- Relationship: Temporal
</brainstorm>
Fact: Laura found the broken guitar pieces in her room, which was smashed earlier by Susannah.
Fact Reasoning: In Chapter 15, Susannah smashes Laura's old guitar in a fit of anger and frustration. Later, Laura discovers the broken guitar pieces in her room, causing confusion and suspicion among the trio. The temporal relationship between the two events suggests a connection between Susannah's outburst and the broken guitar pieces found by Laura.
Source: Chapter 15 (Item 1, 9)
Corrupted Fact: Susannah found the broken guitar pieces in her room, which was smashed earlier by Laura.
Corrupted Fact Reasoning: This corrupted fact misattributes the discovery of the broken guitar pieces to Susannah instead of Laura.
</example_fact_1>

<example_fact_2>
<brainstorm>
- Chapter 15, item 2: Mo feels a mix of hunger and sadness.
- Chapter 15, item 4: Laura and Daniel are eating ramen to satisfy their unusual hunger.
- Relationship: Mutual experience
</brainstorm>
Fact: Mo, Laura, and Daniel were all hungry, with Mo still hungry after Jenny's casserole, and Laura and Daniel had to eat ramen to satisfy their hunger.
Fact Reasoning: In Chapter 15, Mo feels a mix of hunger and sadness, despite eating Jenny's breakfast casserole. Meanwhile, Laura and Daniel are eating ramen to satisfy their unusual hunger, indicating a shared experience of hunger among the trio. This connection highlights the surreal nature of their situation and the impact of Mr. Anabin's magic on their physical needs.
Source: Chapter 15 (Item 2, 4)
Corrupted Fact: Mo was not hungry after eating Jenny's casserole, but Laura and Daniel had to eat ramen to satisfy their hunger.
Corrupted Fact Reasoning: This corrupted fact contradicts item 2, where Mo still feels a mix of hunger and sadness despite eating Jenny's breakfast casserole.
</example_fact_2>
</example_facts>
</example_1>

<example_fact_3>
<brainstorm>
- Chapter 15, item 6: The trio is frustrated after failing to transform a saltshaker into a hairless cat.
- Chapter 15, item 8: Mo leaves the Hands' house. 
- Relationship: None (No meaningful connection)
</brainstorm>
No meaningful fact.
</example_fact_3>
</example_facts>
</example_1>

<example_2>
<example_summary>
Sarah Wiegreff discovers an ancient wooden box with strange symbols in her attic, which contains a journal revealing the history of a secret society and a prophecy about the return of a powerful being known as "The Shadow." As unusual events begin to plague her town, Sarah, along with her friend Mark, uncovers clues that connect these occurrences to the prophecy. They find a hidden chamber beneath the town containing ancient texts and artifacts, including a weapon capable of banishing "The Shadow." With this weapon, they confront a member of the secret society who attempts to summon "The Shadow," and after a tense battle, Sarah successfully uses the weapon to banish the being, restoring peace to the town.

Throughout the story, the connection between the ancient artifact, the journal, and the unfolding events reveals the central role of the wooden box and the secret society in the impending danger. Sarah and Mark's journey highlights their struggle to protect their town from supernatural forces while deciphering the mysterious symbols and prophecies tied to the powerful entity, "The Shadow."
</example_summary>

<example_existing_facts>
- Fact 1: Sarah and Mark confront Myander, a member of the secret society who attempts to summon "The Shadow."
- Fact 2: Sarah successfully uses a machine gun to banish "The Shadow."
</example_existing_facts>

<example_chapter_outline>
## Chapter 3 outline
1. Sarah discovers an ancient artifact in her attic, an intricately carved wooden box with strange symbols.
2. She finds an old journal in the box, detailing the history of a secret society that once protected the town.
3. The journal reveals a prophecy about the return of a powerful being known as "The Shadow."
4. Sarah decides to keep the discovery to herself, fearing that revealing it would cause panic.

## Chapter 8 outline
1. Sarah begins to notice strange occurrences around town, like unusual weather patterns and eerie shadows.
2. She consults the journal again and discovers a passage that seems to describe unusual event patterns as signs of "The Shadow's" return.
3. Sarah's friend Mark, who is a local historian, suggests that they investigate further by visiting the town's library.
4. At the library, they find more texts related to the secret society and "The Shadow."
<example_chapter_outline>

<example_facts>
<example_fact_1>
<brainstorm>
- Chapter 3, item 1: Sarah discovers an ancient artifact, a wooden box with strange symbols.
- Chapter 3, item 2: Sarah finds an old journal in the box, detailing the history of a secret society.
- Relationship: Temporal. 
</brainstorm>
Fact: Sarah discovers a wooden box with strange symbols, which contains a journal detailing the history of a secret society.
Fact Reasoning: In Chapter 3, Sarah finds a wooden box with strange symbols, and inside it, she discovers a journal that reveals the history of a secret society. The connection between the artifact and the journal establishes the importance of the box in the story.
Source: Chapter 3
Corrupted Fact: Sarah discovers a wooden box with strange symbols, which contains a crystal ball revealing the future.
Corrupted Fact Reasoning: This corrupted fact introduces a crystal ball, which is not part of the chapter outline.
</example_fact_1>

<example_fact_2>
<brainstorm>
- Chapter 8, item 1: Sarah notices strange occurrences around town, like unusual weather patterns.
- Chapter 8, item 1: Sarah discovers a passage in the journal that describes these occurrences as signs of "The Shadow's" return.
- Relationship: Temporal
</brainstorm>
Fact: Sarah notices unusual weather patterns around town, which are described in the journal as signs of "The Shadow's" return.
Fact Reasoning: In Chapter 8, Sarah observes unusual weather patterns and other strange occurrences around town. She then finds a passage in the journal that links these events to the return of "The Shadow," suggesting that the events are connected to the prophecy.
Source: Chapter 8
Corrupted Fact: Sarah notices unusual weather patterns around town, which are described in the journal as signs of "The Sun God's" arrival.
Corrupted Fact Reasoning: This corrupted fact focuses on "The Sun God," which is absent from the story
</example_fact_2>
</example_facts>
</example_2>

Now, generate as many valid facts as possible based on the provided chapter outline. Return “No meaningful fact" if there is no valid fact. Present your facts in the following format:

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

Remember to create facts that are objectively valid, coherent with the outline, and demonstrate strong, meaningful relationships between the outline items. No part of the fact can include subjective interpretations or generalizations. The relationship must be meaningful. The included chapter items must be SPECIFIC and DETAILED!!!!!