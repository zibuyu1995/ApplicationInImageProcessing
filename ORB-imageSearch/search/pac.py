# coding=utf-8
def pac(des):
    average = np.mean(des, axis=0)
    m, n = np.shape(des)
    meanRemoved = des - np.tile(average, (m,1))
    normData = meanRemoved / np.std(des)
    covMat = np.cov(normData.T)
    eigValue, eigVec = np.linalg.eig(covMat)
    eigValInd = np.argsort(-eigValue)
    selectVec = np.matrix(eigVec.T[:3])
    finalData = normData * selectVec.T
    return des
