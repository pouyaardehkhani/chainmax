"""Persistent isolated workers with wall-time and resident-memory enforcement."""
import multiprocessing as mp
import queue
import time
import psutil


def worker(inbox, outbox):
    from .pipeline import make_candidate
    while True:
        job = inbox.get()
        if job is None:
            return
        try:
            outbox.put((True,make_candidate(job)))
        except Exception as e:
            import traceback
            outbox.put((False,{"status":"MALFORMED_OR_ERROR","error":str(e),"traceback":traceback.format_exc()}))


class Pool:
    def __init__(self, count, seconds, memory_mb):
        self.context = mp.get_context("spawn")
        self.seconds, self.memory_mb = seconds, memory_mb
        self.slots = [self.start() for _ in range(count)]

    def start(self):
        inbox, outbox = self.context.Queue(), self.context.Queue()
        p = self.context.Process(target=worker,args=(inbox,outbox),daemon=True)
        p.start()
        return {"process":p,"inbox":inbox,"outbox":outbox,"job":None,"started":None}

    def submit(self, job):
        for s in self.slots:
            if s["job"] is None:
                s["job"],s["started"] = job,time.monotonic()
                s["inbox"].put(job)
                return True
        return False

    def poll(self):
        for i,s in enumerate(self.slots):
            if s["job"] is None:
                continue
            try:
                ok, result = s["outbox"].get_nowait()
                job,s["job"] = s["job"],None
                return job,result
            except queue.Empty:
                pass
            reason = None
            if not s["process"].is_alive():
                reason = "RESOURCE_FAILURE"
            elif time.monotonic()-s["started"] > self.seconds:
                reason = "TIMEOUT"
            else:
                try:
                    rss = psutil.Process(s["process"].pid).memory_info().rss/1024**2
                    if rss > self.memory_mb:
                        reason = "RESOURCE_FAILURE"
                except psutil.NoSuchProcess:
                    reason = "RESOURCE_FAILURE"
            if reason:
                job = s["job"]
                s["process"].terminate()
                s["process"].join()
                s["inbox"].close()
                s["outbox"].close()
                self.slots[i] = self.start()
                return job,{"status":reason,"error":"worker exceeded resource limit or exited"}
        return None

    def close(self):
        for s in self.slots:
            s["inbox"].put(None)
        for s in self.slots:
            s["process"].join(timeout=2)
            if s["process"].is_alive():
                s["process"].terminate()
                s["process"].join()
            s["inbox"].close()
            s["outbox"].close()
