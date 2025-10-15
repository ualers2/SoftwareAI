    
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
            'price': 5,
            'limit_monthly_tokens': 1000000,
            'features': [
                'PR Premium automation',
                '1 million monthly tokens',
                '20 - 40 PRs/mo',
                'Logs advanced',
                'API access'
            ],
            'payment_link': ''
        },
        "Pro": {
            'price': 29,
            'limit_monthly_tokens': 10000000,
            'features': [
                'Everything from Premium',
                '10 million monthly tokens',
                '60 - 90 PRs/mo',
                'Git Context Layer',
                'Auto-Commit Intelligence',
                'Smart Threshold Detection',
                'Context-Aware Messages'
            ],
            'payment_link': ''
        }
    }