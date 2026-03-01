```python
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):
            if i != j and nums[i] + nums[j] == target:
                return i, j
    return None
```
Potential issues: O(n^2), duplicate pairs.

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)
```
