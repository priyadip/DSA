import sys
input = sys.stdin.readline
output = sys.stdout.write

def knroll(wt, vl, W):
    n = len(wt)
    dp = [0]*(W+1)
    for i in range(n):
        for j in range(W, wt[i]-1, -1):
            if (new := dp[j - wt[i]] + vl[i]) > dp[j]:
                dp[j] = new
    return dp[W]

if __name__ == "__main__":
    weight = list(map(int, input().split()))
    price = list(map(int, input().split()))
    cap = int(input())
    output(f"Answer is {knroll(weight, price, cap)}\n")
