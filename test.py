# Sortowanie. 
# Napisz algorytm, sortujący tablice obiektów po różnych kluczach.
# Stopnie ważności kluczy: A,B,C 
# [{a:2, b:3, c:4}, 
# {a:1, b:10, c:8},
# {a:2, b:3, c:5},
# {a:2, b:1,c:5},
# {a:0, b:10, c:8}]
# result
# [{a:0, b:10, c:8},
# {a:1, b:10, c:8},
# {a:2, b:1, c:5}, 
# {a:2, b:3, c:4},
# {a:2, b:3, c:5}]

key_priority = ['a', 'b', 'c']

original_data = [{'a':2, 'b':3, 'c':4},
                 {'a':1, 'b':10, 'c':8},
                 {'a':2, 'b':3, 'c':5},
                 {'a':2, 'b':1, 'c':5},
                 {'a':0, 'b':10, 'c':8}]

sorted_data = []
p1_values = dict()
p2_values = dict()
p3_values = dict()

for i in range(len(original_data)):
    # value for first prioriy
    p1 = original_data[i].get(key_priority[0])
    p1_values[i] = p1
    # value for second priority
    p2 = original_data[i].get(key_priority[1])
    p2_values[i] = p2

    # value for third priority
    p3 = original_data[i].get(key_priority[2])
    p3_values[i] = p3

print(p1_values)
print(p2_values)
print(p3_values)

min_index_p1 = 0
min_value = 0

for key in p1_values:
   print("key: %s , value: %s" % (key, p1_values[key]))
   if p1_values[key] < p1_values[min_index_p1]:
       min_index_p1 = key
       min_value = p1_values[key]
       print(p1_values[key])

    



print("*****************")

#new_sorted = original_data.sort(reverse=True, key=(key_priority))

# correct
new_list = sorted(original_data, key=lambda x: (x[key_priority[0]], x[key_priority[1]])) 

print(new_list)


result = [{'a':0, 'b':10, 'c':8},
{'a':1, 'b':10, 'c':8},
{'a':2, 'b':1, 'c':5}, 
{'a':2, 'b':3, 'c':4},
{'a':2, 'b':3, 'c':5}]

print(result == new_list)