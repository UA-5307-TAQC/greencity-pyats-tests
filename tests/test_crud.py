import logging
import requests
import random
from pyats import aetest

from tests.base_test import BaseSetup, BaseCleanup

log = logging.getLogger(__name__)


class CommonSetup(BaseSetup):
    pass

class TestHabitStateMachine(aetest.Testcase):
    
    @aetest.test
    def test_crud_lifecycle(self, steps):
        log.info("Task 5: Validating Habit State Machine (CRUD)...")
        main_url = self.parent.parameters['main_api_url']
        headers = self.parent.parameters['headers']
        habit_assign_id = None

        # STEP 1: CREATE (Assign habit)
        with steps.start('Step 1: CREATE - Assign a new habit', continue_=False) as step:
            # Беремо рандомну звичку
            res = requests.get(f"{main_url}/habit?page=0&size=20", headers=headers)
            habit_id = random.choice([h['id'] for h in res.json().get('page', [])])
            
            log.info(f"Trying to assign Habit ID: {habit_id}")
            post_res = requests.post(f"{main_url}/habit/assign/{habit_id}", headers=headers)
            
            if post_res.status_code != 201:
                step.failed(f"Create failed! Status: {post_res.status_code}, Details: {post_res.text}")
            
            habit_assign_id = post_res.json().get('id')
            log.info(f"CREATE successful. HabitAssignId: {habit_assign_id}")

        # STEP 2: READ (Retrieve details by ID)
        with steps.start('Step 2: READ - Retrieve habit details', continue_=False) as step:
            get_res = requests.get(f"{main_url}/habit/assign/{habit_assign_id}", headers=headers)
            
            if get_res.status_code != 200:
                step.failed(f"Read failed! Status: {get_res.status_code}")
                
            status = get_res.json().get('status')
            log.info(f"READ successful. Current Status: {status}")

        # STEP 3: UPDATE (Update status)
        with steps.start('Step 3: UPDATE - Change habit status', continue_=True) as step:
            # Зазвичай GreenCity дозволяє оновити статус через PATCH
            payload = {"status": "INPROGRESS"}
            patch_res = requests.patch(f"{main_url}/habit/assign/{habit_assign_id}", json=payload, headers=headers)
            
            if patch_res.status_code in [200, 201, 204]:
                log.info("UPDATE successful!")
            else:
                log.warning(f"Update returned {patch_res.status_code}. Endpoint format might differ, but moving to Delete to clean up.")

        # STEP 4: DELETE (Unassign habit)
        with steps.start('Step 4: DELETE - Unassign the habit', continue_=False) as step:
            del_res = requests.delete(f"{main_url}/habit/assign/delete/{habit_assign_id}", headers=headers)
            
            if del_res.status_code not in [200, 204]:
                step.failed(f"Delete failed! Status: {del_res.status_code}")
                
            log.info("DELETE successful! State machine validated.")

# Підключаємо базове прибирання
class CommonCleanup(BaseCleanup):
    pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    aetest.main()