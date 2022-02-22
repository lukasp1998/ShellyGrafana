import requests

t_IP = '10.0.1.222:3000'
query = {'Authorization':'Bearer eyJrIjoiNWdxYTBNQ2tjNzRLZmY0SWE3WlJ1Z0U4ejVSMEpIM3EiLCJuIjoiUHl0aG9uRGFzaGJvYXJkIiwiaWQiOjF9'}

def createNewDashboard():
    null = None
    false = False
    dashboardData={ "dashboard": {
            "id": null,
            "uid": null,
            "title": "Shelly Auto Generated",
            "tags": [ "templated" ],
            "timezone": "browser",
            "schemaVersion": 16,
            "version": 0,
            "refresh": "25s"
              },
              "folderId": 0,
              "folderUid": "",
              "message": "Made changes to xyz",
              "overwrite": false
          }

    resp = requests.post('http://' + t_IP + '/api/dashboards/db', data=dashboardData, params=query)
    print(resp.json())


def getDashboard():
## API Key = eyJrIjoiNWdxYTBNQ2tjNzRLZmY0SWE3WlJ1Z0U4ejVSMEpIM3EiLCJuIjoiUHl0aG9uRGFzaGJvYXJkIiwiaWQiOjF9

    #resp = requests.get('http://' + t_IP + '/api/dashboards/home', params=query)
    resp = requests.get('http://' + t_IP + '/api/dashboards/uid/RyziF-Wgz', params=query)
    print(resp.json())


if __name__ == '__main__':
    #setDebug(True)
    #getDashboard()
    createNewDashboard()