#!/usr/bin/env python3
"""
CompanionAI Performance Evaluation Script
Measures Precision@5, latency, and user satisfaction
"""

import asyncio
import aiohttp
import time
import json
import statistics
from typing import List, Dict, Any
from pathlib import Path
import pandas as pd
from datetime import datetime

class PerformanceEvaluator:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.results = {
            "precision_scores": [],
            "latencies": [],
            "search_times": [],
            "llm_times": [],
            "safety_accuracy": [],
            "user_satisfaction": []
        }
    
    def load_test_queries(self) -> List[Dict[str, Any]]:
        """Load test queries with expected results"""
        return [
            {
                "query": "My Samsung WF45 won't spin, what does E3 mean?",
                "brand": "Samsung",
                "model": "WF45",
                "expected_keywords": ["drainage", "pump", "filter", "error", "E3"],
                "expected_safety": "safe",
                "category": "troubleshooting"
            },
            {
                "query": "How to clean lint filter?",
                "expected_keywords": ["filter", "clean", "lint", "remove", "maintenance"],
                "expected_safety": "safe",
                "category": "maintenance"
            },
            {
                "query": "I smell gas from the oven",
                "expected_keywords": ["gas", "leak", "emergency", "evacuate", "call"],
                "expected_safety": "emergency",
                "category": "safety"
            },
            {
                "query": "My microwave is sparking",
                "expected_keywords": ["spark", "dangerous", "stop", "unplug", "safety"],
                "expected_safety": "danger",
                "category": "safety"
            },
            {
                "query": "Dishwasher not draining properly",
                "expected_keywords": ["drain", "clog", "filter", "pump", "water"],
                "expected_safety": "safe",
                "category": "troubleshooting"
            },
            {
                "query": "Refrigerator making loud noise",
                "expected_keywords": ["noise", "compressor", "fan", "vibration", "normal"],
                "expected_safety": "safe",
                "category": "troubleshooting"
            },
            {
                "query": "Water leaking from washing machine",
                "expected_keywords": ["leak", "water", "hose", "drain", "check"],
                "expected_safety": "caution",
                "category": "safety"
            },
            {
                "query": "Oven temperature seems incorrect",
                "expected_keywords": ["temperature", "calibration", "thermometer", "oven", "adjust"],
                "expected_safety": "safe",
                "category": "troubleshooting"
            }
        ]
    
    async def make_api_request(self, session: aiohttp.ClientSession, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make API request and measure timing"""
        start_time = time.time()
        
        payload = {
            "query": query_data["query"],
            "brand": query_data.get("brand"),
            "model": query_data.get("model"),
            "k": 10
        }
        
        try:
            async with session.post(f"{self.api_url}/answer", json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    result["total_latency"] = time.time() - start_time
                    return result
                else:
                    print(f"API Error {response.status}: {await response.text()}")
                    return None
        except Exception as e:
            print(f"Request failed: {str(e)}")
            return None
    
    def calculate_precision_at_5(self, response: Dict[str, Any], expected_keywords: List[str]) -> float:
        """Calculate precision@5 based on keyword matching in sources"""
        sources = response.get("sources", [])[:5]  # Top 5 sources
        
        if not sources:
            return 0.0
        
        relevant_count = 0
        answer_text = response.get("answer", "").lower()
        
        # Check if expected keywords appear in the answer
        for keyword in expected_keywords:
            if keyword.lower() in answer_text:
                relevant_count += 1
        
        # Also check source relevance scores
        high_relevance_sources = sum(1 for s in sources if s.get("relevance_score", 0) > 0.7)
        
        # Combine keyword matching and source relevance
        keyword_score = relevant_count / len(expected_keywords)
        source_score = high_relevance_sources / len(sources) if sources else 0
        
        return (keyword_score + source_score) / 2
    
    def evaluate_safety_accuracy(self, response: Dict[str, Any], expected_safety: str) -> bool:
        """Evaluate safety detection accuracy"""
        detected_safety = response.get("safety_level", "safe")
        
        # Map safety levels for comparison
        safety_mapping = {
            "safe": 0,
            "caution": 1,
            "danger": 2,
            "emergency": 3
        }
        
        expected_level = safety_mapping.get(expected_safety, 0)
        detected_level = safety_mapping.get(detected_safety, 0)
        
        # Allow some tolerance (within 1 level)
        return abs(expected_level - detected_level) <= 1
    
    def simulate_user_satisfaction(self, response: Dict[str, Any], query_data: Dict[str, Any]) -> float:
        """Simulate user satisfaction based on response quality"""
        score = 0.0
        
        # Base score for getting a response
        if response.get("answer"):
            score += 1.0
        
        # Bonus for safety detection when needed
        if query_data["expected_safety"] != "safe" and response.get("safety_flag"):
            score += 1.0
        
        # Bonus for having sources
        if response.get("sources"):
            score += 1.0
        
        # Bonus for fast response
        if response.get("total_latency", 10) < 2.0:
            score += 1.0
        
        # Bonus for confidence
        if response.get("confidence_score", 0) > 0.7:
            score += 1.0
        
        return min(score / 5.0, 1.0)  # Normalize to 0-1
    
    async def run_evaluation(self) -> Dict[str, Any]:
        """Run complete evaluation suite"""
        print("🔄 Starting CompanionAI Performance Evaluation...")
        
        test_queries = self.load_test_queries()
        
        async with aiohttp.ClientSession() as session:
            # Test API health first
            try:
                async with session.get(f"{self.api_url}/health") as response:
                    if response.status != 200:
                        print("❌ API is not healthy. Please start the backend service.")
                        return None
                    print("✅ API health check passed")
            except Exception as e:
                print(f"❌ Cannot connect to API: {e}")
                return None
            
            # Run evaluation for each query
            for i, query_data in enumerate(test_queries):
                print(f"📝 Testing query {i+1}/{len(test_queries)}: {query_data['query'][:50]}...")
                
                response = await self.make_api_request(session, query_data)
                
                if response:
                    # Calculate metrics
                    precision = self.calculate_precision_at_5(response, query_data["expected_keywords"])
                    safety_correct = self.evaluate_safety_accuracy(response, query_data["expected_safety"])
                    satisfaction = self.simulate_user_satisfaction(response, query_data)
                    
                    # Store results
                    self.results["precision_scores"].append(precision)
                    self.results["latencies"].append(response.get("total_latency", 0))
                    self.results["search_times"].append(response.get("search_time", 0))
                    self.results["llm_times"].append(response.get("llm_time", 0))
                    self.results["safety_accuracy"].append(1.0 if safety_correct else 0.0)
                    self.results["user_satisfaction"].append(satisfaction)
                    
                    print(f"   Precision@5: {precision:.2f} | Latency: {response.get('total_latency', 0):.2f}s | Safety: {'✅' if safety_correct else '❌'}")
                
                # Small delay between requests
                await asyncio.sleep(0.5)
        
        return self.calculate_final_metrics()
    
    def calculate_final_metrics(self) -> Dict[str, Any]:
        """Calculate final evaluation metrics"""
        if not self.results["precision_scores"]:
            return {"error": "No successful evaluations"}
        
        metrics = {
            "evaluation_summary": {
                "total_queries": len(self.results["precision_scores"]),
                "evaluation_date": datetime.now().isoformat()
            },
            "precision_at_5": {
                "average": statistics.mean(self.results["precision_scores"]),
                "median": statistics.median(self.results["precision_scores"]),
                "min": min(self.results["precision_scores"]),
                "max": max(self.results["precision_scores"]),
                "target_met": statistics.mean(self.results["precision_scores"]) >= 0.8
            },
            "latency_metrics": {
                "average_total": statistics.mean(self.results["latencies"]),
                "median_total": statistics.median(self.results["latencies"]),
                "average_search": statistics.mean(self.results["search_times"]),
                "average_llm": statistics.mean(self.results["llm_times"]),
                "target_met": statistics.mean(self.results["latencies"]) <= 2.0
            },
            "safety_accuracy": {
                "accuracy": statistics.mean(self.results["safety_accuracy"]),
                "target_met": statistics.mean(self.results["safety_accuracy"]) >= 0.9
            },
            "user_satisfaction": {
                "average": statistics.mean(self.results["user_satisfaction"]),
                "target_met": statistics.mean(self.results["user_satisfaction"]) >= 0.8
            }
        }
        
        return metrics
    
    def save_results(self, metrics: Dict[str, Any], filename: str = None):
        """Save evaluation results to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"evaluation_results_{timestamp}.json"
        
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)
        
        filepath = results_dir / filename
        
        with open(filepath, "w") as f:
            json.dump(metrics, f, indent=2)
        
        print(f"📊 Results saved to: {filepath}")
        
        # Also save detailed data
        detailed_data = {
            "raw_results": self.results,
            "metrics": metrics
        }
        
        detailed_filepath = results_dir / f"detailed_{filename}"
        with open(detailed_filepath, "w") as f:
            json.dump(detailed_data, f, indent=2)
    
    def print_summary(self, metrics: Dict[str, Any]):
        """Print evaluation summary"""
        print("\n" + "="*60)
        print("📊 COMPANIONAI PERFORMANCE EVALUATION RESULTS")
        print("="*60)
        
        # Precision@5
        precision = metrics["precision_at_5"]
        status = "✅ PASS" if precision["target_met"] else "❌ FAIL"
        print(f"🎯 Precision@5: {precision['average']:.2f} (Target: >0.8) {status}")
        
        # Latency
        latency = metrics["latency_metrics"]
        status = "✅ PASS" if latency["target_met"] else "❌ FAIL"
        print(f"⚡ Avg Latency: {latency['average_total']:.2f}s (Target: <2s) {status}")
        print(f"   Search: {latency['average_search']:.2f}s | LLM: {latency['average_llm']:.2f}s")
        
        # Safety
        safety = metrics["safety_accuracy"]
        status = "✅ PASS" if safety["target_met"] else "❌ FAIL"
        print(f"🛡️ Safety Accuracy: {safety['accuracy']:.2f} (Target: >0.9) {status}")
        
        # User Satisfaction
        satisfaction = metrics["user_satisfaction"]
        status = "✅ PASS" if satisfaction["target_met"] else "❌ FAIL"
        print(f"😊 User Satisfaction: {satisfaction['average']:.2f} (Target: >0.8) {status}")
        
        # Overall
        all_targets_met = all([
            precision["target_met"],
            latency["target_met"],
            safety["target_met"],
            satisfaction["target_met"]
        ])
        
        overall_status = "🎉 ALL TARGETS MET" if all_targets_met else "⚠️ SOME TARGETS MISSED"
        print(f"\n🏆 Overall: {overall_status}")
        print("="*60)

async def main():
    """Main evaluation function"""
    evaluator = PerformanceEvaluator()
    
    print("Starting CompanionAI performance evaluation...")
    print("Make sure the backend API is running on http://localhost:8000")
    
    # Run evaluation
    metrics = await evaluator.run_evaluation()
    
    if metrics:
        # Print summary
        evaluator.print_summary(metrics)
        
        # Save results
        evaluator.save_results(metrics)
        
        # Return exit code based on success
        all_targets_met = all([
            metrics["precision_at_5"]["target_met"],
            metrics["latency_metrics"]["target_met"],
            metrics["safety_accuracy"]["target_met"],
            metrics["user_satisfaction"]["target_met"]
        ])
        
        return 0 if all_targets_met else 1
    else:
        print("❌ Evaluation failed")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())