#############################################################################################
# $$\      $$\ $$\   $$\     $$\                                          $$\ $$\           #
# $$$\    $$$ |\__|  $$ |    $$ |                                         $$ |\__|          #
# $$$$\  $$$$ |$$\ $$$$$$\   $$$$$$$\   $$$$$$\  $$$$$$\  $$$$$$$\   $$$$$$$ |$$\  $$$$$$\  #
# $$\$$\$$ $$ |$$ |\_$$  _|  $$  __$$\ $$  __$$\ \____$$\ $$  __$$\ $$  __$$ |$$ |$$  __$$\ #
# $$ \$$$  $$ |$$ |  $$ |    $$ |  $$ |$$ |  \__|$$$$$$$ |$$ |  $$ |$$ /  $$ |$$ |$$ |  \__|#
# $$ |\$  /$$ |$$ |  $$ |$$\ $$ |  $$ |$$ |     $$  __$$ |$$ |  $$ |$$ |  $$ |$$ |$$ |      #
# $$ | \_/ $$ |$$ |  \$$$$  |$$ |  $$ |$$ |     \$$$$$$$ |$$ |  $$ |\$$$$$$$ |$$ |$$ |      #
# \__|     \__|\__|   \____/ \__|  \__|\__|      \_______|\__|  \__| \_______|\__|\__|      #
#############################################################################################
                                                                                          
###############################################################
#                             _,-                             # 
#   (¨¨)                 _,-','                               # 
#     \\              ,-"  ,'                                 # 
#      \\           ,'   ,'                                   # 
#       \\        _:.----__.-."-._,-._                        # 
#        \\    .-".:--`:::::.:.:'  )  `-.                     # 
#         \\   `. ::L .::::::'`-._  (  ) :                    # 
#          \\    ":::::::'  `-.   `-_ ) ,'                    # 
#           \\.._/_`:::,' `.     .  `-:                       # 
#           :" _   "\"" `-_    .    `  `.                     # 
#            "\\"":--\     `-.__ ` .     `.                   # 
#              \\'::  \    _-"__`--.__ `  . `.     _,--..-    # 
#               \\ ::  \_-":)(        ""-._ ` `.-''           # 
#                \\`:`-":::/ \\ .   .      `-.  :             # 
#                :\\:::::::'  \\     `    .   `. :            # 
#                 :\\:':':'  . \\           `,  : :           # 
#                 : \\     .    \\      .       `. :       ,- # 
#                __`:\\      .   \\ .   `  ,'    ,: :   ,-'   # 
#         _,---""  :  \\ '        \\  .          :-"  ,'      # 
#     ,-""        :    \\:  .  :   \\  `  '     ,'   /        # 
#    '            :  :  \       .   \\   .   _,'  ,-'         # 
#                :  .   '       :   :`   `,-' ,--'            # 
#                 :     :   :      ,'-._,' ,-'                # 
#                 _:     :        :8:  ,--'                   # 
#                :dd`-._,'-._.__-""' ,'                       # 
#                              ,----'                         # 
#                       _.----'                               # 
#               __..--""                                      # 
#             ""                                              # 
#                                                             #
############################################################### 

"""
API para criação e manipulação de ordens de serviço.
"""
import graphene
import graphql_jwt
import jobs.schema as jobs
import service_orders.schema as service
import users.schema as users
import login.schema as logins


class Query(logins.Query, jobs.Query, service.Query, users.Query, graphene.ObjectType):
    pass


class Mutation(logins.Mutation, jobs.Mutation, service.Mutation, users.Mutation, graphene.ObjectType):
    # token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # aux = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im1pdGhyYW5kaXQiLCJleHAiOjE1ODk0MTAyMTksIm9yaWdfaWF0IjoxNTg5NDA5OTE5fQ.3wWodE1H8m1IjyodsDl2144BcZmgFkBqGecujQw-9cQ'
    # verify_token = graphql_jwt.Verify.Field()
    # refresh_token = graphql_jwt.Refresh.Field()
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
