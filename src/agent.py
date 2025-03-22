from fetchai import fetch

# Your AI's query that it wants to find another
# AI to help it take action on.
query = "Buy me a pair of shoes"

# Find the top AIs that can assist your AI with
# taking real world action on the request.
available_ais = fetch.ai(query)

print(f"{available_ais.get('ais')}")