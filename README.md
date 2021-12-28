# GraphCut Computer Vision

Implemented interactive graph cut algorithm, which was developed by Professor Yuri Boykov. The general idea is that we want to perform object segmentation. In our case, we want to approximate two continuous hypersurface on the image so that we could separate the object from the image.

The algorithm we are using is Graph Cut algorithm. 

In the algorithm, we have source (s) and sink(t) and a set of non-terminal nodes P. We want to find the minimum cut from the source s to sink t. The cost of a cut C={S,T} is defined summing up the costs/weights of "boundary edges" (p,q) such that p is in S, and q is in T. The below picture is a nice demonstration of graph cut algorithm taken from Professor Boykov's and Professor Veksler's paper. https://cs.uwaterloo.ca/~yboykov/Papers/chapter_04.pdf

<img width="449" alt="Screen Shot 2021-12-28 at 11 14 52 AM" src="https://user-images.githubusercontent.com/54965707/147585592-874703ef-f450-4e8f-b64b-1e1b6a8b0385.png">



![Screen Shot 2021-12-28 at 11 07 31 AM](https://user-images.githubusercontent.com/54965707/147585569-7b6e2e17-1ff4-43dd-9555-5b8ee3e538f5.png)
![Screen Shot 2021-12-28 at 11 07 40 AM](https://user-images.githubusercontent.com/54965707/147585579-96c29e5d-6d4a-47fe-9427-44de1fa6ae39.png)
![Screen Shot 2021-12-28 at 11 07 47 AM](https://user-images.githubusercontent.com/54965707/147585583-ac65a475-28e3-422a-b813-72b2f35c0375.png)
