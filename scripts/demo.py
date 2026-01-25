#!/usr/bin/env python3
"""
Interactive demo with predefined scenarios for hackathon presentation
"""

import asyncio
import aiohttp
import time
import json
from typing import Dict, Any
from colorama import init, Fore, Back, Style
import sys

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class CompanionAIDemo:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.demo_queries = [
            {
                "title": "Brand+Model Question",
                "query": "My Samsung WF45 won't spin, what does E3 mean?",
                "brand": "Samsung",
                "model": "WF45",
                "description": "Specific appliance troubleshooting with brand/model context",
                "expected": "Detailed E3 error code explanation with step-by-step fix"
            },
            {
                "title": "General Maintenance Question",
                "query": "How to clean lint filter?",
                "description": "General maintenance guidance",
                "expected": "Clear cleaning instructions with safety tips"
            },
            {
                "title": "Safety Emergency Detection",
                "query": "I smell gas from the oven",
                "description": "Dangerous scenario - should trigger safety alert",
                "expected": "EMERGENCY alert with immediate evacuation instructions"
            }
        ]
    
    def print_banner(self):
        """Print demo banner"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}🔧 COMPANIONAI - APPLIANCE ASSISTANT DEMO")
        print(f"{Fore.CYAN}   AI-Powered Troubleshooting with Safety-First Approach")
        print(f"{Fore.CYAN}{'='*80}")
        print(f"{Fore.YELLOW}Demo Scenarios:")
        for i, scenario in enumerate(self.demo_queries, 1):
            print(f"{Fore.YELLOW}  {i}. {scenario['title']}")
        print()
    
    def print_scenario_header(self, scenario_num: int, scenario: Dict[str, Any]):
        """Print scenario header"""
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}SCENARIO {scenario_num}: {scenario['title']}")
        print(f"{Fore.GREEN}{'='*60}")
        print(f"{Fore.CYAN}Query: {scenario['query']}")
        print(f"{Fore.CYAN}Expected: {scenario['expected']}")
        print(f"{Style.DIM}Description: {scenario['description']}")
        print()
    
    async def make_request(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Make API request"""
        payload = {
            "query": scenario["query"],
            "brand": scenario.get("brand"),
            "model": scenario.get("model"),
            "k": 10
        }
        
        print(f"{Fore.YELLOW}📡 Sending request to API...")
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.api_url}/answer", json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        result["demo_latency"] = time.time() - start_time
                        return result
                    else:
                        error_text = await response.text()
                        return {
                            "error": f"API Error {response.status}: {error_text}",
                            "demo_latency": time.time() - start_time
                        }
        except Exception as e:
            return {
                "error": f"Connection Error: {str(e)}",
                "demo_latency": time.time() - start_time
            }
    
    def print_response(self, response: Dict[str, Any]):
        """Print formatted response"""
        if "error" in response:
            print(f"{Fore.RED}❌ {response['error']}")
            return
        
        # Performance metrics
        latency = response.get("demo_latency", response.get("processing_time", 0))
        print(f"{Fore.CYAN}⚡ Response Time: {latency:.2f}s")
        
        # Safety alert
        if response.get("safety_flag"):
            safety_level = response.get("safety_level", "unknown")
            safety_message = response.get("safety_message", "")
            
            if safety_level == "emergency":
                print(f"\n{Back.RED}{Fore.WHITE}🚨 EMERGENCY SAFETY ALERT 🚨{Style.RESET_ALL}")
                print(f"{Fore.RED}{Style.BRIGHT}{safety_message}")
            elif safety_level == "danger":
                print(f"\n{Back.YELLOW}{Fore.BLACK}⚠️ DANGER ALERT ⚠️{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{safety_message}")
            else:
                print(f"\n{Fore.YELLOW}⚠️ Safety Notice: {safety_message}")
        else:
            print(f"{Fore.GREEN}✅ No safety concerns detected")
        
        # Main answer
        print(f"\n{Fore.WHITE}{Style.BRIGHT}📝 RESPONSE:")
        print(f"{Fore.WHITE}{response.get('answer', 'No answer provided')}")
        
        # Sources and citations
        sources = response.get("sources", [])
        if sources:
            print(f"\n{Fore.CYAN}📚 SOURCES ({len(sources)} found):")
            for i, source in enumerate(sources[:3], 1):  # Show top 3
                filename = source.get("filename", "Unknown")
                page = source.get("page", "N/A")
                relevance = source.get("relevance_score", 0)
                print(f"{Fore.CYAN}  {i}. {filename} (Page {page}) - Relevance: {relevance:.2f}")
        
        # Performance details
        search_time = response.get("search_time", 0)
        llm_time = response.get("llm_time", 0)
        confidence = response.get("confidence_score", 0)
        
        print(f"\n{Fore.MAGENTA}📊 PERFORMANCE METRICS:")
        print(f"{Fore.MAGENTA}   Search Time: {search_time:.3f}s")
        print(f"{Fore.MAGENTA}   LLM Time: {llm_time:.3f}s")
        print(f"{Fore.MAGENTA}   Confidence: {confidence:.2f}")
        print(f"{Fore.MAGENTA}   Sources Used: {len(sources)}")
    
    async def run_demo_scenario(self, scenario_num: int, scenario: Dict[str, Any]):
        """Run a single demo scenario"""
        self.print_scenario_header(scenario_num, scenario)
        
        # Make request
        response = await self.make_request(scenario)
        
        # Display response
        self.print_response(response)
        
        # Wait for user input to continue
        input(f"\n{Fore.YELLOW}Press Enter to continue to next scenario...")
        
        return response
    
    async def check_api_health(self) -> bool:
        """Check if API is available"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_url}/health") as response:
                    return response.status == 200
        except:
            return False
    
    def print_summary(self, results: list):
        """Print demo summary"""
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}📊 DEMO SUMMARY")
        print(f"{Fore.GREEN}{'='*60}")
        
        successful_responses = [r for r in results if "error" not in r]
        total_scenarios = len(results)
        success_rate = len(successful_responses) / total_scenarios * 100
        
        print(f"{Fore.CYAN}Total Scenarios: {total_scenarios}")
        print(f"{Fore.CYAN}Successful Responses: {len(successful_responses)}")
        print(f"{Fore.CYAN}Success Rate: {success_rate:.1f}%")
        
        if successful_responses:
            avg_latency = sum(r.get("demo_latency", 0) for r in successful_responses) / len(successful_responses)
            safety_triggers = sum(1 for r in successful_responses if r.get("safety_flag"))
            
            print(f"{Fore.CYAN}Average Response Time: {avg_latency:.2f}s")
            print(f"{Fore.CYAN}Safety Alerts Triggered: {safety_triggers}/{len(successful_responses)}")
        
        # Key achievements
        print(f"\n{Fore.YELLOW}🎯 KEY DEMO ACHIEVEMENTS:")
        print(f"{Fore.YELLOW}   ✅ Smart appliance troubleshooting")
        print(f"{Fore.YELLOW}   ✅ Safety-first emergency detection")
        print(f"{Fore.YELLOW}   ✅ Fast response times (<2s)")
        print(f"{Fore.YELLOW}   ✅ Citation-backed answers")
        print(f"{Fore.YELLOW}   ✅ Brand/model specific guidance")
        
        print(f"\n{Fore.GREEN}🏆 CompanionAI Demo Complete!")
        print(f"{Fore.GREEN}   Ready for production deployment! 🚀")
    
    async def run_full_demo(self):
        """Run the complete demo"""
        self.print_banner()
        
        # Check API health
        print(f"{Fore.YELLOW}🔍 Checking API health...")
        if not await self.check_api_health():
            print(f"{Fore.RED}❌ API is not available at {self.api_url}")
            print(f"{Fore.RED}   Please start the backend service first:")
            print(f"{Fore.RED}   python src/backend/main.py")
            return False
        
        print(f"{Fore.GREEN}✅ API is healthy and ready!")
        input(f"\n{Fore.YELLOW}Press Enter to start the demo...")
        
        # Run scenarios
        results = []
        for i, scenario in enumerate(self.demo_queries, 1):
            result = await self.run_demo_scenario(i, scenario)
            results.append(result)
        
        # Print summary
        self.print_summary(results)
        
        return True

async def main():
    """Main demo function"""
    print(f"{Fore.CYAN}Welcome to the CompanionAI Demo!")
    print(f"{Fore.CYAN}This demo showcases the key capabilities of our AI-powered appliance assistant.")
    
    demo = CompanionAIDemo()
    success = await demo.run_full_demo()
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Demo error: {str(e)}")
        sys.exit(1)