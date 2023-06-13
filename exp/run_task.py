import colink
import glob
import json
from typing import Dict

# read the colink handler from json file in "users" folder
users = {}
cls: Dict[str, colink.CoLink] = {}
for user_file in glob.glob("./users/*.json"):
    with open(user_file) as f:
        user = json.load(f)
        file_name = user_file.split("/")[-1].split(".")[0]
        users[file_name] = user
        cls[file_name] = colink.CoLink(user["server_url"], user["user_jwt"])

# create a new task, assuming cl0 is the initiator

# load param from json config json

with open("config.json") as f:
    param = json.load(f)

participants = [
    colink.Participant(user_id=d["user_id"], role=d["role"]) for d in param["deployment"]["participants"]
]

for i in range(1,len(users)):
    cls["test-0"].update_entry(
        "_internal:known_users:{}:guest_jwt".format(users["test-{}".format(i)]["user_id"]),
        users["test-{}".format(i)]["user_jwt"],
    )
    cls["test-0"].update_entry(
        "_internal:known_users:{}:core_addr".format(users["test-{}".format(i)]["user_id"]),
        users["test-{}".format(i)]["server_url"],
    )
    cls["test-{}".format(i)].update_entry(
        "_internal:known_users:{}:guest_jwt".format(users["test-0"]["user_id"]),
        users["test-0"]["user_jwt"],
    )
    cls["test-{}".format(i)].update_entry(
        "_internal:known_users:{}:core_addr".format(users["test-0"]["user_id"]),
        users["test-0"]["server_url"],
    )

task_id = cls["test-0"].run_task("unifed.crypten", json.dumps(param), participants, True)
print("task_id: ", task_id)
cls["test-0"].wait_task(task_id)
print("task finished")

example_log_from_server = cls["test-0"].read_entry(f"unifed:task:{task_id}:return")
print("return from server 0:")
print(example_log_from_server)
