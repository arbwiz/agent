import difflib

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

def find_arbitrage_bettings(data1, data2):
  """
  Finds arbitrage bettings between two arrays of objects.

  Args:
    array1: The first array of objects.
    array2: The second array of objects.

  Returns:
    A list of arbitrage bettings.
  """

  arbitrage_bettings = []
  analysed_combinations = []

  for event_from_data1 in data1:
    # Find the matching event in the second array.
    event_from_data2_match = None
    for event_from_data2 in data2:
      if compare_strings(event_from_data1["name"], event_from_data2["name"]):
        event_from_data2_match = event_from_data2
        break

    # If there is a match, check if there is an arbitrage betting opportunity.
    if event_from_data2_match is not None:
      # Calculate the arbitrage percentage for both scenarios
      arbitrage_percentage1 = 1 / event_from_data1["selections"][0]["price"] + 1 / event_from_data2_match["selections"][1]["price"]
      arbitrage_percentage2 = 1 / event_from_data1["selections"][1]["price"] + 1 / event_from_data2_match["selections"][0]["price"]

      combination = {
        'event_name': event_from_data2_match["name"],
        'arbitrage_percentage1': arbitrage_percentage1,
        'arbitrage_percentage2': arbitrage_percentage2
      }
      analysed_combinations.append(combination)

      # If the arbitrage percentage is less than 1 for either scenario, then there is an arbitrage betting opportunity.
      if arbitrage_percentage1 < 1 or arbitrage_percentage2 < 1:

        sel1_name = ''
        sel2_name = ''
        price1 = 0
        price2 = 0

        if arbitrage_percentage1 > arbitrage_percentage2:
          sel1_name = event_from_data1["selections"][1]["name"]
          sel2_name = event_from_data2_match["selections"][0]["name"]
          price1 = event_from_data1["selections"][1]["price"]
          price2 = event_from_data2_match["selections"][0]["price"]
        elif arbitrage_percentage1 <= arbitrage_percentage2:
          sel1_name = event_from_data1["selections"][0]["name"]
          sel2_name = event_from_data2_match["selections"][1]["name"]
          price1 = event_from_data1["selections"][0]["price"]
          price2 = event_from_data2_match["selections"][1]["price"]

        arbitrage_bettings.append({
          "event": event_from_data1["name"],
          "arbitrage_percentage": min(arbitrage_percentage1, arbitrage_percentage2),
          "sel1": sel1_name,
          "sel2": sel2_name,
          "odd1": price1,
          "odd2": price2
        })

  return arbitrage_bettings, analysed_combinations


def compare_strings_with_ratio(string1, string2, minimum_ratio):
  matcher = difflib.SequenceMatcher(None, string1, string2)
  ratio = matcher.ratio()
  #if ratio < 0.6 and ratio > 0:
    #debug
    #print('Not match but not 0:' + string1 + " VS " + string2)
  return ratio >= minimum_ratio


def calculate_arbitrage_3_websites(odds):

  arbitrage_possibilities = []

  # Iterate over all possible combinations of bets.

  size = len(odds[0])

  for i in range(size):
    for j in range(size):
      for k in range(size):
        if i == j == k:
          continue
        
        arbitrage_percentage = 1 / odds[i][0] + 1 / odds[j][1] + 1 / odds[k][2]
        
        arbitrage_possibilities.append({
                "arbitrage_percentage": arbitrage_percentage,
                "win": odds[i][0],
                "draw": odds[j][1],
                "lose": odds[k][2],
          })
        
  return arbitrage_possibilities

