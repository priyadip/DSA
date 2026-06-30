import sys
input = sys.stdin.readline
output = sys.stdout.write

def kn(wt,pr,M):
    n = len(wt)
    dp=[[0]*(M+1) for _ in range(n+1)]
    for i in range(1,n+1):
        for w in range(1, M+1):
            if wt[i-1]>w:
                dp[i][w] = dp[i-1][w]
            else:
                skip = dp[i-1][w]
                take = pr[i-1] + dp[i-1][w-wt[i-1]]
                dp[i][w] = max(skip, take)
    return dp[n][M]
if __name__ == "__main__":
    weight = list (map(int, input().split()))
    price = list( map(int, input().split()))
    cap = int(input())
    ans = kn(weight, price, cap)
    output(f"max profit: {ans}\n")

