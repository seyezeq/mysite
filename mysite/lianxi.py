l = [9, 6, 5, 6, 6, 7, 8, 9, 6, 0]

def binary_sort(l,item):
    start = 0
    last = len(l) - 1
    
    while start <= last:
        mid = (start+last) // 2
        if item == l[mid]:
            return True
        elif item > l[mid]:
            start = mid +1
        else:
            last = mid - 1
    return False
binary = binary_sort(l,6)
print(binary)