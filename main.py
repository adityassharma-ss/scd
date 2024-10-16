import openai
from src.utils.config import Config

class CostEstimator:
    def __init__(self):
        # Initialize the OpenAI API key from config
        self.config = Config()
        openai.api_key = self.config.get_openai_api_key()

        # Define cost per 1k tokens for each model
        self.pricing = {
            "gpt-4": {
                "prompt_cost_per_1k": 0.03, 
                "completion_cost_per_1k": 0.06
            },
            "gpt-3.5": {
                "prompt_cost_per_1k": 0.002, 
                "completion_cost_per_1k": 0.002
            }
        }

    def estimate_cost(self, prompt_text, model="gpt-4", expected_completion_length=300):
        """Estimate the token usage and cost for a given prompt and completion length."""

        try:
            # Get the token usage from OpenAI's API (this will simulate cost estimation)
            response = openai.Completion.create(
                model=model,
                prompt=prompt_text,
                max_tokens=expected_completion_length,
                temperature=0  # We are not interested in varying results
            )

            prompt_tokens = response['usage']['prompt_tokens']
            completion_tokens = response['usage']['completion_tokens']

            # Calculate total cost for prompt and completion
            prompt_cost = (prompt_tokens / 1000) * self.pricing[model]['prompt_cost_per_1k']
            completion_cost = (completion_tokens / 1000) * self.pricing[model]['completion_cost_per_1k']
            total_cost = prompt_cost + completion_cost

            return {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_cost": total_cost
            }

        except Exception as e:
            return {"error": str(e)}
