df = pd.read_csv(...) # your data here

# the following lines are already in the notebook
contexted = []
n = 7 # the context window size

for i in range(n, len(df['line'])):
  row = []
  prev = i - 1 - n # we additionally substract 1, so each row will contain the current response and 7 previous responses  
  for j in range(i, prev, -1):
    row.append(df['line'][j])
  contexted.append(row)