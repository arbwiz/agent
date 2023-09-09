def is_two_way_market_surebet(odd1, odd2):
  """
  This function checks if two odds are a surebet.

  Args:
    odd1: The first odd.
    odd2: The second odd.

  Returns:
    True if the odds are a surebet, False otherwise.
  """

  return (1 / odd1 + 1 / odd2) < 1

def calculate_optimal_stake_for_two_way_market(odd1, odd2, stake):
  """
  This function determines how much of a determined stake should be put on each odd to guarantee profit on a sure bet.

  Args:
    odd1: The first odd.
    odd2: The second odd.
    stake: The determined stake.

  Returns:
    The amount to bet on each odd.
  """

  # Calculate the combined probability of winning both bets.
  combined_probability = 1 / odd1 + 1 / odd2

  # Calculate the amount to bet on each odd.
  bet_amount1 = stake * (1 - combined_probability)
  bet_amount2 = stake * combined_probability

  return bet_amount1, bet_amount2


if __name__ == "__main__":
  # Set the odds.
  odd1 = 2.0
  odd2 = 3.0

  # Check if the odds are a surebet.
  is_surebet = is_surebet(odd1, odd2)

  # Print the result.
  print("The odds are a surebet:", is_surebet)
  print(surebet_profit(odd1,odd2,100))