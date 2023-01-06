import dotenv
import os
import riaps.log.main

# dotenv.load_dotenv(dotenv_path="sample_config/.env",
#                    override=True)
#
# home = os.getenv('RIAPSHOME')
# print(home)

if __name__ == '__main__':
    riaps.log.main.main()
    # riaps.log.main.setup(platform=("172.21.20.70", 9020),
    #                      app=None)
    # riaps.log.main.setup(platform=None,
    #                      app=("172.21.20.70", 12345))
    # riaps.log.main.setup(platform=("172.21.20.70", 9020),
    #                      app=("172.21.20.70", 12345))
