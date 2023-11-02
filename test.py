

def test(error):
    global cumu_error
    if e==1:
        cumu_error = 0
    cumu_error += error
    
error = [1,2,3]

for e in error:
    test(e)
    
print(cumu_error)





