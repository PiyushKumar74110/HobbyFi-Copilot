import json

from datetime import datetime

import os





AUDIT_DIR = "logs"



os.makedirs(

    AUDIT_DIR,

    exist_ok=True

)





AUDIT_FILE = (

    f"{AUDIT_DIR}/audit.log"

)





def audit_log(
    event: str,
    data: dict
):


    record = {


        "event":
        event,


        "timestamp":
        str(
            datetime.utcnow()
        ),


        "data":
        data

    }



    with open(
        AUDIT_FILE,
        "a"
    ) as file:


        file.write(

            json.dumps(
                record,
                default=str
            )

            +

            "\n"

        )