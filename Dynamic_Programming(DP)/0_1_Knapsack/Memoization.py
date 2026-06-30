import sys
input = sys.stdin.readline
output = sys.stdout.write

def knap(wt, pr, M):
    n = len(wt)
    DT = [[-1] * (M+1) for _ in range(n+1)]
    def val(i,M):
        if i < 0 or M <= 0: return 0
        if DT[i][M] != -1: return DT[i][M]
        if wt[i] > M: return val(i-1,M)
        else:
            skip = val(i-1,M)
            take = pr[i] + val(i-1, M-wt[i])
            return (DT[i][M] := max(skip, take))
    return val(n-1, M)

if __name__=="__main__":
    weight=list(map(int,input().split()))
    price = list(map(int , input().split()))
    cap=int (input())
    res=knap(weight,price,cap)
    output(f"Maximum Profit =  {res}\n")

