import time
import requests
from datetime import datetime



def checkcommentspr(OWNER, REPO, PR_NUMBER, github_token):
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    def verificar_status_pr():
        url = f'https://api.github.com/repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pr_data = response.json()
            #print(pr_data)
            estado = pr_data['state']
            mergeado = pr_data['merged']
            comments = pr_data['comments']
            review_comments = pr_data['review_comments']
            print(f"comments: {comments}")
            print(f"review_comments: {review_comments}")
            if mergeado:
                return 'Aprovado e mergeado ✅'
            elif estado == 'closed':
                return 'Rejeitado ❌'
            else:
                return 'Aberto ⏳'
        else:
            return f'Erro: {response.status_code}'
        
    def checkcomments():

        url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{PR_NUMBER}/comments"
        response = requests.get(url)
        if response.status_code == 200:
            comments = response.json() 
            if comments:
                latest_comment = max(
                    comments, 
                    key=lambda c: datetime.strptime(c['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                )
                review_comment = latest_comment['body']
                return review_comment
        else:
            print(f"Erro ao acessar a API: {response.status_code}")

    def checkreviewcomments():
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}/comments"
        response = requests.get(url)
        if response.status_code == 200:
            comments = response.json()
            if comments:
                latest_comment = max(
                    comments, 
                    key=lambda c: datetime.strptime(c['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                )
                review_comment = latest_comment['body']
                return review_comment
        else:
            print(f"Erro ao acessar a API: {response.status_code}")

    while True:
        status = verificar_status_pr()
        comments = checkcomments()
        review_comments = checkreviewcomments()
        time.sleep(30)  
        if comments:
            return {"Pull Request Status": f"{status}", "message": f"Review Comment: {comments}"}
          
        if review_comments:
            return {"Pull Request Status": f"{status}", "message": f"Review Human Comment: {review_comments}"}
                


        



    
        

