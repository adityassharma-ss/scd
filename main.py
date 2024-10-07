import openai
from src.config.config import Config

class CostEstimator:
    def __init__(self):
        # Initialize the OpenAI API key from config
        self.config = Config()
        openai.api_key = self.config.get_openai_key()
        
        # Define cost per 1k tokens for each model
        self.pricing = {
            "gpt-4": {"prompt_cost_per_1k": 0.03, "completion_cost_per_1k": 0.06},
            "gpt-3.5": {"prompt_cost_per_1k": 0.002, "completion_cost_per_1k": 0.002}
        }
    
    def estimate_cost(self, prompt_text, model="gpt-4", expected_completion_length=300):
        """Estimate the token usage and cost for a given prompt and completion length."""

        try:
            # Get the token usage from OpenAI's API
            response = openai.Completion.create(
                model=model,
                prompt=prompt_text,
                max_tokens=expected_completion_length
            )

            prompt_tokens = response['usage']['prompt_tokens']
            completion_tokens = response['usage']['completion_tokens']
            total_tokens = prompt_tokens + completion_tokens

            # Get the model-specific pricing
            model_pricing = self.pricing.get(model, None)
            if not model_pricing:
                raise ValueError(f"Unsupported model: {model}")
            
            # Calculate the cost
            prompt_cost = (prompt_tokens / 1000) * model_pricing["prompt_cost_per_1k"]
            completion_cost = (completion_tokens / 1000) * model_pricing["completion_cost_per_1k"]
            total_cost = prompt_cost + completion_cost

            return {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "total_cost": total_cost
            }

        except Exception as e:
            print(f"Error estimating cost: {str(e)}")
            return None


# Example usage (can be removed or kept for testing)
if __name__ == "__main__":
    estimator = CostEstimator()
    prompt = "Generate a detailed security control definition for AWS S3"
    result = estimator.estimate_cost(prompt, model="gpt-4", expected_completion_length=300)
    
    if result:
        print(f"Total tokens used: {result['total_tokens']}")
        print(f"Estimated cost: ${result['total_cost']:.4f}")
