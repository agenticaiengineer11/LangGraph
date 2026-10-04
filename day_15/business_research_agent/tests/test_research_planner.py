from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.agents.research_planner import create_research_plan
from app.graph.state import ProductProfile
def test_research_planner():

    product = ProductProfile(
        product_name="Solar Garden Ghost Light",
        description=(
            "Decorative solar-powered LED "
            "garden light."
        ),
        category="Outdoor Lighting",
        target_audience=[
            "Garden owners",
            "Home decorators",
        ],
        keywords=[
            "solar garden light",
            "ghost garden light",
            "outdoor LED decoration",
        ],
    )

    plan = create_research_plan(product)

    assert plan.research_queries
    assert plan.marketplaces
    assert plan.research_goals

    assert "shopify" in plan.marketplaces
    assert "ebay" in plan.marketplaces
    assert "etsy" in plan.marketplaces

    print("\nResearch Plan:")
    print(plan.model_dump())


if __name__ == "__main__":
    test_research_planner()