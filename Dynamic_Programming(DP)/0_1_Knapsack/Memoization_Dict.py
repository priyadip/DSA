import sys
input = sys.stdin.readline
output = sys.stdout.write

def knap(wt,pr,M):
    n = len(wt)
    dp = {}
    
    def fn(i,w):
        if i<0 or w<=0: return 0 

        if (i,w) in dp: return dp[(i,w)]

        skip = fn(i-1,w)
        take = 0
        if wt[i] <= w: take = pr[i] + fn(i-1, w-wt[i])

        return (dp[(i,w)] := max(skip, take))
    
    return fn(n-1,M)

if __name__  == "__main__":
    weight = list(map(int, input().split()))
    price = list(map(int, input().split()))
    cap = int(input())
    output(f"max profit : {knap(weight,price,cap)}\n")
