from typing import Dict


def get_full_name(description: str) -> Dict[str, str]:
    full_name = description.strip().split()
    borrower_data = {
        "last_name": full_name[0],
        "first_name": full_name[1],
    }
    if len(full_name) >= 3:
        borrower_data["middle_name"] = full_name[2]
    return borrower_data
