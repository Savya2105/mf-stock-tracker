INSIGHT_GENERATION_PROMPT = """
You are an expert quantitative research analyst and risk manager specialized in Indian mutual fund strategies.
Analyze the following raw transaction delta metrics gathered from a Month-on-Month mutual fund portfolio alignment.

### PORTFOLIO DELTA METRICS SUMMARY:
{summary_stats}

### SIGNIFICANT POSITIONAL ACCUMULATIONS (Top Additions/New Entries):
{top_buys}

### SIGNIFICANT POSITIONAL REDUCTIONS (Top Liquidation/Exits):
{top_sells}

### EXECUTION REQUIREMENTS:
Provide an expert evaluation of these changes. Your final analysis must include:
1. STRATEGIC POSITIONING ANALYSIS: Interpret the intent behind the major accumulations and liquidations. What specific themes or structural updates are being executed?
2. CONCENTRATION & RISK ASSESSMENTS: Evaluate shifts in individual asset concentrations. Identify if the fund is building high-conviction momentum plays or defensively raising cash/liquidation frameworks.
3. LIQUIDITY TRENDS: Analyze the operational ease or scale of these adaptations relative to standard market floats where visible.

Format your output into clear, crisp Markdown with clear thematic sections.
"""