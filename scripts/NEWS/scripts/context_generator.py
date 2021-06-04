# This script generates the context dictionaries for the news generation task

# Imports the time library
import time

# Imports the JSON library
import json

# Imports the datetime library
import datetime

# Prints the log information
print("INFO: Started generating context files")

# Opens the global parameters file
global_params_file = open("./parameters/global_parameters.json", "r")

# Parses and opens the global parameters file
global_params = json.load(global_params_file)

# Creates a datetime instance for start date
start_date = datetime.datetime(
  global_params["start_year"],
  global_params["start_month"],
  global_params["start_day"]
)

# Creates a datetime instance for stop date
stop_date = start_date + datetime.timedelta(days=1)

# Creates a datetime instance for end date
end_date = datetime.datetime(
  global_params["end_year"],
  global_params["end_month"],
  global_params["end_day"]
)

# Creates the generator stop flag
generator_running = True

# Sets the context counter
context_counter = 0

# Main generator loop
while generator_running:

  # Creates the start date string
  start_date_str = "{}-{}-{}".format(
    start_date.year,
    start_date.month,
    start_date.day
  )

  # Creates the stop date string
  stop_date_str = "{}-{}-{}".format(
    stop_date.year,
    stop_date.month,
    stop_date.day
  )

  # Iterates over languages
  for lang in global_params["search"].keys():

    # Iterates over countries
    for country in global_params["search"][lang]["countries"]:

      # Iterates over keywords
      for keyword in global_params["search"][lang]["keywords"]:

        # Creates the context dictionary
        context = {
          "lang": lang,
          "country": country,
          "start_date": start_date_str,
          "stop_date": stop_date_str,
          "keyword": keyword
        }

        # Creates the filepath for context
        context_filepath = "./context/param_" + str(context_counter) + ".json"

        # Opens the context file
        context_file = open(context_filepath, "w")

        # Dumps dictionary to file
        json.dump(
          context,
          context_file,
          indent=0
        )

        # Closes the context file
        context_file.close()

        # Increments context counter
        context_counter += 1  

  # Checks if stop-day equals end-day
  stop_day_flag = stop_date.day == end_date.day

  # Checks if stop-month equals end-month
  stop_month_flag = stop_date.month == end_date.month

  # Checks if stop-year equals stop end-month
  stop_year_flag = stop_date.year == stop_date.year

  # Checks the stop condition: stop-date equals end-date
  if stop_day_flag and stop_month_flag and stop_year_flag:
    
    # Stops the generator if condition is met
    generator_running = False

  # If stop condition is not met then dates are incremented
  else:

    # Start date is incremented
    start_date += datetime.timedelta(days=1)

    # Stop date is incremented
    stop_date += datetime.timedelta(days=1)

# Prints goodbye message
print("INFO: Finished generating context")
