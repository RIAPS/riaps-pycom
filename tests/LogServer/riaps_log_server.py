import dotenv
import os
import riaps.log.main

dotenv.load_dotenv(dotenv_path="sample_config/.env",
                   override=True)

home = os.getenv('RIAPSHOME')

if __name__ == '__main__':
    riaps.log.main.main()
