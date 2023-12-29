# implementation of min heap on error values of edges

class MinHeap:
    def __init__(self, edges):
        self.heap = edges.copy()
        self.heapify()

    def __len__(self):
        return len(self.heap)
    
    def __contains__(self, edge):
        return edge.heap_index < len(self.heap) and len(self.heap) > 0
    
    def print_heap(self):
        print([e.error.round(2) for e in self.heap])
    
    #----------------------------------------------
    # sift down withouth recursion
    #----------------------------------------------
    # edge -- a simplex of dimension 1
    # edge.error -- priority value
    # edge.heap_index -- index of edge in heap
    def sift_down(self, edge):
        # while edge is not a leaf
        while edge.heap_index < len(self.heap)//2:
            # get children
            i = edge.heap_index
            c1 = 2*i+1
            c2 = 2*i+2
            # get child with min priority
            if c2 < len(self.heap) and self.heap[c2].error < self.heap[c1].error:
                c = c2
            else:
                c = c1
            # swap if child has higher priority
            if self.heap[c].error < edge.error:
                self.heap[i], self.heap[c] = self.heap[c], self.heap[i]
                self.heap[i].heap_index = i
                self.heap[c].heap_index = c
                edge = self.heap[c]
            else:
                break
    
    #----------------------------------------------
    # sift up withouth recursion
    #----------------------------------------------
    # edge -- a simplex of dimension 1
    # edge.error -- priority value
    # edge.heap_index -- index of edge in heap
    def sift_up(self, edge):
        # while edge is not a root
        while edge.heap_index > 0:
            # get parent
            i = edge.heap_index
            p = (i-1)//2
            # swap if parent has lower priority
            if self.heap[p].error > edge.error:
                self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
                self.heap[i].heap_index = i
                self.heap[p].heap_index = p
                edge = self.heap[p]
            else:
                break
    
    #----------------------------------------------
    # heapify in O(n) using sift_down
    #----------------------------------------------
    def heapify(self):
        # set heap_index
        for i, edge in enumerate(self.heap):
            edge.heap_index = i
        # sift_down every edge, starting from the last non-leaf
        for i in range(len(self.heap)//2)[::-1]:
            self.sift_down(self.heap[i])

    #----------------------------------------------
    # pop edge with min priority
    #----------------------------------------------
    def pop(self):
        # commented, because it is not needed in the current implementation of the algorithm
        #if len(self.heap) == 0:
        #    return None
        e = self.heap[0]
        self.remove(e)
        return e
    
    #----------------------------------------------
    # get min value
    #----------------------------------------------
    def min(self):
        return self.heap[0].error
    
    #----------------------------------------------
    # update priority of edge
    #----------------------------------------------
    # priority can potentially increase or decrease
    def update(self, edge):
        self.sift_down(edge)
        self.sift_up(edge)

    #----------------------------------------------
    # remove edge from heap
    #----------------------------------------------
    def remove(self, edge):
        i = edge.heap_index
        #print(i, len(self.heap))
        #print(self.verify_indexes())
        # if edge is the last element - or the only element
        if edge.heap_index == len(self.heap)-1:
            self.heap.pop()
            return
        # swap edge with last element
        self.heap[-1].heap_index, edge.heap_index = i, len(self.heap)-1
        self.heap[i], self.heap[-1] = self.heap[-1], self.heap[i]
        # remove last element
        self.heap.pop()
        # sift down the new element
        self.sift_down(self.heap[i])

    def verify_indexes(self):
        for i, edge in enumerate(self.heap):
            if edge.heap_index != i:
                print("Error: heap index of edge", edge.id, "is", edge.heap_index, "but should be", i)
                return False
        return True
    

