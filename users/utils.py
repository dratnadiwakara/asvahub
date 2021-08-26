from hub.models import DepositProduct

def is_admin(user):
    return user.groups.filter(name="admin").exists()


def is_borrower(user):
    return user.groups.filter(name="borrower").exists()


def is_investor(user):
    return user.groups.filter(name="investor").exists()


def add_deposit_products():
    for m in [1,3,6,12,15,18,24,36,48,60]:
        print(m)
        for t in ['Normal','Senior Citizen']:
            print(t)
            for i in ["Monthly","Maturity"]:
                print(i)
                dp = DepositProduct(term=m,rate_type=t,interest_payment=i)
                dp.save()