You will be given a list of facts. Your task is to identify all duplicate facts within this list. A fact is considered a duplicate if it is exactly the same as another fact, or if it contains the same information as another fact, even if worded differently.

Here is the list of facts:

<fact_list>
{fact_list}
</fact_list>

To identify the duplicate facts, follow these guidelines step by step:
1. Read through the list of facts carefully.
2. Identify any facts that are exact duplicates of each other, or that convey the same atomic information using different wording.
3. Return a list of facts that are duplicates of one other, along with an explanation of why they are duplicates.
4. DO NOT return facts that are not duplicates of any other fact in the list.

Here's an example of how your output should look:

<example>
<example_fact_list>
1. Jim worked hard, so he got a promotion.
2. Jim's hard work paid off, and he was promoted.
3. Jim and Sarah worked together on the project.
4. Jim worked hard, so he received praise from his boss, who promoted him.
</example_fact_list>

<example_answer>
- 1, 2: These two facts convey the same atomic information but are worded differently. 
</example_answer>
</example>

Remember, your goal is to identify all duplicate facts, whether they are exact matches or convey the same information in different words. Be thorough in your analysis and clear in your explanations. If there is no duplication in the list, output "No duplicates found."

<answer>
- [Index of duplicate facts, separated by commas]: [Explanation of why they are duplicates]
- [Index of duplicate facts, separated by commas]: [Explanation of why they are duplicates]
(... and so on)
</answer>