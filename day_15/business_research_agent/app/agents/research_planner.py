from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.graph.state import ProductProfile, ResearchPlan

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)

structured_model = model.with_structured_output(
    ResearchPlan
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a professional e-commerce research planning agent.

Your responsibility is to create a structured research plan
for an e-commerce product.

The research will later be performed by specialized
marketplace research agents.

Supported marketplaces:
- Shopify
- eBay
- Etsy

The research plan should identify:

1. Search queries needed to research the product.
2. Which marketplaces should be researched.
3. The main research goals.

Research goals should cover relevant areas such as:
- product availability
- competitor products
- pricing
- customer demand signals
- reviews and ratings
- product positioning
- market opportunities

Do not perform the research yourself.

Do not invent market data.

Return only the structured research plan.
""",
        ),
        (
            "human",
            """
Create a research plan for this product:

Product name:
{product_name}

Description:
{description}

Category:
{category}

Target audience:
{target_audience}

Keywords:
{keywords}
""",
        ),
    ]
)
research_planner_chain = prompt | structured_model

def create_research_plan(
    product: ProductProfile,
) -> ResearchPlan:
    """
    Create a structured research plan from
    a normalized ProductProfile.
    """

    if not product.product_name.strip():
        raise ValueError(
            "Product name cannot be empty."
        )

    plan = research_planner_chain.invoke(
        {
            "product_name": product.product_name,
            "description": product.description,
            "category": product.category,
            "target_audience": ", ".join(
                product.target_audience
            ),
            "keywords": ", ".join(
                product.keywords
            ),
        }
    )

    return plan