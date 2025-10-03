    
def get_plans_data():
    return {
        "Free": {
            'price': 0,
            'limit_monthly_tokens': 300000,
            'features': [
                'PR basic automation',
                '5 - 10 PRs/mo',
                'Logs basic'
            ],
            'payment_link': ''
        },
        "Premium": {
            'price': 15,
            'limit_monthly_tokens': 3000000,
            'features': [
                'PR Premium automation',
                '20 - 40 PRs/mo',
                'Logs advanced',
                'API access'
            ],
            'payment_link': 'teste 123'
        },
        "Pro": {
            'price': 29,
            'limit_monthly_tokens': 10000000,
            'features': [
                'Everything from Premium',
                '60 - 90 PRs/mo',
                'Git Context Layer',
                'Auto-Commit Intelligence',
                'Smart Threshold Detection',
                'Context-Aware Messages'
            ],
            'payment_link': 'teste 123'
        }
    }