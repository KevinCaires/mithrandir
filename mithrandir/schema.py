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
import login.schema as logins
import profiles.schema as profiles


class Query(
    jobs.Query,
    logins.Query,
    service.Query, 
    graphene.ObjectType
):
    pass


class Mutation(
    jobs.Mutation,
    logins.Mutation,
    profiles.Mutation,
    service.Mutation,
    graphene.ObjectType,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
