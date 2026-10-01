from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.graph.state import ProductProfile

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)

structured_model = model.with_structured_output(
    ProductProfile
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a professional e-commerce product research analyst.

Your job is to extract a clean and structured product profile
from the customer's raw product input.

Extract only information that can reasonably be inferred from
the provided input.

Do not invent:
- prices
- sales numbers
- reviews
- market demand
- competitors
- profitability

Generate:
- product_name
- description
- category
- target_audience
- keywords
- source_url

If information is missing, use an empty value rather than
inventing information.
""",
        ),
        (
            "human",
            """
Customer product input:

{product_input}
""",
        ),
    ]
)

product_extraction_chain = prompt | structured_model

def extract_product(product_input: str) -> ProductProfile:
    """
    Convert raw customer input into a validated ProductProfile.
    """

    if not product_input or not product_input.strip():
        raise ValueError("Product input cannot be empty.")

    product = product_extraction_chain.invoke(
        {
            "product_input": product_input.strip()
        }
    )

    return product