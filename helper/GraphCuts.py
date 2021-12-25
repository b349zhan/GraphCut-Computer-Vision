import numpy as np
import maxflow
from skimage.color import rgb2grey
from numpy.linalg import norm
from sklearn.mixture import GaussianMixture
from error_handling import Figure, GraphCutsPresenter
class GraphCuts:
    bgr_value = 0
    obj_value = 1
    none_value = 2
    
    def __init__(self, img, sigma, l):
        self.fig = Figure()
        self.pres = GraphCutsPresenter(img, self)
        self.pres.connect_figure(self.fig)

        self.num_rows = img.shape[0]
        self.num_cols = img.shape[1]
        self.img = img
        self.sigma = sigma
        self.l = l
        self.backgroundCost = np.zeros(img.shape[:2])
        self.objectCost = np.zeros(img.shape[:2])
        
    def run(self):
        self.fig.show()

    def compute_labels(self, seed_mask):
        num_rows = self.num_rows
        num_cols = self.num_cols
        
        ## Initialize the graph
        graph = maxflow.GraphFloat()
        nodeids = graph.add_grid_nodes((num_rows, num_cols))
        structure_x = np.array([[0, 0, 0],
                        [0, 0, 1],
                        [0, 0, 0]])
                        
        structure_y = np.array([[0, 0, 0],
                        [0, 0, 0],
                        [0, 1, 0]])
        
        ## Adding the x edges' weight (lambda integrated inside)
        rightImg = np.roll(self.img, -1, axis = 1)
        rightWeight = self.l * np.exp(-norm(self.img - rightImg, axis = 2)**2/self.sigma**2)
        graph.add_grid_edges(nodeids, weights=rightWeight, structure=structure_x, symmetric=True)
        
        ## Adding the y edges' weight (lambda integrated inside)
        belowImg = np.roll(self.img, -1, axis = 0)
        belowWeight = self.l * np.exp(-norm(self.img - belowImg, axis = 2)**2/self.sigma**2)
        graph.add_grid_edges(nodeids, weights=belowWeight, structure=structure_y, symmetric=True)
        
        ## Getting the user clicked pixels for background and object
        backgroundSelectedPixels = self.img[seed_mask == self.bgr_value]
        backgroundSelectedCount = backgroundSelectedPixels.shape[0]
        
        objectSelectedPixels = self.img[seed_mask == self.obj_value]
        objectSelectedCount = objectSelectedPixels.shape[0]
        ## Compute the cost
        backgroundCost = np.zeros(self.img.shape[:2])
        objectCost = np.zeros(self.img.shape[:2])
        if backgroundSelectedCount > 0:
            if backgroundSelectedCount > 6:
                backgroundGMM = GaussianMixture(n_components = 6).fit(backgroundSelectedPixels)
                backgroundCost = backgroundGMM.score_samples(self.img.reshape(-1,3)).reshape(num_rows, num_cols)
        
        if objectSelectedCount > 0:
            if objectSelectedCount > 6:
                objectGMM = GaussianMixture(n_components = 6).fit(objectSelectedPixels)
                objectCost = objectGMM.score_samples(self.img.reshape(-1,3)).reshape(num_rows, num_cols)
                
        ## Setup terminal cost to be super big
        backgroundCost[seed_mask == self.bgr_value] = 10000 * self.l
        graph.add_grid_tedges(nodeids, 0, backgroundCost)
        
        objectCost[seed_mask == self.obj_value] = 10000 * self.l
        graph.add_grid_tedges(nodeids, objectCost, 0)
        
        ## Perform Optimization
        graph.maxflow()    
        # +---------+---------+
        # |         |         |
        # |   bgr   |  none   |
        # |         |         |
        # +---------+---------+
        # |         |         |
        # |  none   |   obj   |
        # |         |         |
        # +---------+---------+
        label_mask = graph.get_grid_segments(nodeids)
        label_mask = np.where(label_mask, self.bgr_value, self.obj_value)
        return label_mask