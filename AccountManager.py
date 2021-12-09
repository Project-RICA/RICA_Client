import os
import json


class RICAAccount:
    user = None

    @classmethod
    def check_rdat(cls):
        if not os.path.isfile("setting.rdat"):
            cls.generate_rdat()

    @staticmethod
    def generate_rdat():
        with open("setting.rdat", 'w') as f:
            dump_str = {
                "rica_account":
                    {
                        "id": "",
                        "pw": ""
                    },
                "client_setting": {
                    "showed_instruction": False
                    }
            }
            json.dump(dump_str, f)
            print("Generated .rdat")

    def update_data(self):
        pass
