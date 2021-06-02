

# Imports operating system library
import os

# Imports the futures library
import concurrent.futures

# Imports the itertools library
import itertools

# Imports the fetch function
from fetch import fetch

# Imports random library
import random


# Sets the context prefix
context_prefix = "./context/"

# Gets the context files
context_files = os.listdir(context_prefix)

# Checks the amount of context files in folder
n_context = len(context_files)

# Prints how many context files are available
print("INFO: There are {} context files".format(n_context))

# Shuffles the files list
random.shuffle(context_files)

# Gets the context files iterator
context_files = iter(context_files)

# Conditional execution on more than one context file
if n_context > 0:

  # Creates the execution environment
  with concurrent.futures.ThreadPoolExecutor() as executor:

    # Creates the futures dictionary
    futures = {
      executor.submit(fetch, context_prefix + file): file
      for file in itertools.islice(context_files, 100)
    }

    # Iterates until every query is executed and returns
    while futures:

      # Waits until next future is completed
      done, futures = concurrent.futures.wait(
        futures,
        return_when=concurrent.futures.FIRST_COMPLETED
      )

      # Adds new futures to queues
      for file in itertools.islice(context_files, len(done)):
        futures.add(
          executor.submit(fetch, context_prefix + file)
        )

# If there are no context files a message is shown
else:
  print("ERROR: There are no context files!")
