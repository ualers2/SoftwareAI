    
from Modules.Resolvers.user_identifier import auth_user, require_user_token, resolve_user_identifier

def user_plan_limit(email, password, logs_collection, app):

    user, _, status = auth_user(email, password, logs_collection, app)

    if status != "success" or not user:
        return False

    numeric_user_id = user.id
    plan_name = user.plan_name
    if plan_name == "Free":
        payload = {
            'price': 0,
            'limit_monthly_tokens': 300000,
            'features': [
                'PR basic automation',
                '5 - 10 PRs/mo',
                'Logs basic'
            ]
        }
    elif plan_name == "Premium":
        payload = {
            'price': 15,
            'limit_monthly_tokens': 3000000,
            'features': [
                'PR Premium automation',
                '20 - 40 PRs/mo',
                'Logs advanced',
                'API access'
            ]
        }
  
    elif plan_name == "Pro":
        payload = {
            'price': 29,
            'limit_monthly_tokens': 10000000,
            'features': [
                'Everything from Premium',
                '60 - 90 PRs/mo',
                'Git Context Layer',
                'Auto-Commit Intelligence',
                'Smart Threshold Detection',
                'Context-Aware Messages'
            ]
        }
    return payload