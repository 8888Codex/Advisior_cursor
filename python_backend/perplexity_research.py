"""
Perplexity Research Module
Contextualizes market research using BusinessProfile data
"""
import os
import httpx
from typing import List, Dict, Optional, Any
from models import BusinessProfile

class PerplexityResearch:
    """Wrapper for Perplexity API with business context"""
    
    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY not found in environment")
        
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.model = "sonar-pro"  # Advanced search with grounding for complex queries
    
    async def research(
        self,
        problem: str,
        profile: Optional[BusinessProfile] = None
    ) -> Dict[str, Any]:
        """
        Perform contextualized market research
        
        Args:
            problem: User's business problem/question
            profile: BusinessProfile for context (optional)
        
        Returns:
            Dict with findings and sources
        """
        # Build contextualized research query
        query = self._build_research_query(problem, profile)
        
        # Call Perplexity API
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a market research analyst. Provide factual, "
                                "data-driven insights with specific statistics, trends, "
                                "and examples. Focus on recent data (2024-2025). "
                                "Include competitive analysis and industry benchmarks when relevant."
                            )
                        },
                        {
                            "role": "user",
                            "content": query
                        }
                    ],
                    "temperature": 0.2,
                    "search_recency_filter": "month",
                    "return_related_questions": False
                }
            )
            response.raise_for_status()
            data = response.json()
        
        # Extract findings and citations
        findings = data["choices"][0]["message"]["content"]
        # Sources can be in 'citations' or 'search_results'
        sources = []
        if "citations" in data:
            sources = data["citations"]
        elif "search_results" in data:
            sources = [result.get("url", "") for result in data["search_results"]]
        
        return {
            "query": query,
            "findings": findings,
            "sources": sources,
            "model": data["model"]
        }
    
    def _build_research_query(
        self,
        problem: str,
        profile: Optional[BusinessProfile]
    ) -> str:
        """Build contextualized research query using business profile"""
        
        if not profile:
            # Generic research without context
            return f"Market research and trends for: {problem}"
        
        # Build rich context from profile (Pydantic uses camelCase attributes)
        context_parts = []
        
        # Industry and company size context
        context_parts.append(
            f"Industry: {profile.industry} "
            f"(company size: {profile.companySize})"
        )
        
        # Target audience context
        context_parts.append(f"Target audience: {profile.targetAudience}")
        
        # Channels context
        if profile.channels:
            channels_str = ", ".join(profile.channels)
            context_parts.append(f"Sales channels: {channels_str}")
        
        # Primary goal context
        goal_map = {
            "growth": "focused on growth and customer acquisition",
            "positioning": "working on brand positioning and differentiation",
            "retention": "improving customer retention and loyalty",
            "launch": "launching new products/services",
            "awareness": "building brand awareness"
        }
        goal_desc = goal_map.get(profile.primaryGoal, profile.primaryGoal)
        context_parts.append(f"Primary goal: {goal_desc}")
        
        # Build final query
        context = ". ".join(context_parts)
        
        query = (
            f"Context: {context}. "
            f"Problem/Question: {problem}. "
            f"\n\nProvide market research including: "
            f"1) Current industry trends and statistics for {profile.industry}, "
            f"2) Competitive landscape and benchmarks, "
            f"3) Best practices for companies of similar size ({profile.companySize}), "
            f"4) Specific data relevant to the problem stated above. "
            f"Focus on actionable insights with recent data (2024-2025)."
        )
        
        return query

# Global instance
perplexity_research = PerplexityResearch()
