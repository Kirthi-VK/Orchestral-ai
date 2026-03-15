import streamlit as st
from orchestral_ai import TravelPlannerOrchestrator

class DestinationAgent:
    def suggest_destination(self, trip_type):
        destinations = {
            "beach": ["Miami", "Goa", "Thailand"],
            "mountains": ["Mount Everest", "Himalayas", "Alps"],
            "city": ["New York", "Paris", "Tokyo"]
        }
        return destinations.get(trip_type, ["New York"])[0]


class BudgetAgent:
    def check_budget(self, destination, budget):
        costs = {
            "Miami": 250,
            "Goa": 400,
            "Thailand": 300,
            "Mount Everest": 200,
            "Himalayas": 350,
            "Alps": 150,
            "New York": 300,
            "Paris": 450,
            "Tokyo": 400
        }
        cost = costs.get(destination, 300)
        return cost, cost <= budget


class ItineraryAgent:
    def plan_itinerary(self, destination):
        itineraries = {
            "Miami": ["Morning: Beach", "Afternoon: Art gallery", "Evening: Ocean Drive Dinner"],
            "Goa": ["Morning: Surfing", "Afternoon: Pier visit", "Evening: Sunset Drive"],
            "Thailand": ["Morning: Surfing", "Afternoon: lunch in fancy resto", "Evening: Beach Party"],
            "Mount Everest": ["Morning: Mountain Hike", "Afternoon: Museum", "Evening: Downtown Dinner"],
            "Himalayas": ["Morning: Skiing", "Afternoon: Snowshoe Trail", "Evening: Hot Chocolate"],
            "Alps": ["Morning: Skiing", "Afternoon: Snowshoe Trail", "Evening: Hot Chocolate"],
            "New York": ["Morning: Central Park", "Afternoon: Museum of Modern Art", "Evening: Broadway Show"],
            "Paris": ["Morning: Eiffel Tower", "Afternoon: Louvre", "Evening: Seine River Cruise"],
            "Tokyo": ["Morning: Tsukiji Market", "Afternoon: Shibuya Crossing", "Evening: Tokyo Tower"]
        }
        return itineraries.get(destination, ["Full day sightseeing"])


class ReviewAgent:
    def review_plan(self, destination, cost, budget, itinerary):
        feedback = []
        if cost > budget:
            feedback.append(f"Warning: {destination} exceeds your budget by ${cost - budget}")
        if not itinerary:
            feedback.append("Itinerary seems empty.")
        if not feedback:
            feedback.append("Plan looks great!")
        return feedback
        

class TravelPlannerOrchestrator:
    def __init__(self):
        self.destination_agent = DestinationAgent()
        self.budget_agent = BudgetAgent()
        self.itinerary_agent = ItineraryAgent()
        self.review_agent = ReviewAgent()

    def plan_trip(self, trip_type, budget):
        destination = self.destination_agent.suggest_destination(trip_type)
        cost, budget_ok = self.budget_agent.check_budget(destination, budget)
        itinerary = self.itinerary_agent.plan_itinerary(destination)
        feedback = self.review_agent.review_plan(destination, cost, budget, itinerary)
        return {
            "destination": destination,
            "cost": cost,
            "budget_ok": budget_ok,
            "itinerary": itinerary,
            "feedback": feedback
        }

#Streamlit

st.set_page_config(page_title="Smart Travel Planner", layout="centered")
st.title("Smart Travel Planner")
st.write("Demo: Multi-Agent Orchestration in action!")

trip_type = st.selectbox("Select trip type:", ["beach", "mountains", "city"])
budget = st.number_input("Enter your budget ($):", min_value=50, max_value=1000, value=300, step=50)

if st.button("Plan My Trip"):
    orchestrator = TravelPlannerOrchestrator()
    plan = orchestrator.plan_trip(trip_type, budget)

    st.subheader("Destination Recommendation")
    st.write(f"**Destination:** {plan['destination']}")
    st.write(f"**Estimated Cost:** ${plan['cost']} | Within Budget? {'Yes' if plan['budget_ok'] else 'No'}")

    st.subheader("Suggested Itinerary")
    for item in plan['itinerary']:
        st.write(f"- {item}")

    st.subheader("Review Feedback")
    for f in plan['feedback']:
        st.write(f"- {f}")
