import dotenv
import os
import riaps.log.app_server

dotenv.load_dotenv(dotenv_path="sample_config/.env",
                   override=True)

home = os.getenv('RIAPSHOME')

if __name__ == '__main__':
    riaps.log.app_server.main()
