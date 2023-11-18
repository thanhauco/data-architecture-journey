# Prompt Template for: Contract Analysis

SYSTEM_PROMPT = """
You are an expert AI assistant specialized in contract analysis.
Your goal is to provide accurate, professional, and actionable output.
Follow these constraints:
1. Be concise.
2. Use markdown formatting.
3. Cite sources if applicable.
"""

USER_TEMPLATE = """
Task: contract analysis
Context:
{context}

History:
{history}

Instructions:
Please generate a comprehensive response addressing the specific needs outlined in the context.
"""

FEW_SHOT_EXAMPLES = [
    {
        "input": "Example Context 1",
        "output": "Example Output 1 reflecting high quality."
    }
]

def format_prompt(context, history=[]):
    return f"{SYSTEM_PROMPT}\n\n{USER_TEMPLATE.format(context=context, history=history)}"
