import time
class TokenBucket:
    def __init__(self,rate,capacity):
        self.rate=rate; self.capacity=capacity; self.tokens=capacity; self.last=time.time()
    def allow(self,tokens=1):
        now=time.time(); self.tokens=min(self.capacity,self.tokens+(now-self.last)*self.rate); self.last=now
        if self.tokens>=tokens: self.tokens-=tokens; return True
        return False
class SlidingWindow:
    def __init__(self,limit,window_sec):
        self.limit=limit; self.window=window_sec; self.timestamps=[]
    def allow(self):
        now=time.time()
        self.timestamps=[t for t in self.timestamps if now-t<self.window]
        if len(self.timestamps)<self.limit: self.timestamps.append(now); return True
        return False
class LeakyBucket:
    def __init__(self,rate,capacity):
        self.rate=rate; self.capacity=capacity; self.water=0; self.last=time.time()
    def allow(self):
        now=time.time(); self.water=max(0,self.water-(now-self.last)*self.rate); self.last=now
        if self.water<self.capacity: self.water+=1; return True
        return False
if __name__=="__main__":
    tb=TokenBucket(10,10)
    assert all(tb.allow() for _ in range(10))
    assert not tb.allow()
    time.sleep(0.11)
    assert tb.allow()
    sw=SlidingWindow(5,1.0)
    assert all(sw.allow() for _ in range(5))
    assert not sw.allow()
    lb=LeakyBucket(10,5)
    assert all(lb.allow() for _ in range(5))
    assert not lb.allow()
    print("Rate limiters: token bucket, sliding window, leaky bucket all working")
    print("All tests passed!")
