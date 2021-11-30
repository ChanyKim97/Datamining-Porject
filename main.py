import cf

CF_user = cf.CF('chun', 3)
#print(CF_user.recommendation())

CF_recommendation_list = CF_user.recommendation()
print(CF_recommendation_list)