Phase 1 — Customer Requirement
1. Customer Problem

Assume our customer is an e-commerce entrepreneur, product researcher, or e-commerce agency who wants to determine whether a product represents a viable market opportunity.

Currently, the customer may have to manually:

Search competing products
Research Shopify stores
Analyze eBay listings
Analyze Etsy listings
Compare competitors
Investigate demand
Analyze pricing
Estimate profitability
Identify risks
Decide whether the opportunity is worth pursuing

This is time-consuming and requires information from multiple sources.

Our system's job

The customer gives the system a product/listing/store research request, and our AI system performs the research and produces a structured business opportunity report.

2. High-Level Customer Workflow
                  CUSTOMER
                     │
                     ▼
             Product / Request
                     │
                     ▼
            Product Extraction
                     │
                     ▼
           Research Planning
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
      Shopify       eBay       Etsy
      Research     Research   Research
          │          │          │
          └──────────┼──────────┘
                     ▼
             Research Aggregation
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
      Competitor    Demand     Profit
       Analysis    Analysis   Analysis
          │          │          │
          └──────────┼──────────┘
                     ▼
             Opportunity Analysis
                     │
                     ▼
             Opportunity Scoring
                     │
                     ▼
              Human Review
                     │
                     ▼
             Final Report
                     │
                     ▼
                  CUSTOMER

This workflow will eventually become our LangGraph architecture.

3. Business Goal

The system should answer questions such as:

"What does the available market research indicate about this product opportunity?"

The report should give the customer evidence-based information about:

Product
Product name
Category
Product characteristics
Target market
Key selling points
Competition
Competitor products
Competitor prices
Product positioning
Market saturation indicators
Competitor strengths/weaknesses
Demand
Demand indicators
Market interest
Seasonality where available
Customer/review signals
Marketplace activity
Profitability
Estimated selling price
Estimated product cost
Estimated gross margin
Relevant selling/advertising costs
Profitability considerations
Opportunity
Market opportunity analysis
Competition analysis
Demand analysis
Profitability analysis
Risks
Supporting evidence
Overall opportunity assessment
4. Important Architecture Principle

We are not going to build one giant AI agent.

Instead:

                 Supervisor / Orchestrator
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
 Product Research   Competitor Research   Market Research
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                    Analysis Layer
              ┌───────────┼───────────┐
              ▼           ▼           ▼
           Demand      Competition   Profit
           Analysis     Analysis    Analysis
              └───────────┼───────────┘
                          ▼
                  Opportunity Engine
                          │
                          ▼
                     Human Review
                          │
                          ▼
                    Report Generator

This gives us clear agent boundaries, which will be important when we implement the LangGraph system.

5. Technology Direction

Our core orchestration technology will be:

LangGraph

And we'll apply what you learned during Days 1–14:

Capability	Where we'll use it
StateGraph	Main workflow
Typed state	Shared workflow state
Nodes	Specialized agents
Conditional routing	Dynamic workflow decisions
Parallel execution	Marketplace research
Reducers	Aggregating research
ToolNode	Tool execution
ReAct	Tool-using agents
Retry/fallback	Research failures
Checkpointing	Durable workflow
HITL	Customer approval/review
Subgraphs	Modular agent workflows
Multi-agent architecture	Specialized researchers
Streaming	Progress updates
Testing	Production reliability
LangSmith	Observability

This is where the previous 14 days become one real system.

6. Today's Design Rule

Before we write even one production implementation file, we will define:

Business Requirements
        ↓
Functional Requirements
        ↓
Non-functional Requirements
        ↓
System Architecture
        ↓
Agent Architecture
        ↓
State Schema
        ↓
Data Contracts
        ↓
Tool Contracts
        ↓
Error Strategy
        ↓
Repository Architecture
        ↓
Implementation

Functional Requirements — First Version

So our system currently has these major functions:

ID	Function
FR-01	Accept product research request
FR-02	Validate customer input
FR-03	Extract normalized product profile
FR-04	Generate research plan
FR-05	Execute Shopify research
FR-06	Execute eBay research
FR-07	Execute Etsy research
FR-08	Aggregate research
FR-09	Analyze competition
FR-10	Analyze demand
FR-11	Analyze profitability
FR-12	Analyze opportunity
FR-13	Support human review
FR-14	Handle revision requests
FR-15	Generate final report
FR-16	Track execution and failures
FR-17	Preserve workflow state
FR-18	Provide observable execution through LangSmith

Non-Functional Specification

We can now freeze the first version:

ID	Requirement
NFR-01	Reliability
NFR-02	Fault tolerance
NFR-03	Scalability
NFR-04	Performance
NFR-05	Cost control
NFR-06	Data accuracy & provenance
NFR-07	Security
NFR-08	Maintainability
NFR-09	Observability
NFR-10	Persistence & recovery
NFR-11	Extensibility
NFR-12	Human control