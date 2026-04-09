# Binary Search

## Definition

Binary search is an algorithm for finding a value in a sorted list by repeatedly checking the middle element and reducing the search interval by half.

## Precondition

The input list must be sorted. If the list is not sorted, binary search can return wrong results.

## Steps

1. Set low to 0 and high to n-1.
2. Find mid as low + (high - low) // 2.
3. Compare the target with list[mid].
4. If equal, return the index.
5. If target is smaller, move high to mid - 1.
6. If target is larger, move low to mid + 1.
7. Repeat until low > high.

## Complexity

Time complexity is O(log n), space complexity is O(1) in iterative form.

## Common Mistakes

- Forgetting the sorted-array condition.
- Off-by-one boundary updates.
- Midpoint overflow in some languages when using (low + high) // 2 directly.
