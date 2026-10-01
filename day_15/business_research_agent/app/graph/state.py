
from typing import Annotated, Literal
from typing_extensions import TypedDict
from operator import add
from datetime import datetime, timezone

from pydantic import BaseModel, Field, HttpUrl

class ProductProfile(BaseModel):
    product_name: str = Field(
        description="Canonical name of the product"
    )
    description: str = Field(
        default="",
        description="Detailed product description"
    )
    category: str = Field(
        default="",
        description="Product category"
    )
    target_audience: list[str] = Field(
        default_factory=list
    )
    keywords: list[str] = Field(
        default_factory=list
    )
    source_url: str | None = None

class ResearchPlan(BaseModel):
    research_queries: list[str] = Field(
        default_factory=list
    )
    marketplaces: list[
        Literal["shopify", "ebay", "etsy"]
    ] = Field(
        default_factory=lambda: [
            "shopify", "ebay", "etsy"
        ]
    )
    research_goals: list[str] = Field(
        default_factory=list
    )

class ResearchSource(BaseModel):
    title: str
    url: str
    marketplace: str
    retrieved_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class MarketplaceProduct(BaseModel):
    title: str
    price: float | None = None
    currency: str = "USD"
    url: str | None = None
    seller: str | None = None
    reviews_count: int | None = None
    rating: float | None = None

class MarketplaceResearchResult(BaseModel):
    marketplace: Literal["shopify", "ebay", "etsy"]
    status: Literal[
        "success", "partial", "failed", "skipped"
    ] = "success"
    products: list[MarketplaceProduct] = Field(
        default_factory=list
    )
    demand_signals: list[str] = Field(
        default_factory=list
    )
    sources: list[ResearchSource] = Field(
        default_factory=list
    )
    errors: list[str] = Field(
        default_factory=list
    )
    retrieved_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class AnalysisResult(BaseModel):
    summary: str
    findings: list[str] = Field(
        default_factory=list
    )
    evidence: list[str] = Field(
        default_factory=list
    )
    assumptions: list[str] = Field(
        default_factory=list
    )
    limitations: list[str] = Field(
        default_factory=list
    )

class ProfitAnalysis(BaseModel):
    selling_price: float | None = None
    product_cost: float | None = None
    shipping_cost: float | None = None
    advertising_cost: float | None = None
    other_costs: float = 0.0
    estimated_profit: float | None = None
    profit_margin_percent: float | None = None
    assumptions: list[str] = Field(
        default_factory=list
    )

class OpportunityAnalysis(BaseModel):
    summary: str
    opportunity_score: float | None = Field(
        default=None, ge=0, le=100
    )
    strengths: list[str] = Field(
        default_factory=list
    )
    risks: list[str] = Field(
        default_factory=list
    )
    evidence: list[str] = Field(
        default_factory=list
    )
    assumptions: list[str] = Field(
        default_factory=list
    )

class ResearchReport(BaseModel):
    product: ProductProfile
    competitor_analysis: AnalysisResult | None = None
    demand_analysis: AnalysisResult | None = None
    profit_analysis: ProfitAnalysis | None = None
    opportunity_analysis: OpportunityAnalysis | None = None
    recommendations: list[str] = Field(
        default_factory=list
    )
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class AgentState(TypedDict, total=False):
    product_input: str
    product: ProductProfile
    research_plan: ResearchPlan

    marketplace_results: dict[
        str, MarketplaceResearchResult
    ]

    competitor_analysis: AnalysisResult
    demand_analysis: AnalysisResult
    profit_analysis: ProfitAnalysis
    opportunity_analysis: OpportunityAnalysis

    review_status: Literal[
        "pending", "approved", "revision_requested"
    ]
    review_feedback: str

    report: ResearchReport
    errors: Annotated[list[str], add]
    execution_status: str