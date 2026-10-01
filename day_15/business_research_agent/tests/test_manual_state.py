
from app.graph.state import (
    ProductProfile,
    MarketplaceProduct,
    MarketplaceResearchResult,
    OpportunityAnalysis,
    AgentState,
)

product = ProductProfile(
    product_name="Solar Garden Light",
    category="Outdoor Lighting",
    target_audience=["Garden owners"],
    keywords=["solar", "garden", "LED"],
)

marketplace = MarketplaceResearchResult(
    marketplace="etsy",
    products=[
        MarketplaceProduct(
            title="Solar Garden Stake Light",
            price=19.99,
            currency="USD",
        )
    ],
)

opportunity = OpportunityAnalysis(
    summary="An illustrative research result.",
    opportunity_score=75,
    strengths=["Seasonal outdoor decor"],
)

state: AgentState = {
    "product_input": "Solar Garden Light",
    "product": product,
    "marketplace_results": {
        "etsy": marketplace
    },
    "opportunity_analysis": opportunity,
}

print("Product:", state["product"].product_name)
print("Marketplace:", state["marketplace_results"]["etsy"].marketplace)
print("Score:", state["opportunity_analysis"].opportunity_score)
print("Schema test passed!")