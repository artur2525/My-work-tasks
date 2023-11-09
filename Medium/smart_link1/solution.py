from random import choice
from collections import defaultdict
import uvicorn
from fastapi import FastAPI
import random 

app = FastAPI()


# Global dictionaries to store data
recommendations = {}
click_offer_mapping = {}
offer_rewards = {}
offer_actions = {} # Для действий для количества действий (для conversions)


# Sample initial random offer for the first 100 clicks
random.seed(42)  # For reproducibility

@app.on_event("startup")
async def startup_event():
    # Reset statistics on service startup
    recommendations.clear()
    click_offer_mapping.clear()
    offer_rewards.clear()
    offer_actions.clear()

@app.get("/sample/")
def sample(click_id: int, offer_ids: str) -> dict:

    # Parse offer IDs
    offer_ids = [int(offer_id) for offer_id in offer_ids.split(",")]

    # Generate random offer on the first 100 clicks
    if len(click_offer_mapping) < 100:
        offer_id = random.choice(offer_ids)
        sampler = "random"
    else:
        rpc_values = [offer_rewards.get(offer_id, 0) / len(click_offer_mapping) for offer_id in offer_ids]
        max_rpc = max(rpc_values)
        if max_rpc == 0:
            offer_id = offer_ids[0]
        else:
            offer_id = offer_ids[rpc_values.index(max_rpc)]
        sampler = "greedy"

    click_offer_mapping[click_id] = offer_id

    response = {
        "click_id": click_id,
        "offer_id": offer_id,
        "sampler": sampler,
    }

    return response

    
@app.put("/feedback/")
def feedback(click_id: int, reward: float) -> dict:
    response = {
        "click_id": click_id,
        "offer_id": click_offer_mapping[click_id],
        "is_conversion": reward > 0,
        "reward": reward
    }

    if reward > 0:
        offer_id = click_offer_mapping[click_id]
        offer_rewards[offer_id] += reward
        offer_actions[offer_id] += 1

    return response

@app.get("/offer_ids/{offer_id}/stats/")
def stats(offer_id: int) -> dict:
    clicks = len([click_id for click_id, offer in click_offer_mapping.items() if offer == offer_id])
    conversions = offer_actions.get(offer_id, 0)
    reward = offer_rewards.get(offer_id, 0)
    cr = conversions / clicks if clicks > 0 else 0
    rpc = reward / clicks if clicks > 0 else 0

    response = {
        "offer_id": offer_id,
        "clicks": clicks,
        "conversions": conversions,
        "reward": reward,
        "cr": cr,
        "rpc": rpc,
    }
    return response


def main() -> None:
    """Run application"""
    uvicorn.run("app:app", host="localhost")


if __name__ == "__main__":
    main()