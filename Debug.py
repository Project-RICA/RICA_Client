from AccountDataManager import RICAAccount


# Constants for debugging
SHOW_INTRODUCTION = "force_to_show_introduction"
SELECT_MENU_AUTOMATICALLY = "select_menu_automatically_at_startup"


def debug(opt):
    return RICAAccount.rdat["debug"][opt]
