import os
import json
import utils
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

import Debug


def debug(opt):
    return RICAAccount.rdat["debug"][opt]







class FireBase:
    @classmethod
    def connect(cls):
        default_app = firebase_admin.initialize_app()
        cred = credentials.RefreshToken('path/to/refreshToken.json')
        default_app = firebase_admin.initialize_app(cred)


class RICAAccount:
    rdat = None  # After rdat updated, other modules will use this to get rdat file's information.

    @classmethod
    def check_rdat(cls):
        if not os.path.isfile("setting.rdat"):
            cls.generate_rdat()
        cls.login()

    @classmethod
    def generate_rdat(cls):
        with open("setting.rdat", 'w') as f:
            cls.rdat = {
                "rica_account":
                    {
                        "id": "",
                        "pw": ""
                    },
                "client_setting": {
                    "showed_instruction": False,
                    "restore_bad_comment": False
                    },
                "debug": {
                    Debug.SHOW_INTRODUCTION: False,
                    Debug.SELECT_MENU_AUTOMATICALLY: False
                    }
            }
            json.dump(cls.rdat, f, indent=4)
            print("Generated .rdat")

    @classmethod
    def update_data(cls):
        with open("setting.rdat", 'w') as f:
            json.dump(cls.rdat, f)
            print("Updated .rdat")

    @classmethod
    def login(cls):
        cls.get_rdat_as_json()
        if cls.rdat["rica_account"]["id"] == "" or cls.rdat["rica_account"]["pw"] == "":
            utils.double_line(40)
            opt = input("RICA Account - Please select option\n\n"
                        "1. 기존 RICA 계정으로 로그인\n"
                        "2. 신규 가입\n\n"
                        "=> ")
            while True:
                ID = input("ID : ")
                PW = input("PW : ")
                if opt == 1:
                    # TODO firebase connect, if ID/PW wrong -> continue
                    # continue
                    pass
                elif opt == 2:
                    # TODO firebase connect, email authentication
                    # continue
                    pass
                cls.rdat["rica_account"]["id"] = ID
                cls.rdat["rica_account"]["pw"] = PW
                cls.update_data()
                break
        # TODO login and synchronizing with firebase server.


    @classmethod
    def get_rdat_as_json(cls):
        f = utils.read_file("setting.rdat")
        if f is None:  # get_rdat_as_json() only runs on the premise that there is a data file.
            raise FileNotFoundError("Incorrect access. This function must be executed after data get ready.")
        with open("setting.rdat", 'r') as f:
            cls.rdat = json.load(f)






class DiscordAccount:
    pass









