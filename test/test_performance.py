from typing import Any, Dict, List
from time import perf_counter
from db_properties import UserAttr
from internal import generate_id
from properties import (
    PacketHeader,
    RequestField,
    ResponseField,
)
from lambda_function import TestRequest
from lambda_function import lambda_handler

mock_id = generate_id(UserAttr.SORT_KEY_PREFIX)
debug_request = {
    PacketHeader.REQUEST: TestRequest.ONE.value,
    RequestField.User.ID: mock_id,
}
debug_name = "test.one:View.debug"
error_message = "hello world"
error_request = {
    PacketHeader.REQUEST: TestRequest.THREE.value,
    ResponseField.Generic.Error.MESSAGE: error_message,
}
error_name = "test.three:View.error"
generic_request = {
    PacketHeader.REQUEST: TestRequest.TWO.value,
    ResponseField.Generic.RESULTS: True,
}
generic_name = "test.two:View.generic"
test_range = range(100000)


class TestPerformance:
    alive: str = ""

    @classmethod
    def run_handler(cls, request: Dict[str, Any], test_name: str) -> Dict[str, str]:
        t1 = perf_counter()
        output_str: str = lambda_handler(request, None)
        end1 = perf_counter()
        cls.alive = output_str
        t2 = perf_counter()
        for _ in test_range:
            output_str: str = lambda_handler(request, None)
        end2 = perf_counter()
        print(
            f"'{test_name}'\t:\tx1 {((end1-t1)*1000000):.1f}us\tx{test_range[-1]+1} {end2-t2:.3f}s"
        )
        cls.alive = output_str
        return {
            "Name": test_name,
            "x1": f"{((end1-t1)*1000000):.1f}us",
            f"x{test_range[-1]+1}": f"{end2-t2:.3f}s",
        }

    @classmethod
    def time_requests(cls) -> List[Dict[str, str]]:
        return [
            cls.run_handler(generic_request, generic_name),
            cls.run_handler(error_request, error_name),
            cls.run_handler(debug_request, debug_name),
        ]


# import getpass
# import socket
# from csv import DictWriter
# from datetime import datetime
#
# batch_one = TestPerformance.time_requests()
# print()
# batch_two = TestPerformance.time_requests()
# print("\nIt's all ogre now.")
#
#
# data = batch_one + batch_two
# with open(
#     f"{getpass.getuser()}@{socket.gethostname()}_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt",
#     "w",
# ) as r_file:
#     csv_writer = DictWriter(
#         r_file, fieldnames=["Name", "x1", f"x{test_range[-1]+1}"], delimiter="\t"
#     )
#     csv_writer.writeheader()
#     for entry in data:
#         csv_writer.writerow(entry)
