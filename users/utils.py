def is_admin(user):
    return user.groups.filter(name="admin").exists()


def is_borrower(user):
    return user.groups.filter(name="borrower").exists()


def is_investor(user):
    return user.groups.filter(name="investor").exists()