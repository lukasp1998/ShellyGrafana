t_IP = 10.0.1.222

def getDashboard():

    resp = requests.get('http://' + t_IP + '/api/dashboards/db')



if __name__ == '__main__':
    #setDebug(True)
    getDashboard()