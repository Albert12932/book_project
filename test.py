from queue import PriorityQueue
def top_k(nums, k):
        freq_count = {}
        for num in nums:
            if num in freq_count:
                freq_count[num] += 1
            else:
                freq_count[num] = 1
        pq = PriorityQueue()
        for num, count in freq_count.items():
            pq.put((-count, num))
        result = []
        for _ in range(k):
            result.append(pq.get()[1])
        return result
        
nums = (1, 1, 1, 2, 2, 3, 1, 4, 7, 8, 7, 6, 7, 3, 6, 2, 1)
k = 3
top_k = top_k(nums, k)
print(top_k)
