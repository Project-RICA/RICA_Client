import os
import json
import requests
import utils
import Debug


class FireBase:
    # Initialize
    BY_LOGIN = "login"
    BY_REGISTER = "create_account"
    # FireBase Auth response keys
    ID_TOKEN = "idToken"
    LOCAL_ID = "localId"
    EMAIL = "email"
    EXPIRE_TIME = "expiresIn"
    # Query
    CREATE_ACCOUNT = "signUp"
    LOGIN = "signInWithPassword"
    SEND_VERIFICATION_EMAIL = "sendOobCode"
    SEND_PW_RESET_EMAIL = "sendOobCode"
    TOKEN = None
    UID = None


    # noinspection PyTypeChecker
    @classmethod
    def initialize(cls, by) -> bool:
        """
        Get TOKEN and UID from FireBase.
        :return: True when succeeded, False when failed.
        """
        value = None
        if by == cls.BY_LOGIN:
            value = cls.login()
        elif by == cls.BY_REGISTER:
            value = cls.create_account()
        if value == 'Failed':
            return False
        else:  # Allocate
            cls.TOKEN = value[cls.ID_TOKEN]
            cls.UID = value[cls.LOCAL_ID]
            return True


    @classmethod
    def login(cls):
        response = cls.post(cls.LOGIN)
        if response['result'] == 'success':
            return response['value']
        elif response['value'] == 'INVALID_PASSWORD' or response['value'] == 'EMAIL_NOT_FOUND':
            print("로그인 실패 : 이메일 또는 비밀번호가 틀렸습니다.")
        elif response['value'] == 'PASSWORD_LOGIN_DISABLED':
            print("서버가 점검중에 있거나 긴급하게 서버의 사용을 중단했을 가능성이 있습니다. rica.projectrica@gmail.com 으로 문제를 알려주세요.")
        else:  # Unexpected Error
            raise Exception(f"Something went wrong during login. Error message from server: {response['value']}")
        return 'Failed'


    @classmethod
    def create_account(cls):
        response = cls.post(cls.CREATE_ACCOUNT)
        if response['result'] == 'success':
            return response['value']
        elif response['value'] == 'EMAIL_EXISTS':
            print("이미 해당 이메일로 가입된 계정이 존재합니다.")
        elif response['value'] == 'INVALID_EMAIL':
            print("유효하지 않은 이메일입니다. 이메일 주소를 제대로 적어주세요.")
        elif response['value'] == 'WEAK_PASSWORD':
            print("비밀번호는 최소 6자리 이상이어야 합니다.")
        elif response['value'] == 'OPERATION_NOT_ALLOWED':
            print("현재 모종의 사유로 이메일 가입이 불가능한 상태입니다. rica.projectrica@gmail.com 으로 문의해주시기 바랍니다.")
        else:  # Unexpected Error
            raise Exception(f"Something went wrong during registration. Error message from server: {response['value']}")
        return 'Failed'


    @classmethod
    def verify_email(cls) -> bool:
        response = cls.post(cls.SEND_VERIFICATION_EMAIL)
        if response['result'] == 'success':
            return True
        elif response['value'] == 'INVALID_ID_TOKEN':
            print("현재 로그인한 계정과 인증을 시도하려는 계정의 이메일이 다릅니다.")
        elif response['value'] == 'USER_NOT_FOUND':
            print("해당 이메일로 가입한 계정을 찾을 수 없습니다.")
        else:  # Unexpected Error
            raise Exception(f"Something went wrong during verification. Error message from server: {response['value']}")
        return False


    @classmethod
    def reset_pw(cls, email):
        response = cls.post(cls.SEND_PW_RESET_EMAIL, email=email)
        if response['result'] == 'success':
            return True
        elif response['value'] == 'EMAIL_NOT_FOUND':
            print("해당 이메일로 가입된 계정을 찾을 수 없습니다.")
        else:  # Unexpected Error
            raise Exception(f"Something went wrong during finding password. Error message from server: {response['value']}")
        return False


    @classmethod
    def get_token(cls):
        if cls.TOKEN is None:
            raise NotImplementedError("You should allocate token before using this function. You can get token by initialize()")
        return cls.TOKEN


    @classmethod
    def post(cls, query: str, **kwargs) -> dict:
        key = "AIzaSyCIE--2DN4kG90UfQYhhmCAogtHXYYd3n8"  # RICA FireBase web key
        details = None
        headers = None
        if query == cls.CREATE_ACCOUNT or query == cls.LOGIN:
            details = {
                'email': RICAAccount.get_rdat()['rica_account']['email'],
                'password': RICAAccount.get_rdat()['rica_account']['pw'],
                'returnSecureToken': True
            }
        elif query == cls.SEND_VERIFICATION_EMAIL and kwargs[cls.EMAIL] is None:
            headers = {
                'Content-Type': 'application/json',
            }
            details = '{"requestType":"VERIFY_EMAIL","idToken":"' + cls.get_token() + '"}'  # Because get_token use SIGN_UP option, cls.get_token() does not fall into infinite call.
        elif query == cls.SEND_PW_RESET_EMAIL and kwargs[cls.EMAIL] is not None:
            headers = {
                'Content-Type': 'application/json',
            }
            details = '{"requestType":"PASSWORD_RESET","email":"' + kwargs[cls.EMAIL] + '"}'

        response = requests.post(f'https://identitytoolkit.googleapis.com/v1/accounts:{query}?key={key}',
                                 headers=headers, data=details)

        if 'error' in response.json().keys():
            return {'result': 'failed', 'value': response.json()['error']['message']}
        elif 'idToken' in response.json().keys():
            return {'result': 'success', 'value': response.json()}
        elif 'kind' in response.json().keys():
            return {'result': 'success', 'value': response.json()}




class RICAAccount:
    rdat = None


    @classmethod
    def get_rdat(cls):
        if not os.path.isfile("setting.rdat"):  # If there is no .rdat
            cls.generate_rdat()
        elif cls.rdat is None:  # If setting.rdat exist but is not loaded yet
            f = utils.read_file("setting.rdat")
            if f is None:
                raise FileNotFoundError("It seems setting.rdat is deleted instantly by other program or OS.")
            with open("setting.rdat", 'r') as f:
                cls.rdat = json.load(f)
        return cls.rdat


    @classmethod
    def generate_rdat(cls):
        with open("setting.rdat", 'w') as f:
            cls.rdat = {
                "rica_account":
                    {
                        "email": "",
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
    def update_rdat(cls):
        if cls.rdat is None:
            raise NotImplementedError("Cannot update setting.rdat because rdat has not been initialized.")
        with open("setting.rdat", 'w') as f:
            json.dump(cls.rdat, f)
            print("Updated .rdat")


    @classmethod
    def login(cls):
        cls.get_rdat()
        if cls.rdat["rica_account"]["email"] != "" and cls.rdat["rica_account"]["pw"] != "":  # Try to login automatically
            if FireBase.initialize(FireBase.BY_LOGIN):  # If login was successful
                return
            else:
                print("자동 로그인을 시도하던 중 오류가 발생했습니다. 다시 로그인하세요.")
        else:
            print("계정 정보가 손상되었거나 없습니다.\n\n")

        # If failed to login automatically or user data is empty
        utils.double_line(40)
        opt = input("RICA Account - 메뉴를 선택하세요.\n\n"
                    "1. 기존 RICA 계정으로 로그인\n"
                    "2. 신규 가입\n"
                    "3. 비밀번호 재설정\n\n"
                    "=> ")
        utils.double_line(40)
        while True:
            try:
                opt = abs(int(opt))
            except ValueError:
                opt = input('숫자만 입력하세요 => ')
                continue

            if opt > 3:
                opt = input("숫자를 정확히 입력하세요 =>")
                continue
            elif opt != 3:
                EMAIL = input("EMAIL : ")
                PW = input("PW : ")
                cls.rdat["rica_account"]["email"] = EMAIL
                cls.rdat["rica_account"]["pw"] = PW

            if opt == 1:  # Login to existing account
                if not FireBase.initialize(FireBase.BY_LOGIN):
                    continue
            elif opt == 2:  # Create account
                if not FireBase.initialize(FireBase.BY_REGISTER):
                    continue
                if FireBase.verify_email():
                    input(f'{cls.rdat["rica_account"]["email"]}로 인증 메일이 발송되었습니다. 인증을 진행하신 후 엔터를 누르세요.')
                else:
                    raise RuntimeError("인증메일 발송 과정에서 알 수 없는 에러가 발생했습니다. 데이터파일 삭제 후 다시 진행해보세요.")
            elif opt == 3:  # Find pw
                email = input("복구하고자 하는 계정의 이메일을 적으세요 => ")
                if not FireBase.reset_pw(email):
                    continue
                opt = 1
                print("해당 이메일로 비밀번호 재설정 주소가 발송되었습니다. 재설정 후 기존 RICA 계정으로 로그인하세요.")
                continue
            else:
                print()
            break
        cls.update_rdat()  # Save to .rdat when editing is completed




class DiscordAccount:
    pass









