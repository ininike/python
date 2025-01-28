
import time
'''test of mp'''
__version__ = '0.1'
import multiprocessing

input = [1,2,3,4,5]

def producer(q, i):
        time.sleep(2)
        q.put(input[i])
    

def consumer(q):
    results = []
    for x in input:
        item = q.get()
        if item == None:
            break
        
        print(item)
        results.append(item)
    q.put(results)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    q = multiprocessing.SimpleQueue()
    c = multiprocessing.Process(target=consumer, args=(q,))
    c.start()
    for x in range(len(input)):
        p = multiprocessing.Process(target=producer, args=(q, x))
        p.start()
    
    c.join();p.join()
    print(q.get())

